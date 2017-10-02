from flask_restplus import fields
from app.api import api


need_minimal = api.model('Need Minimal', {
    'name': fields.String(required=True, description='Need name', min_length=3, max_length=64)
})

need_data_container = api.model('Need DataContainer', {
    'needs': fields.List(fields.Nested(need_minimal))
})