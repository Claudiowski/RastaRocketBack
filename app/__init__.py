from elasticsearch import Elasticsearch
from flask import Flask
from config import config

els_client = None


def create_app(config_name='default'):
    """
    Create Flask app

    :param config_name:
    :return: Flask
    """
    from .api import blueprint as api_blueprint

    app = Flask(__name__)
    app.config.from_object(config[config_name])
    config[config_name].init_app(app)
    app.els_client = Elasticsearch([{'host': config[config_name].ELS_HOST, 'port': config[config_name].ELS_PORT}])

    app.register_blueprint(api_blueprint)

    extensions(app)

    return app


def extensions(app):
    """
    Init extensions

    :param app: Flask app
    """
    pass