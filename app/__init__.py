from flask import Flask
from config import config


def create_app(config_name='default'):
    """
    Create Flask app

    :param config_name:
    :return:
    """
    from .api import blueprint as api_blueprint

    app = Flask(__name__)
    app.config.from_object(config[config_name])
    config[config_name].init_app(app)

    app.register_blueprint(api_blueprint)

    extensions(app)

    return app


def extensions(app):
    """
    Init extensions

    :param app:
    :return:
    """
    pass