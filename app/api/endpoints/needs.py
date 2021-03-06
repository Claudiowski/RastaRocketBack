# -*- coding: utf-8 -*-

import os
from datetime import datetime

from flask import request, g, current_app, send_from_directory
from flask_httpauth import HTTPTokenAuth
from flask_restplus import Namespace, Resource, abort
from flask.ext.mail import Message

from app.elastic import get_user_from_id, get_need_from_id, delete_need_from_id, get_needs, get_customer_from_id, \
    get_contact_from_id, get_consultant_from_id, add_need_from_parameters, update_need, add_need_content, \
    get_need_content_from_id, delete_need_content_from_id

from app.models import User
from app.utils import allowed_file
from ..parsers import need_parser, upload_parser
from ..serializers.needs import need_post, need_put, need_minimal, need_data_container, need_content, need_complete

ns = Namespace('needs', description='Needs related operations')

# ================================================================================================
# AUTH
# ================================================================================================
#
#   Auth verification
#
# ================================================================================================

auth = HTTPTokenAuth(scheme='Token')


@auth.verify_token
def verify_token(token):
    """
    Verify auth token

    :param token: User token
    :type token: str

    :return: True if valid token, else False
    :rtype: bool
    """
    user_id = User.verify_auth_token(token)

    if user_id is None:
        return False

    else:
        user = get_user_from_id(user_id)

        if not user:
            return False

        g.user = user
        return True


# ================================================================================================
# ENDPOINTS
# ================================================================================================
#
#   API needs endpoints
#
# ================================================================================================

@ns.route('/')
class NeedCollection(Resource):
    decorators = [auth.login_required]

    @ns.marshal_with(need_data_container)
    @ns.expect(need_parser)
    def get(self):
        """
        Return need collection
        """

        args = need_parser.parse_args()
        size = args.get('size') if args.get('size') else 20
        start = args.get('page') * size if args.get('page') else 0

        title = args.get('title')
        status = args.get('status')
        customer_id = args.get('customer')

        needs = get_needs(start, size, g.user.id, title, status, customer_id)

        for need in needs:
            need.customer_obj = get_customer_from_id(need.customer)
            need.contact_obj = get_contact_from_id(need.contact)

        return {'needs': needs}

    @ns.marshal_with(need_minimal, code=201, description='Need successfully created.')
    @ns.doc(responses={
        400: 'Validation error'
    })
    @ns.expect(need_post)
    def post(self):
        """
        Add need
        """

        data = request.json

        if not data.get('created_at'):
            data['created_at'] = datetime.now().strftime('%Y-%m-%dT%H:%M:%S')

        if not get_customer_from_id(data.get('customer')):
            abort(400, error='Customer not found')

        if not get_contact_from_id(data.get('contact')):
            abort(400, error='Contact not found')

        if data.get('consultants'):
            for consultant in data.get('consultants'):
                if not get_consultant_from_id(consultant):
                    abort(400, error='Consultant not found')

        if data.get('status') not in ['open', 'win', 'lost']:
            abort(400, error='Invalid status choice')

        data['author'] = g.user.id

        need = add_need_from_parameters(data)
        need.customer_obj = get_customer_from_id(need.customer)
        need.contact_obj = get_contact_from_id(need.contact)

        if not need:
            abort(400, error='Error during save need')

        else:

            msg = Message('Need need added',
                          recipients=["a.verdier@outlook.fr"])

            msg.body = 'Need need added, see {0}'.format(need.id)

            return need, 201


@ns.route('/<need_id>')
@ns.response(404, 'Need not found')
class NeedItem(Resource):
    decorators = [auth.login_required]

    @ns.marshal_with(need_complete)
    def get(self, need_id):
        """
        Get need
        """

        need = get_need_from_id(need_id)
        if not need or need.author != g.user.id:
            abort(404)

        need.customer_obj = get_customer_from_id(need.customer)
        need.contact_obj = get_contact_from_id(need.contact)

        need.consultants_obj = []
        for consultant in need.consultants:
            need.consultants_obj.append(get_consultant_from_id(consultant))

        return need

    @ns.response(204, 'Need successfully updated.')
    @ns.doc(responses={
        409: 'Value exist',
        400: 'Validation error'
    })
    @ns.expect(need_put)
    def put(self, need_id):
        """
        Update need
        """

        need = get_need_from_id(need_id)
        if not need or need.author != g.user.id:
            abort(404)

        data = request.json

        consultants = data.get('consultants')
        if consultants and len(consultants) > 0:
            for consultant in consultants:
                if not get_consultant_from_id(consultant):
                    abort(400, error='Consultant not found')

        if data.get('status') and data.get('status') not in ['open', 'win', 'lost']:
            abort(400, error='Invalid status choice')

        if update_need(need_id, data):
            return 'Need successfully updated.', 204
        else:
            abort(400, error='Unable to update need.')

    @ns.response(204, 'Need successfully deleted.')
    def delete(self, need_id):
        """
        Delete need
        """

        need = get_need_from_id(need_id)
        if not need or need.author != g.user.id:
            abort(404)

        if delete_need_from_id(need_id):
            return 'Need successfully deleted.', 204

        else:
            abort(400, error='Unable to deleted need #{0}'.format(need_id))


@ns.route('/<need_id>/contents')
@ns.response(404, 'Need not found')
class NeedContentCollection(Resource):
    decorators = [auth.login_required]

    @ns.marshal_with(need_content, code=201, description='Content successfully uploaded.')
    @ns.doc(responses={
        400: 'Validation error'
    })
    @ns.expect(upload_parser)
    def post(self, need_id):
        """
        Upload need content
        """

        need = get_need_from_id(need_id)
        if not need or need.author != g.user.id:
            abort(404)

        args = upload_parser.parse_args()
        file = args['file']

        if not allowed_file(current_app.config['ALLOWED_EXTENSIONS'], file.filename):
            abort(400, error='File not allowed')

        path = os.path.join(current_app.config['UPLOAD_FOLDER'], file.filename)

        if os.path.exists(path):
            abort(400, error='File {0} already exist'.format(file.filename))

        file.save(os.path.join(current_app.config['UPLOAD_FOLDER'], file.filename))

        content = add_need_content(need.id, file.filename)

        if content:
            return content, 201

        else:
            os.remove(path)
            abort(400, error='Unable to save content')


@ns.route('/<need_id>/contents/<content_id>')
@ns.response(404, 'Need content not found')
class NeedContentItem(Resource):
    decorators = [auth.login_required]

    @ns.doc(responses={
        200: 'Success',
        400: 'Need have no content'
    })
    def get(self, need_id, content_id):
        """
        Return need content
        """

        need = get_need_from_id(need_id)
        if not need or need.author != g.user.id:
            abort(404)

        content = get_need_content_from_id(content_id)
        if not content or content.need != need.id:
            abort(404)

        path = os.path.join(current_app.config['UPLOAD_FOLDER'], content.filename)

        if not os.path.exists(path) or not os.path.isfile(path):
            delete_need_content_from_id(content.id)
            abort(400, error='Need have no content')

        return send_from_directory(current_app.config['UPLOAD_FOLDER'], content.filename)

    @ns.response(204, 'Need content successfully deleted')
    def delete(self, need_id, content_id):
        """
        Delete need content
        """

        need = get_need_from_id(need_id)
        if not need or need.author != g.user.id:
            abort(404)

        content = get_need_content_from_id(content_id)
        if not content or content.need != need.id:
            abort(404)

        path = os.path.join(current_app.config['UPLOAD_FOLDER'], content.filename)

        if os.path.exists(path):
            os.remove(path)

        delete_need_content_from_id(content.id)

        return 'Need content successfully deleted', 201
