from flask import Blueprint, jsonify,current_app
from flask_jwt_extended import jwt_required
from app.utils.auth import permission_required
from app.models import Permissions, Logs

admin_bp = Blueprint('admin', __name__, url_prefix='/admin')

@admin_bp.route('/logs', methods=['GET'])
@jwt_required()
@permission_required(Permissions.ADMIN_READ)
def logs():
    logs_queryset = Logs.query.order_by(Logs.id.desc()).all()
    logs_list = [log.to_dict() for log in logs_queryset]
    return jsonify({'logs': logs_list})
