import os
_basedir = os.path.abspath(os.path.dirname(__file__))
envs = os.environ


class Config(object):
    DEBUG = False  # should debug mode be on?
    TESTING = False  # are unit tests running?
    SQLALCHEMY_DATABASE_URI = envs.get('SQLALCHEMY_DATABASE_URI') + os.path.join(_basedir, 'test.db')
    DB_KEY = envs.get('DB_KEY')
    CONSTR = envs.get('TEST_CONSTR')
    # SQLALCHEMY_DATABASE_URI = CONSTR % DB_KEY
    SQLALCHEMY_MIGRATE_REPO = os.path.join(_basedir, 'db_repository')
    SECRET_KEY = envs.get('SECRET_KEY')
    API_URL = envs.get('API_URL')
    API_USERNAME = envs.get('API_USERNAME')
    API_PASSWORD = envs.get('API_PASSWORD')


class ProductionConfig(Config):
    SQLALCHEMY_DATABASE_URI = envs.get('SQLALCHEMY_DATABASE_URI')
    CONSTR = envs.get('PROD_CONSTR')

class DevelopmentConfig(Config):
    DEBUG = True
    TESTING = False
    TEST_USERNAME = envs.get('TEST_USERNAME')

class TestingConfig(Config):
    TESTING = True
