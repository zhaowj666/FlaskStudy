from flask import g, request, jsonify, Blueprint, current_app
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.tasks.example_tasks import long_running_task

task_bp = Blueprint('task', __name__, url_prefix='/task')

@task_bp.route('/long_task', methods=['POST'])
@jwt_required()
def start_long_task():
    current_user_id = get_jwt_identity()
    request_id = g.get('request_id', 'no-request-id')
    current_app.logger.info('start long task with user id %s', current_user_id)

    task = long_running_task.delay(
        user_id = current_user_id,
        request_id_from_web = request_id
    )

    return jsonify({
        'msg': '后台任务已完成',
        'task_id': task.id,
        'request_id': request_id
    }), 202



