"""
ARCHIVO: middleware/auth_middleware.py

INTERMEDIARIOS DE AUTENTICACION Y SEGURIDAD

Proporciona decoradores funcionales jerarquicos para proteger endpoints y encapsularlos 
con el modelo actual inyectado desde la base activa.
"""
from functools import wraps
from flask import request, jsonify


def require_auth(auth_service):
    """
    DECORADOR DE EXIGENCIA ESTRICTA
    
    Elemento fábrica (Factory wrapper) para validar blindaje algorítmico o de sesión.

    Modo interno natural: Solicita y escanea envíos unívocos correspondientes a una boleta empadronada.
    Modo corporativo Azure: Cruza e intercepta obligatoriamente un token OAuth/JWT adherido al esquema portador Bearer.

    Convencion practica:
        @app.route("/api/protected")
        @require_auth(auth_service)
        def protected_endpoint(current_user):
            return jsonify(current_user)
    """
    def decorator(f):
        @wraps(f)
        def decorated(*args, **kwargs):
            current_user = None

            if auth_service.auth_provider == 'azure':
                # Ruta condicional corporativa usando validez por cabeceras tokenizadas Bearer
                auth_header = request.headers.get('Authorization', '')
                if not auth_header.startswith('Bearer '):
                    return jsonify({"error": "Token de autorización requerido"}), 401

                token = auth_header.split(' ', 1)[1]
                current_user, error = auth_service.login({'azure_token': token})
                if error:
                    return jsonify({"error": error}), 401

            else:
                # Transito basico por omision, sacudiendo boletas extraidas
                boleta = (
                    request.args.get('boleta')
                    or request.headers.get('X-User-Boleta')
                    or (request.get_json(silent=True) or {}).get('boleta')
                )
                if boleta:
                    current_user = auth_service.user_repo.find_by_boleta(boleta)

            # Empaquetado indirecto propagando estado pre-inyectado al controlador subyacente
            kwargs['current_user'] = current_user
            return f(*args, **kwargs)

        return decorated
    return decorator


def optional_auth(auth_service):
    """
    DECORADOR DE CAIDA PASIVA DE AUTENTICACION
    
    Eficaz intermediario que trata silenciosamente intentos inválidos permitiendo resoluciones limpias abiertas.
    Frecuentemente utilizado para recursos con doble nivel de fidelidad o exposición pública generalizada.
    """
    def decorator(f):
        @wraps(f)
        def decorated(*args, **kwargs):
            current_user = None
            try:
                boleta = (
                    request.args.get('boleta')
                    or request.headers.get('X-User-Boleta')
                )
                if boleta:
                    current_user = auth_service.user_repo.find_by_boleta(boleta)
            except Exception:
                pass
            kwargs['current_user'] = current_user
            return f(*args, **kwargs)
        return decorated
    return decorator
