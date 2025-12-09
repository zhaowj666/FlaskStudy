import uuid
from flask import request, g


# Flask的应用级请求钩子
def init_request_id_middleware(app):
    """注册request_id相关的请求钩子"""

    @app.before_request
    def generate_request_id():
        request_id = request.headers.get('X-Request-ID')
        if not request_id:
            request_id = str(uuid.uuid4())      # 生成新的UUID

        g.request_id = request_id               # 存入全局上下文


    @app.after_request
    def inject_request_id_header(response):
        response.headers['X-Request-ID'] = g.get('request_id', '')                  # 从g中取出并放入响应头
        return response