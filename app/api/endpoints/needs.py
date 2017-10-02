from flask import request, g
from flask_restplus import Namespace, Resource
from flask_httpauth import HTTPTokenAuth
from app.elastic import get_user_from_id
from app.models import User
from ..serializers.needs import need_post, need_minimal


ns = Namespace('need', description='Needs related operations')

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

        return {'name': 'test'}, 201