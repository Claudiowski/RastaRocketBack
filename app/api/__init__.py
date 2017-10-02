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

from .endpoints.needs import ns as need_namespace
from .endpoints.token import ns as token_namespace

api.add_namespace(need_namespace)
api.add_namespace(token_namespace)
