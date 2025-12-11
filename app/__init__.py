from flask import Flask, g, request, jsonify
from .config import config      #导入配置
from .extensions import jwt, db, migrate, celery
from .routes import register_blueprints     #导入路由注册
from .middleware import register_middleware
from .utils.errors import register_exception_handler
from .utils.logger import save_log_to_db
from datetime import datetime, timezone, UTC

def create_app(config_name='default'):
    app = Flask(__name__)

    app.config.from_object(config[config_name])

    #初始化扩展
    jwt.init_app(app)
    db.init_app(app)
    migrate.init_app(app, db)

    # 将Flask配置中CELERY字典的配置，更新到Celery实例
    celery.conf.update(app.config['CELERY'])
    # 为Celery设置一个上下文，使其能在Flask应用上下文中运行（访问db等）
    class ContextTask(celery.Task):
        def __call__(self, *args, **kwargs):
            with app.app_context():
                return self.task(*args, **kwargs)
    celery.Task = ContextTask

    #注册所有自定义中间件
    register_middleware(app)

    # 注册蓝图
    register_blueprints(app)

    register_exception_handler(app)

    @app.before_request
    def before_request():
        log = {
            'level': 'INFO',
            'request_id': g.get('request_id', 'pre-request'),
            'message': f'请求开始 Method: {request.method}  Url: {request.url}',
            'created_at': datetime.now(timezone.utc)
        }
        save_log_to_db(log)

    @app.after_request
    def after_request(response):
        log = {
            'level': 'INFO',
            'request_id': g.get('request_id', 'pre-request'),
            'message': f'请求完成 Method: {request.method}  Url: {request.url} - 状态码：{response.status_code}',
            'created_at': datetime.now(timezone.utc)
        }
        save_log_to_db(log)
        return response


    return app