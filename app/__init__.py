# -*- coding: utf-8 -*-

from elasticsearch import Elasticsearch
from flask import Flask, request
from flask_cors import CORS
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
    CORS(app, resources={r"/api/*": {"origins": "*"}})

    app.config.from_object(config[config_name])
    config[config_name].init_app(app)
    app.els_client = Elasticsearch([{'host': config[config_name].ELS_HOST, 'port': config[config_name].ELS_PORT}])

    app.register_blueprint(api_blueprint)

    extensions(app)

    @app.after_request
    def after_request(response):
        response.headers.add('Access-Control-Allow-Origin', '*')
        if request.method == 'OPTIONS':
            response.headers['Access-Control-Allow-Methods'] = 'DELETE, GET, POST, PUT'
            headers = request.headers.get('Access-Control-Request-Headers')
            if headers:
                response.headers['Access-Control-Allow-Headers'] = headers
        return response

    return app


def extensions(app):
    """
    Init extensions

    :param app: Flask app
    """
    pass