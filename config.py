# -*- coding: utf-8 -*-

import os

basedir = os.path.abspath(os.path.dirname(__file__))


class Config:
    """
    Base configuration
    """
    SECRET_KEY = os.environ.get('RASTAROCKET_SECRET_KEY') or 'djgkkfv44dfdfgd!'
    TOKEN_EXPIRATION_TIME = 600
    RESTPLUS_SWAGGER_UI_DOC_EXPANSION = 'list'
    RESTPLUS_VALIDATE = True
    SMTP_HOST = ''
    SMTP_AUTH = True
    SMTP_USERNAME = ''
    SMTP_PASSWORD = ''
    SMTP_SECURE = 'tls'
    SMTP_PORT = 587
    EMAIL_FROM = ''
    ELS_HOST = 'localhost'
    ELS_PORT = 9200
    UPLOAD_FOLDER = os.path.join(basedir, 'upload')
    ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}

    @staticmethod
    def init_app(app):
        """
        Init app

        :param app: Flask App
        :type app: Flask
        """
        pass


class DevelopmentConfig(Config):
    """
    Development configuration
    """
    DEBUG = True
    RESTPLUS_MASK_SWAGGER = False
    RESTPLUS_ERROR_404_HELP = True


class ProductionConfig(Config):
    """
    Production configuration
    """
    DEBUG = False
    RESTPLUS_MASK_SWAGGER = True
    RESTPLUS_ERROR_404_HELP = False


class UnixDevelopmentConfig(DevelopmentConfig):
    """
    Unix development configuration, logs in syslog
    """

    @classmethod
    def init_app(cls, app):
        DevelopmentConfig.init_app(app)

        import logging
        from logging.handlers import SysLogHandler
        syslog_handler = SysLogHandler()
        syslog_handler.setLevel(logging.DEBUG)
        app.logger.addHandler(syslog_handler)


class UnixProductionConfig(ProductionConfig):
    """
    Unix production configuration, logs in syslog
    """

    @classmethod
    def init_app(cls, app):
        ProductionConfig.init_app(app)

        import logging
        from logging.handlers import SysLogHandler
        syslog_handler = SysLogHandler()
        syslog_handler.setLevel(logging.WARNING)
        app.logger.addHandler(syslog_handler)


config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'development_unix': UnixDevelopmentConfig,
    'production_unix': UnixProductionConfig,
    'default': DevelopmentConfig
}
