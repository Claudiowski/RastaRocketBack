from flask_restplus import fields
from app.api import api


customer_minimal = api.model('Customer Minimal', {
    'name': fields.String(required=True, description='Customer name', min_length=3, max_length=64),
})

customer_data_container = api.model('Customer DataContainer', {
    'customers': fields.List(fields.Nested(customer_minimal))
})