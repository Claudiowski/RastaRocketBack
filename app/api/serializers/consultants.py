# -*- coding: utf-8 -*-

from flask_restplus import fields
from app.api import api


consultant_minimal = api.model('Consultant Minimal', {
    'id': fields.String(required=True, description='Consultant unique ID'),
    'name': fields.String(required=True, description='Consultant name', min_length=3, max_length=64),
})

consultant_data_container = api.model('Consultant DataContainer', {
    'consultants': fields.List(fields.Nested(consultant_minimal))
})
