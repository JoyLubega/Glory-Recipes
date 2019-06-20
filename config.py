import os


class MainConfiguration(object):
    DEBUG = False
    WTF_CSRF_ENABLED = True
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = "Thi-is-a-secret-key-pliz-change-it"


class TestingEnvironment(MainConfiguration):
    DEBUG = True
    TESTING = True
    SQLALCHEMY_DATABASE_URI = os.getenv('TEST_DATABASE_URL')


class DevelopmentEnvironment(MainConfiguration):
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL')
    DEBUG = True
    TESTING = True


class ProductionEnvironment(MainConfiguration):
    DEBUG = True
    TESTING = False
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL')


application_config = {
    'MainConfig': MainConfiguration,
    'TestingEnv': TestingEnvironment,
    'DevelopmentEnv': DevelopmentEnvironment,
    'ProductionEnv': ProductionEnvironment
}
