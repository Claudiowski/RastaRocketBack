from flask import request, g, abort
from flask_restplus import Namespace, Resource
from flask_httpauth import HTTPTokenAuth
from app.elastic import get_user_from_id, get_need_from_id, delete_need_from_id
from app.models import User
from ..serializers.needs import need_post, need_minimal, need_data_container
from ..parsers import need_parser


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

        return {'needs': []}

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
        print(data)

        return {'title': 'test'}, 201


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
        if not need:
            abort(404)

        return need

    @ns.response(204, 'Need successfully updated.')
    @ns.doc(responses={
        409: 'Value exist',
        400: 'Validation error'
    })
    @ns.expect(need_post)
    def put(self, need_id):
        """
        Update need
        """

        need = get_need_from_id(need_id)
        if not need:
            abort(404)

        return 'Need successfully updated.', 204

    @ns.response(204, 'Need successfully deleted.')
    def delete(self, need_id):
        """
        Delete need
        """

        need = get_need_from_id(need_id)
        if not need:
            abort(404)

        if delete_need_from_id(need_id):
            return 'Need successfully deleted.', 204

        else:
            abort(400, error='Unable to deleted need #{0}'.format(need_id))
