from flask import Blueprint
from flask_restplus import Api


blueprint = Blueprint('api', __name__, url_prefix='/api')
api = Api(blueprint,
          title='RastaRocket GFI API',
          version='0.1',
          description='API for EPSI Workshop'
)


from .endpoints.needs import ns as need_namespace

api.add_namespace(need_namespace)