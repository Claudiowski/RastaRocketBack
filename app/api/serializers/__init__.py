from flask_restplus import fields
from app.api import api


auth_token = api.model('Auth Token', {
    'token': fields.String(required=True, description='Auth token')
})