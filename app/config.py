import os
from dotenv import load_dotenv
from datetime import timedelta

load_dotenv()

class Config:
    # 基础配置，多环境共用
    SECRET_KEY = os.getenv('SECRET_KEY') or 'dev-key-please-change'
    #JWT 配置
    JWT_SECRET_KEY = os.getenv('JWT_SECRET_KEY') or 'dev-key-please-change'
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(minutes=30)
    JWT_REFRESH_TOKEN_EXPIRES = timedelta(days=30)
    JWT_TOKEN_LOCATION = ['headers']
    #数据库配置
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL') or 'sqlite:///data.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_ECHO = True

    # celery 配置
    CELERY = {
        'broker_url': os.getenv('CELERY_BROKER_URL') or 'redis://:xl20210823@localhost:6379/1',
        'result_backend': os.getenv('CELERY_RESULT_BACKEND') or 'redis://:xl20210823@localhost:6379/2',
        'task_serializer': 'json',
        'accept_content': ['json'],
        'result_serializer': 'json',
        'timezone': 'Asia/Shanghai',
        'enable_utc': True
    }



class DevelopmentConfig(Config):
    DEBUG = True


class TestingConfig(Config):
    TESTING = True


class ProductionConfig(Config):
    pass


config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig
}