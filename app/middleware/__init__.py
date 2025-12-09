from .request_id import init_request_id_middleware
from .logging import init_logging

def register_middleware(app):
    init_request_id_middleware(app)
    init_logging(app)
