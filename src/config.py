# -*- coding: utf-8 -*-
import os

basedir = os.path.abspath(os.path.dirname(__file__))


class Config(object):
    SRC_ROOT = os.path.dirname(os.path.abspath(__file__))  # application_top
    APP_ROOT = os.path.join(SRC_ROOT, 'app')
    APP_STATIC = os.path.join(APP_ROOT, 'static')
    LOG_ROOT = os.environ.get('LOG_ROOT') or os.path.join(SRC_ROOT, 'log')
    UPLOADS_ROOT = os.environ.get('UPLOADS_ROOT') or os.path.join(SRC_ROOT, 'uploads')
    DOCS_ROOT = os.environ.get('DOCS_ROOT') or os.path.join(SRC_ROOT, 'docs')

    SECRET_KEY = os.environ.get('SECRET_KEY', 'CHANGETHISSTRING')
    SQLALCHEMY_TRACK_MODIFICATIONS = True
    DEBUG_TB_ENABLED = os.environ.get('DEBUG_TB_ENABLED', False)
    DEBUG_TB_INTERCEPT_REDIRECTS = False
    JSONIFY_PRETTYPRINT_REGULAR = False
    ITEMS_PER_PAGE = 10

    # Babel config
    # LANGUAGES = {'en': 'English', 'es': 'Español'}

    # Celery config
    CELERY_BROKER_URL = 'redis://localhost:6379/0'
    CELERY_RESULT_BACKEND = 'redis://localhost:6379/0'

    # Flask-Mail config
    #MAIL_SERVER = 'smtp.x.com'
    #MAIL_PORT = 587
    #MAIL_USE_TLS = True
    # MAIL_USE_SSL = False
    #MAIL_DEBUG = 0  # app.debug
    #MAIL_USERNAME = 'support@imatec.cl'
    #MAIL_PASSWORD = '1m4t3c'

    # MAIL_DEFAULT_SENDER = None
    # MAIL_MAX_EMAILS = None
    # MAIL_SUPPRESS_SEND = app.testing
    # MAIL_ASCII_ATTACHMENTS = False

    # Mercado Público
    # get ticket from http://api.mercadopublico.cl/modules/Participa.aspx
    MP_TICKET = os.environ.get('MP_TICKET', 'F8537A18-6766-4DEF-9E59-426B4FEE2844')
    MP_ENDPOINT_ORDENESDECOMPRA = "http://api.mercadopublico.cl/servicios/v1/Publico/ordene sdecompra.json"
    MP_ENDPOINT_LICITACIONES = "http://api.mercadopublico.cl/servicios/v1/Publico/licitaciones.json"
    MP_ENDPOINT_PROVEEDOR = "http://api.mercadopublico.cl/servicios/v1/Publico/Empresas/BuscarProveedor"
    MP_ENDPOINT_COMPRADOR = "http://api.mercadopublico.cl/servicios/v1/Publico/Empresas/BuscarComprador"

    @staticmethod
    def init_app(app):
        pass


class DevelopmentConfig(Config):
    DEBUG = os.environ.get('DEBUG') or True
    TESTING = os.environ.get('TESTING') or False
    DEBUG_TB_ENABLED = os.environ.get('DEBUG_TB_ENABLED', False)
    SQLALCHEMY_DATABASE_URI = os.environ.get('DEV_DATABASE_URL') or \
                              'sqlite:///' + os.path.join(basedir, 'data-dev.sqlite')


class TestingConfig(Config):
    DEBUG = os.environ.get('DEBUG') or False
    TESTING = os.environ.get('TESTING') or True
    DEBUG_TB_ENABLED = os.environ.get('DEBUG_TB_ENABLED', False)
    SQLALCHEMY_DATABASE_URI = os.environ.get('TEST_DATABASE_URL') or \
                              'sqlite:///' + os.path.join(basedir, 'data-test.sqlite')


class ProductionConfig(Config):
    DEBUG = os.environ.get('DEBUG') or False
    TESTING = os.environ.get('DEBUG') or False
    DEBUG_TB_ENABLED = os.environ.get('DEBUG_TB_ENABLED', False)
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
                              'sqlite:///' + os.path.join(basedir, 'data.sqlite')


config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig,
    'default': ProductionConfig
}
