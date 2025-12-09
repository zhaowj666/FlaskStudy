from flask import jsonify, request, g, current_app
from werkzeug.exceptions import HTTPException
import traceback
from datetime import datetime,timezone
from app.utils.logger import save_log_to_db


def register_exception_handler(app):
    # 注册全局错误处理器到Flask 应用
    # 此函数应在应用工厂中，于蓝图注册之后被调用

    @app.errorhandler(HTTPException)
    def handler_http_exception(e):
        #处理werkzeug HTTP异常，如404,405
        #记录警告级别日志
        current_app.logger.warning(
            f"HTTPException: {e.description} | "
            f"Path: {request.path} | "
            f"Method: {request.method}"
        )

        error_log = {
            'level': 'ERROR',
            'request_id': g.get('request_id', 'pre-request'),
            'message': f'ErrorType: HTTPException Code: {e.code}  Message: {e.description}',
            'created_at': datetime.now(timezone.utc)
        }
        save_log_to_db(error_log)

        response = jsonify({
            'code': e.code,
            'name': e.name,
            'description': e.description,
            'request_id': g.get('request_id', '')
        })
        response.status_code = e.code
        return response

    @app.errorhandler(Exception)
    def handler_general_exception(e):
        #处理所有其他未被捕获的通用异常（即500内部服务器错误）。
        current_app.logger.error(
            f"Unhandled Exception: {str(e)} | "
            f"Path: request.path {request.path} | "
            f"Method: {request.method}"
            f"request_id: {g.get('request_id', '')} \n"
            f"{traceback.format_exc()}"
        )

        if current_app.debug:
            description = f"{type(e).__name__}: {str(e)}"
        else:
            description = "An internal server error occurred."

        error_log = {
            'level': 'ERROR',
            'request_id': g.get('request_id', 'pre-request'),
            'message': f'ErrorType: Exception Code: {e.code}  Message: {description}',
            'created_at': datetime.now(timezone.utc)
        }
        save_log_to_db(error_log)

        response = jsonify({
            'code': 500,
            'name': "Internal Server Error",
            'description': description,
            'request_id': g.get('request_id', '')
        })
        response.status_code = 500
        return response


