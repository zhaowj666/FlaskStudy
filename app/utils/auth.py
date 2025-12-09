from flask import jsonify, current_app
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity, create_refresh_token, verify_jwt_in_request, get_jwt
from app.models import User, Permissions
from functools import wraps

def authenticate_user(username, password):
    user = User.query.filter_by(username=username, is_active=True).first()
    if user and user.verify_password(password):
        return user
    return None

def create_tokens(user):
    permissions = [perm.name for role in user.roles for perm in role.permissions]
    primary_role = user.roles[0].name if user.roles else None

    additional_claims = {
        'role': primary_role,
        'permissions': permissions,
        'user_id': user.id
    }

    access_token = create_access_token(identity=user.username, additional_claims=additional_claims)
    refresh_token = create_refresh_token(identity=user.username)
    return access_token, refresh_token


def permission_required(permission):
    def decorator(fn):
        @wraps(fn)
        def wrapped(*args, **kwargs):
            verify_jwt_in_request()
            claims = get_jwt()
            user_permissions = claims.get('permissions', [])

            if permission not in user_permissions:
                current_user = claims.get('sub')
                current_app.logger.warning(
                    f'拒绝权限 | 用户: {current_user} | 所需权限： {permission}'
                    f'当前权限： {user_permissions}'
                )
                return jsonify({
                    'code': 403,
                    'msg': f'权限不足'
                }), 403

            return fn(*args, **kwargs)
        return wrapped
    return decorator

def role_required(role_name):
    def decorator(fn):
        @wraps(fn)
        def warpper(*args, **kwargs):
            verify_jwt_in_request()
            claims = get_jwt()
            current_role = claims.get('role')

            if current_role != role_name:
                current_user = claims.get('sub')
                current_app.logger.warning(
                    f'拒绝权限 | 用户： {current_user} | 所需权限： {role_name}'
                    f'当前角色： {current_role}'
                )
                return jsonify({
                    'code': 403,
                    'msg': '权限不足'
                })
            return fn(*args, **kwargs)
        return warpper
    return decorator


