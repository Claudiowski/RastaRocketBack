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

blueprint = Blueprint('api', __name__, url_prefix='/api')
api = Api(blueprint,
          title='RastaRocket GFI API',
          version='0.1',
          description='API for EPSI Workshop',
          authorizations=authorizations,
          security='tokenKey'
          )

from .endpoints.token import ns as token_namespace
from .endpoints.needs import ns as needs_namespace
from .endpoints.customers import ns as customers_namespace
from .endpoints.contacts import ns as contacts_namespace
from .endpoints.consultants import ns as consultants_namespace

api.add_namespace(token_namespace)
api.add_namespace(needs_namespace)
api.add_namespace(customers_namespace)
api.add_namespace(contacts_namespace)
api.add_namespace(consultants_namespace)