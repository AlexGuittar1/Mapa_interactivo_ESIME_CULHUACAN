"""
AuthService — Lógica de autenticación desacoplada.

Soporta dos modos:
- local:  Autenticación por número de boleta (modo actual)
- azure:  Autenticación vía Azure AD con auto-provisioning (modo futuro)

El servicio no conoce HTTP ni Flask; solo recibe datos y retorna resultados.
"""
from datetime import datetime


class AuthService:
    """Servicio de autenticación unificado."""

    def __init__(self, user_repo, auth_provider='local'):
        """
        Args:
            user_repo: Instancia de UserRepository
            auth_provider: 'local' o 'azure'
        """
        self.user_repo = user_repo
        self.auth_provider = auth_provider

    def login(self, credentials):
        """Login unificado. Retorna (user_dict, error_string).

        Args:
            credentials: dict con 'boleta' (local) o 'azure_token' (azure)

        Returns:
            tuple: (user_dict or None, error_message or None)
        """
        if self.auth_provider == 'azure':
            return self._login_azure(credentials)
        return self._login_local(credentials)

    def check_email(self, email):
        """Verificar si un correo ya está registrado.

        Returns:
            tuple: (user_dict or None, exists: bool)
        """
        user = self.user_repo.find_by_email(email)
        return user, user is not None

    def register(self, data):
        """Registrar nuevo alumno.

        Returns:
            tuple: (user_dict or None, error_message or None)
        """
        boleta = data.get('boleta')
        if not boleta:
            return None, "La boleta es requerida"

        if self.user_repo.exists_by_boleta(boleta):
            return None, "La boleta ya está registrada"

        user = self.user_repo.create(data)
        return user, None

    def complete_profile(self, data):
        """Completar perfil de usuario (flujo de registro por email).

        Returns:
            tuple: (user_dict or None, error_message or None)
        """
        boleta = data.get('boleta')
        if not boleta:
            return None, "La boleta es requerida"

        if self.user_repo.exists_by_boleta(boleta):
            return None, "La boleta ya está registrada"

        user = self.user_repo.create(data)
        return user, None

    def update_user(self, boleta, data):
        """Actualizar datos del alumno.

        Returns:
            tuple: (user_dict or None, error_message or None)
        """
        user = self.user_repo.update(boleta, data)
        if not user:
            return None, "Usuario no encontrado"
        return user, None

    # --- Implementaciones de login ---

    def _login_local(self, credentials):
        """Login por boleta (modo actual)."""
        boleta = credentials.get('boleta')
        if not boleta:
            return None, "La boleta es requerida"

        user = self.user_repo.find_by_boleta(boleta)
        if not user:
            return None, "Usuario no encontrado"

        # Actualizar last_login si el campo existe
        self.user_repo.update(boleta, {'last_login': datetime.now()})

        return user, None

    def _login_azure(self, credentials):
        """Login por token de Azure AD (modo institucional futuro).

        Flujo:
        1. Recibe ID token de Azure AD desde el frontend
        2. Valida el token contra Azure AD
        3. Busca al usuario por email o institutional_id
        4. Si no existe, auto-provisiona el usuario
        5. Retorna los datos del usuario
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
        """Validar JWT de Azure AD.

        NOTA: Esta es una implementación placeholder.
        La escuela debe configurar AZURE_TENANT_ID y AZURE_CLIENT_ID
        para activar la validación real.

        En producción, este método:
        1. Descarga las claves públicas de Azure AD (JWKS)
        2. Verifica la firma del JWT
        3. Valida issuer, audience, y expiración
        4. Retorna los claims del token

        Requiere: pip install PyJWT cryptography requests
        """
        # Placeholder: no valida nada en modo local
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
