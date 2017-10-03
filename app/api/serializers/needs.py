from flask_restplus import fields
from app.api import api

need_minimal = api.model('Need Minimal', {
    'created_at': fields.DateTime(dt_format='iso8601', required=False, description='Need creation datetime (iso8601)'),
    'customer': fields.String(required=True, description='Customer unique name', min_length=3, max_length=64),
    'contact_name': fields.String(required=True, description='Customer contact name', min_length=3, max_length=64),
    'title': fields.String(required=True, description='Need title', min_length=3, max_length=64),
})

need_post = api.model('Need POST', {
    'created_at': fields.DateTime(dt_format='iso8601', required=False, description='Need creation datetime (iso8601)'),
    'customer': fields.String(required=True, description='Customer unique ID', min_length=3, max_length=64),
    'contact': fields.String(required=True, description='Customer contact ID', min_length=3, max_length=64),
    'title': fields.String(required=True, description='Need title', min_length=3, max_length=64),
    'description': fields.String(required=True, description='Need description'),
    'success_keys': fields.List(fields.String(description='Key of success', min_length=3, max_length=64),
                                description='Keys of need success', max_items=3),
    'start_at_latest': fields.DateTime(dt_format='iso8601', required=False, description='Start at latest datetime'),
    'month_duration': fields.Float(required=False, description='Month duration', min=0),
    'week_frequency': fields.Float(required=False, description='Week frequency', min=0),
    'rate': fields.Float(required=False, description='HT price', min=0),
    'consultants': fields.List(fields.String(description='Consultant name', min_length=3, max_length=64),
                               description='Consultants unique ID', max_items=5),
    'status': fields.String(required=True, description='Need status (Open, Win, Lost)', min_length=3, max_length=64)

})

need_data_container = api.model('Need DataContainer', {
    'needs': fields.List(fields.Nested(need_minimal))
})
