import logging
from flask import g, has_request_context

class RequestIdFilter(logging.Filter):
    # 创建自定义日志过滤器
    # 如果当前处于一个有效的http请求上下文中，自动为每一条日志添加 request_id字段
    def filter(self, record):
        # 检查是否有活跃的请求上下文， 避免在非请求场景，如启动时、CLI命令中报错
        if has_request_context():
            record.request_id = g.get('request_id', 'no-request-id')
        else:
            record.request_id = 'no-context'
        return True


def init_logging(app):

    #创建我们想要的日志格式
    #%(request_id)s 将由我们上面定义的过滤器动态提供
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - [%(request_id)s] - %(message)s'
    )

    #创建日志处理器，例如输出到控制台
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.DEBUG if app.debug else logging.INFO)
    console_handler.setFormatter(formatter)

    #将创建的自定义过滤器添加到处理器
    console_handler.addFilter(RequestIdFilter())

    #将处理器添加到Flask应用日志器
    app.logger.addHandler(console_handler)
    app.logger.setLevel(logging.DEBUG)

    #避免日志传播到更高级别的根日志器，防止重复打印
    app.logger.propagate = False



