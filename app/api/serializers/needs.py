# -*- coding: utf-8 -*-

from flask_restplus import fields
from app.api import api
from .customers import customer_minimal, contact_minimal
from .consultants import consultant_minimal


need_minimal = api.model('Need Minimal', {
    'id': fields.String(required=True, description='Need unique ID'),
    'created_at': fields.DateTime(dt_format='iso8601', required=False, description='Need creation datetime'),
    'customer': fields.String(required=True, description='Customer unique name', min_length=3, max_length=64),
    'customer_obj': fields.Nested(customer_minimal, required=True, description='Customer Object'),
    'contact': fields.String(required=True, description='Customer contact name', min_length=3, max_length=64),
    'contact_obj': fields.Nested(contact_minimal, required=True, description='Customer Object'),
    'title': fields.String(required=True, description='Need title', min_length=3, max_length=64),
    'start_at_latest': fields.String(required=False, dt_format='iso8601', description='Need start at latest date'),
    'status': fields.String(required=True, description='Need status (open, win, lost)')
})

need_post = api.model('Need POST', {
    'created_at': fields.DateTime(dt_format='iso8601', required=False, description='Need creation datetime (iso8601)'),
    'customer': fields.String(required=True, description='Customer unique ID', min_length=3, max_length=64),
    'contact': fields.String(required=True, description='Customer contact ID', min_length=3, max_length=64),
    'title': fields.String(required=True, description='Need title', min_length=3, max_length=64),
    'description': fields.String(required=True, description='Need description'),
    'success_keys': fields.List(fields.String(description='Key of success', min_length=3),
                                description='Keys of need success', max_items=3),
    'start_at_latest': fields.DateTime(dt_format='iso8601', required=False, description='Start at latest datetime'),
    'month_duration': fields.Float(required=False, description='Month duration', min=0),
    'week_frequency': fields.Float(required=False, description='Week frequency', min=0),
    'rate': fields.Float(required=False, description='HT price', min=0),
    'consultants': fields.List(fields.String(description='Consultant ids', min_length=3, max_length=64),
                               description='Consultants unique ID', max_items=5),
    'status': fields.String(required=True, description='Need status (Open, Win, Lost)', min_length=3, max_length=64)
})

need_complete = api.inherit('Need complete', need_minimal, {
    'month_duration': fields.Float(required=False, description='Month duration', min=0),
    'week_frequency': fields.Float(required=False, description='Week frequency', min=0),
    'rate': fields.Float(required=False, description='HT price', min=0),
    'consultants': fields.List(fields.String(description='Consultant ids'),
                               description='Consultants unique ID', max_items=5),
    'consultants_obj': fields.List(fields.Nested(consultant_minimal), description='Consultants objects'),
    'description': fields.String(required=True, description='Need description'),
    'success_keys': fields.List(fields.String(description='Key of success'), description='Keys of need success', max_items=3)
})

need_put = api.model('Need PUT', {
    'title': fields.String(required=False, description='Need title', min_length=3, max_length=64),
    'description': fields.String(required=False, description='Need description'),
    'success_keys': fields.List(fields.String(description='Key of success', min_length=3),
                                description='Keys of need success', max_items=3),
    'start_at_latest': fields.DateTime(dt_format='iso8601', required=False, description='Start at latest datetime'),
    'month_duration': fields.Float(required=False, description='Month duration', min=0),
    'week_frequency': fields.Float(required=False, description='Week frequency', min=0),
    'rate': fields.Float(required=False, description='HT price', min=0),
    'consultants': fields.List(fields.String(description='Consultant name', min_length=3, max_length=64),
                               description='Consultants unique ID', max_items=5),
    'status': fields.String(required=False, description='Need status (Open, Win, Lost)', min_length=3, max_length=64)
})

need_content = api.model('Need Content', {
    'id': fields.String(required=True, description='Content unique ID'),
    'need': fields.String(reequired=True, description='Need unique ID'),
    'filename': fields.String(required=True, description='Content filename')
})

need_data_container = api.model('Need DataContainer', {
    'needs': fields.List(fields.Nested(need_minimal))
})
