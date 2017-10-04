# -*- coding: utf-8 -*-

from flask import Blueprint
from flask_restplus import Api


authorizations = {
    'tokenKey': {
        'type': 'apiKey',
        'in': 'header',
        'name': 'Authorization'
    },
    'basicAuth': {
        'type': 'basic',
        'in': 'header'
    }
}

blueprint = Blueprint('private', __name__, url_prefix='/private')
api = Api(blueprint,
          title='RastaRocket GFI Private API',
          version='0.1',
          description='Private API for EPSI Workshop',
          authorizations=authorizations,
          security='tokenKey'
          )