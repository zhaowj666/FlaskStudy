from flask import Blueprint, request, jsonify, g
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.models import Permissions
from app.utils.auth import authenticate_user, create_tokens, permission_required, role_required
from app.utils.logger import save_log_to_db
from datetime import datetime, timezone


auth_bp = Blueprint('auth', __name__, url_prefix='/auth')

@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')

    user = authenticate_user(username, password)
    if not user:
        return jsonify({'msg': '用户名或密码错误'}), 401

    access_token, refresh_token = create_tokens(user)

    log = {
        'level': 'INFO',
        'request_id': g.request_id or 'pre-request',
        'message': f'用户登录： 用户名： {username}',
        'created_at': datetime.now(timezone.utc)
    }
    save_log_to_db(log)

    return jsonify({
        'msg': 'success',
        'access_token': access_token,
        'refresh_token': refresh_token,
        'username': user.username
    }), 200

@auth_bp.route('/order', methods=['GET'])
@jwt_required()
def order():
    current_user = get_jwt_identity()
    return jsonify({
        'msg': 'success',
        'username': current_user,
    }), 200

@auth_bp.route('/admin/dashboard', methods=['GET'])
@jwt_required()
@role_required('admin')
def admin_dashboard():
    return jsonify({
        'msg': '欢迎访问管理员仪表面板',
        'data': '敏感数据'
    }), 200

@auth_bp.route('/user/profile', methods=['GET'])
@jwt_required()
@permission_required(Permissions.USER_READ)
def user_profile():
    current_user = get_jwt_identity()
    return jsonify({
        'msg': f'你的个人资料',
        'username': current_user,
    })

@auth_bp.route('/user/profile', methods=['PUT'])
@jwt_required()
@permission_required(Permissions.USER_WRITE)
def update_user_profile():
    return jsonify({
        'msg': '修改个人资料成功'
    }), 200