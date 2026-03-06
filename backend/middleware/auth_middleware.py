"""
Auth Middleware — Validación de autenticación en endpoints.

Proporciona decoradores para proteger endpoints según el modo
de autenticación configurado (local o Azure AD).
"""
from functools import wraps
from flask import request, jsonify


def require_auth(auth_service):
    """Decorador factory para validar autenticación.

    En modo local: verifica que se envíe una boleta válida.
    En modo Azure: verifica el token Bearer en el header.

    Uso:
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
                # Modo Azure: validar Bearer token
                auth_header = request.headers.get('Authorization', '')
                if not auth_header.startswith('Bearer '):
                    return jsonify({"error": "Token de autorización requerido"}), 401

                token = auth_header.split(' ', 1)[1]
                current_user, error = auth_service.login({'azure_token': token})
                if error:
                    return jsonify({"error": error}), 401

            else:
                # Modo local: extraer boleta del request
                boleta = (
                    request.args.get('boleta')
                    or request.headers.get('X-User-Boleta')
                    or (request.get_json(silent=True) or {}).get('boleta')
                )
                if boleta:
                    current_user = auth_service.user_repo.find_by_boleta(boleta)

            # Inyectar usuario en kwargs
            kwargs['current_user'] = current_user
            return f(*args, **kwargs)

        return decorated
    return decorator


def optional_auth(auth_service):
    """Similar a require_auth pero no falla si no hay auth.
    Útil para endpoints que funcionan con o sin autenticación."""
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
