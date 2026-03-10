"""
ARCHIVO: services/auth_service.py

SERVICIO DE AUTENTICACION

Logica de autenticacion desacoplada del controlador web.
Incluye hashing de contrasenas con bcrypt (werkzeug), validacion
de inputs y proteccion contra enumeracion de usuarios.

Soporta dos modos conceptuales:
- local:  Autenticacion por numero de boleta + contrasena
- azure:  Autenticacion via Azure AD con auto-provisionamiento (modo institucional futuro)
"""
import re
import bcrypt
from datetime import datetime
from werkzeug.security import check_password_hash as werkzeug_check


class AuthService:
    """
    CLASE DE SERVICIO DE AUTENTICACION UNIFICADO
    """

    # CONSTANTES DE VALIDACION
    BOLETA_PATTERN = re.compile(r'^\d{7,15}$')  # 7-15 digitos numericos
    MIN_PASSWORD_LENGTH = 6
    MAX_NAME_LENGTH = 100
    MIN_NAME_LENGTH = 2

    def __init__(self, user_repo, auth_provider='local'):
        """
        INICIALIZACION DEL SERVICIO

        Argumentos:
            user_repo: Repositorio de usuarios (SQLite o externo)
            auth_provider: Modo de autenticacion ('local' o 'azure')
        """
        self.user_repo = user_repo
        self.auth_provider = auth_provider

    # -------------------------------------------------------------------
    #  UTILIDADES DE HASHING (bcrypt)
    # -------------------------------------------------------------------

    def _hash_password(self, password):
        """
        Genera un hash bcrypt para la contrasena dada.
        Retorna el hash como cadena de texto.
        """
        return bcrypt.hashpw(
            password.encode('utf-8'),
            bcrypt.gensalt()
        ).decode('utf-8')

    def _verify_password(self, stored_hash, password):
        """
        Verifica una contrasena contra un hash almacenado.
        Soporta migracion transparente: si el hash es pbkdf2/scrypt
        (werkzeug legacy), lo verifica con werkzeug.
        Retorna True si la contrasena es correcta.
        """
        if not stored_hash or not password:
            return False

        # Hash legacy (pbkdf2 o scrypt de werkzeug): verificar con werkzeug
        if stored_hash.startswith(('pbkdf2:', 'scrypt:')):
            return werkzeug_check(stored_hash, password)

        # Hash bcrypt: verificar directamente
        try:
            return bcrypt.checkpw(
                password.encode('utf-8'),
                stored_hash.encode('utf-8')
            )
        except (ValueError, TypeError):
            return False

    def _needs_rehash(self, stored_hash):
        """
        Determina si un hash necesita ser migrado a bcrypt.
        Retorna True si el hash usa un algoritmo legacy.
        """
        if not stored_hash:
            return False
        return stored_hash.startswith(('pbkdf2:', 'scrypt:'))

    def _validate_boleta(self, boleta):
        """
        VALIDAR FORMATO DE BOLETA

        Verifica que la boleta sea una cadena numerica de 7-15 digitos.
        Retorna tupla (valida: bool, mensaje_error: str o None)
        """
        if not boleta or not isinstance(boleta, str):
            return False, "La boleta es requerida"
        boleta = boleta.strip()
        if not self.BOLETA_PATTERN.match(boleta):
            return False, "La boleta debe contener entre 7 y 15 digitos numericos"
        return True, None

    def _validate_password(self, password):
        """
        VALIDAR FORTALEZA DE CONTRASENA

        Verifica longitud minima de la contrasena.
        Retorna tupla (valida: bool, mensaje_error: str o None)
        """
        if not password or not isinstance(password, str):
            return False, "La contrasena es requerida"
        if len(password) < self.MIN_PASSWORD_LENGTH:
            return False, f"La contrasena debe tener al menos {self.MIN_PASSWORD_LENGTH} caracteres"
        return True, None

    def _validate_nombre(self, nombre):
        """
        VALIDAR NOMBRE DEL USUARIO

        Verifica longitud y caracteres basicos del nombre.
        Retorna tupla (valida: bool, mensaje_error: str o None)
        """
        if not nombre or not isinstance(nombre, str):
            return False, "El nombre es requerido"
        nombre = nombre.strip()
        if len(nombre) < self.MIN_NAME_LENGTH:
            return False, f"El nombre debe tener al menos {self.MIN_NAME_LENGTH} caracteres"
        if len(nombre) > self.MAX_NAME_LENGTH:
            return False, f"El nombre no puede exceder {self.MAX_NAME_LENGTH} caracteres"
        return True, None

    def login(self, credentials):
        """
        INICIO DE SESION UNIFICADO

        Argumentos:
            credentials: Diccionario con 'boleta' y 'password', o 'azure_token'

        Retorna:
            tupla: (datos_usuario o None, mensaje_error o None)
        """
        if self.auth_provider == 'azure':
            return self._login_azure(credentials)
        return self._login_local(credentials)

    def check_email(self, email):
        """
        VERIFICAR EXISTENCIA DE CORREO
        """
        user = self.user_repo.find_by_email(email)
        return user, user is not None

    def register(self, data):
        """
        REGISTRAR ALUMNO NUEVO CON CONTRASENA

        Valida inputs, hashea la contrasena con bcrypt y crea el registro.
        """
        boleta = data.get('boleta')
        password = data.get('password')
        nombre = data.get('nombre')

        # Validar boleta
        valid, error = self._validate_boleta(boleta)
        if not valid:
            return None, error

        # Validar nombre
        valid, error = self._validate_nombre(nombre)
        if not valid:
            return None, error

        # Validar contrasena
        valid, error = self._validate_password(password)
        if not valid:
            return None, error

        # Verificar duplicados
        if self.user_repo.exists_by_boleta(boleta):
            return None, "La boleta ya esta registrada"

        # Hashear contrasena con bcrypt
        password_hash = self._hash_password(password)

        # Crear usuario con hash
        create_data = {
            'boleta': boleta.strip(),
            'nombre': nombre.strip(),
            'email': data.get('email'),
            'carrera': data.get('carrera', 'Ingenieria'),
            'vehiculo': data.get('vehiculo', 'ninguno'),
            'id_grupo': data.get('id_grupo'),
            'password_hash': password_hash,
        }
        user = self.user_repo.create(create_data)
        return user, None

    def complete_profile(self, data):
        """
        COMPLETAR PERFIL (FLUJO AZURE)

        Crea cuenta local para usuario autenticado via Azure.
        """
        boleta = data.get('boleta')
        valid, error = self._validate_boleta(boleta)
        if not valid:
            return None, error

        if self.user_repo.exists_by_boleta(boleta):
            return None, "La boleta ya esta registrada"

        # Azure flow: password opcional (la auth es por token)
        password = data.get('password')
        create_data = dict(data)
        if password:
            create_data['password_hash'] = self._hash_password(password)

        user = self.user_repo.create(create_data)
        return user, None

    def update_user(self, boleta, data):
        """
        ACTUALIZAR DATOS DEL ALUMNO
        """
        user = self.user_repo.update(boleta, data)
        if not user:
            return None, "Usuario no encontrado"
        return user, None

    # SECCION DE IMPLEMENTACIONES DE LOGIN

    def _login_local(self, credentials):
        """
        LOGIN LOCAL SEGURO

        Verifica boleta + contrasena usando bcrypt.
        Mensaje de error generico para prevenir enumeracion de usuarios.
        """
        boleta = credentials.get('boleta')
        password = credentials.get('password')

        # Validar formato de boleta
        valid, error = self._validate_boleta(boleta)
        if not valid:
            return None, error

        # Buscar usuario
        user = self.user_repo.find_by_boleta(boleta)
        if not user:
            # Mensaje generico para prevenir enumeracion de usuarios
            return None, "Boleta o contrasena incorrecta"

        # Obtener hash almacenado directamente del modelo
        from models import Alumno
        alumno = Alumno.query.filter_by(boleta=boleta).first()

        # Si el usuario no tiene contrasena (migrado sin password), pedir que la cree
        if not alumno.password_hash:
            return {'needs_password': True, 'boleta': boleta, 'nombre': user.get('nombre')}, None

        # Verificar contrasena (soporta bcrypt y legacy pbkdf2/scrypt)
        if not self._verify_password(alumno.password_hash, password or ''):
            return None, "Boleta o contrasena incorrecta"

        # Migracion transparente: re-hashear a bcrypt si usa formato legacy
        if self._needs_rehash(alumno.password_hash):
            alumno.password_hash = self._hash_password(password)
            from models import db
            db.session.commit()

        # Login exitoso: actualizar last_login
        self.user_repo.update(boleta, {'last_login': datetime.now()})
        return user, None

    def set_password(self, boleta, new_password):
        """
        ESTABLECER CONTRASENA PARA USUARIOS EXISTENTES SIN PASSWORD

        Permite a usuarios migrados (sin contrasena) crear su contrasena.
        """
        valid, error = self._validate_password(new_password)
        if not valid:
            return None, error

        from models import db, Alumno
        alumno = Alumno.query.filter_by(boleta=boleta).first()
        if not alumno:
            return None, "Usuario no encontrado"

        if alumno.password_hash:
            return None, "Este usuario ya tiene contrasena. Usa login normal."

        alumno.password_hash = self._hash_password(new_password)
        db.session.commit()

        return alumno.to_dict(), None

    def _login_azure(self, credentials):
        """
        EJECUCION DE LOGIN EN SERVIDOR AZURE
        
        Suscripción cruzada decodificando el token de Azure AD (modo integrado opcional).

        Flujo estructural:
        1. Recibe ID token de Azure AD desde las cabeceras pasadas por el front-end angular/react
        2. Certifica y cruza el token contra firmas JWKS externas de Microsoft
        3. Identifica al individuo buscando por correo matriz o identificador Azure remoto
        4. Ejerce auto-aprovisionamiento forzado local si no lo logra localizar
        5. Consolida metadatos del usuario persistente devolviéndolos.
        """
        token = credentials.get('azure_token')
        if not token:
            return None, "Token de Azure requerido"

        # Validar token con Azure AD
        claims = self._validate_azure_token(token)
        if not claims:
            return None, "Token de Azure inválido o expirado"

        # Extraer datos del token
        email = claims.get('preferred_username', '')
        name = claims.get('name', '')
        oid = claims.get('oid', '')  # Azure Object ID

        # Buscar por institutional_id primero, luego por email
        user = None
        if oid:
            user = self.user_repo.find_by_institutional_id(oid)
        if not user and email:
            user = self.user_repo.find_by_email(email)

        # Auto-provisioning si no existe
        if not user:
            user = self.user_repo.create({
                'boleta': claims.get('employee_id', f'AZ-{oid[:8]}'),
                'email': email,
                'nombre': name,
                'institutional_id': oid,
                'auth_provider': 'azure_ad',
            })

        # Actualizar last_login
        if user and user.get('boleta'):
            self.user_repo.update(user['boleta'], {
                'last_login': datetime.now()
            })

        return user, None

    def _validate_azure_token(self, token):
        """
        VALIDAR TOKEN WEB JSON (JWT)
        
        Valida que un ticket de autenticación Microsoft posea firmas e identificadores fidedignos.
        (Actualmente actuando como plantilla simulada de marcador de posición)
        
        La escuela deberá instanciar e inyectar sus llaves públicas en variables
        AZURE_TENANT_ID y AZURE_CLIENT_ID para el pase completo hacia la nube.
        
        En producción real en despliegues con red esto deberá:
        1. Descargar las claves públicas rotativas de Azure AD (JWKS).
        2. Ejecutar prueba algorítmica de encriptamiento base.
        3. Medir fecha de expiración y alcance de dominios autorizados.
        4. Vomitar las notificaciones (claims) empaquetadas útiles.
        """
        # Elemento reservado. Sin implementación funcional forzada.
        # La implementación real sería:
        #
        # import jwt
        # import requests
        #
        # jwks_url = f"https://login.microsoftonline.com/{tenant_id}/discovery/v2.0/keys"
        # jwks = requests.get(jwks_url).json()
        #
        # decoded = jwt.decode(
        #     token,
        #     jwks,
        #     algorithms=["RS256"],
        #     audience=client_id,
        #     issuer=f"https://login.microsoftonline.com/{tenant_id}/v2.0"
        # )
        # return decoded
        #
        return None
