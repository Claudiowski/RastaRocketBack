# -*- coding: utf-8 -*-

from elasticsearch import Elasticsearch
from flask import Flask, request
from celery import Celery
from flask_cors import CORS
from config import config

els_client = None

CELERY_TASK_LIST = [
    'app.tasks'
]

def create_celery_app(app=None, config_name='development'):
    app = app or create_app(config_name)
    celery = Celery(
        app.import_name,
        broker=app.config['CELERY_BROKER_URL'],
        include=CELERY_TASK_LIST
    )
    celery.conf.update(app.config)
    TaskBase = celery.Task

    class ContextTask(TaskBase):
        abstract = True

        def __call__(self, *args, **kwargs):
            with app.app_context():
                return TaskBase.__call__(self, *args, **kwargs)

    celery.Task = ContextTask
    return celery


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