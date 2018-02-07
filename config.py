import os
import random, string

basedir = os.path.abspath(os.path.dirname(__file__))


class Config:
    # To Be Deprecated
    SQLALCHEMY_TRACK_MODIFICATIONS = True

    SECRET_KEY = \
        os.environ.get('SECRET_KEY') or \
        ''.join(random.choice(string.ascii_uppercase +
                              string.digits) for x in range(32))
    SQLALCHEMY_COMMIT_ON_TEARDOWN = True

    @staticmethod
    def init_app(app):
        pass


class DevelopmentConfig(Config):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = \
        os.environ.get('DEV_DATABASE_URL') or 'sqlite:///' + os.path.join(
            basedir, 'item-app-dev.sqlite')


class TestingConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = \
        os.environ.get('TEST_DATABASE_URL') or \
        'sqlite:///' + os.path.join(basedir, 'item-app-test.sqlite')


class ProductionConfig(Config):
    db_url = os.environ.get('DATABASE_URL') or 'catalog?host=/var/run/postgresql'
    db_user = os.environ.get('DATABASE_USER') or 'catalog'
    db_password = os.environ.get('DATABASE_PASSWORD') or 'catalog'
    SQLALCHEMY_DATABASE_URI =\
        'postgresql+psycopg2://catalog:mysecretpassword@localhost/catalog'

    @classmethod
    def init_app(cls, app):
        # log to syslog
        import logging
        from logging.handlers import SysLogHandler
        syslog_handler = SysLogHandler()
        syslog_handler.setLevel(logging.WARNING)
        app.logger.addHandler(syslog_handler)




config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig,

    'default': DevelopmentConfig
}
