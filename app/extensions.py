from flask_jwt_extended import JWTManager, jwt_required, create_access_token
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from celery import Celery

jwt = JWTManager()

db = SQLAlchemy()
migrate = Migrate()

celery = Celery()



