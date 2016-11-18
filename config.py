import os
envs = os.environ


class Config(object):
    DEBUG = False  # should debug mode be on?
    TESTING = False  # are unit tests running?
    SQLALCHEMY_DATABASE_URI = envs.get('SQLALCHEMY_DATABASE_URI')
    DB_KEY = envs.get('DB_KEY')
    CONSTR = envs.get('TEST_CONSTR')
    SQLALCHEMY_DATABASE_URI = CONSTR % DB_KEY

class ProductionConfig(Config):
    SQLALCHEMY_DATABASE_URI = envs.get('SQLALCHEMY_DATABASE_URI')
    CONSTR = envs.get('PROD_CONSTR')


class DevelopmentConfig(Config):
    DEBUG = True
    TESTING = False


class TestingConfig(Config):
    TESTING = True
