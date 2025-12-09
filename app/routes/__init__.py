from flask import Blueprint, jsonify, current_app
from .auth import auth_bp
from .task import task_bp
from .admin import admin_bp

main_bp = Blueprint('main', __name__)

@main_bp.route('/')
def index():
    return 'Hello World!'

@main_bp.route('/hello')
def hello():
    current_app.logger.info('Hello World!')
    return jsonify({'msg': 'Hello World!'})



# 路由注册函数
def register_blueprints(app):
    app.register_blueprint(main_bp)
    app.register_blueprint(auth_bp)
    app.register_blueprint(task_bp)
    app.register_blueprint(admin_bp)