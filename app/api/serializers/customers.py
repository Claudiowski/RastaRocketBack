# -*- coding: utf-8 -*-

from flask_restplus import fields
from app.api import api


customer_minimal = api.model('Customer Minimal', {
    'id': fields.String(required=True, description='Customer unique ID'),
    'name': fields.String(required=True, description='Customer name', min_length=3, max_length=64),
})

contact_minimal = api.model('Contact Minimal', {
    'id': fields.String(required=True, description='Contact unique ID'),
    'name': fields.String(required=True, description='Contact name', min_length=3, max_length=64)
})

customer_data_container = api.model('Customer DataContainer', {
    'customers': fields.List(fields.Nested(customer_minimal))
})

contact_data_container = api.model('Contact DataContainer', {
    'contacts': fields.List(fields.Nested(contact_minimal))
})