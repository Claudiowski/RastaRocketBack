from datetime import datetime

from flask import request, g
from flask_httpauth import HTTPTokenAuth
from flask_restplus import Namespace, Resource, abort

from app.elastic import get_user_from_id, get_need_from_id, delete_need_from_id, get_needs, get_customer_from_id, \
    get_contact_from_id, get_consultant_from_id, add_need_from_parameters, update_need

from app.models import User
from ..parsers import need_parser
from ..serializers.needs import need_post, need_put, need_minimal, need_data_container

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

        for consultant in data.get('consultants'):
            if not get_consultant_from_id(consultant):
                abort(400, error='Consultant not found')

        if data.get('status') not in ['open', 'win', 'lost']:
            abort(400, error='Invalid status choice')

        data['author'] = g.user.id

        need = add_need_from_parameters(data)

        if not need:
            abort(400, error='Error during save need')

        else:
            return need, 201


@ns.route('/<need_id>')
@ns.response(404, 'Need not found')
class NeedItem(Resource):
    decorators = [auth.login_required]

    @ns.marshal_with(need_minimal)
    def get(self, need_id):
        """
        Get need
        """

        need = get_need_from_id(need_id)
        if not need or need.author != g.user.id:
            abort(404)

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
