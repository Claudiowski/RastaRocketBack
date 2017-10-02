from flask import g
from flask_restplus import Namespace, Resource
from flask_httpauth import HTTPBasicAuth
from app.elastic import get_user_from_email
from ..serializers import auth_token

ns = Namespace('token', description='Token related operations')

# ================================================================================================
# AUTH
# ================================================================================================
#
#   Auth verification
#
# ================================================================================================

auth = HTTPBasicAuth()


@auth.verify_password
def verify_password(email, password):
    """
    Verify auth token

    :param email: User unique email
    :type email: str

    :param password: User email
    :type password: str

    :return: True if valid credentials, else False
    :rtype: bool
    """

    user = get_user_from_email(email)

    if not user:
        return False

    if not user.verify_password(password):
        return False

    g.user = user
    return True


# ================================================================================================
# ENDPOINTS
# ================================================================================================
#
#   API token endpoints
#
# ================================================================================================


@ns.route('/')
class TokenResource(Resource):
    decorators = [auth.login_required]

    @ns.doc(security='basicAuth')
    @ns.marshal_with(auth_token)
    def get(self):
        """
        Return auth token
        """

        token = g.user.generate_auth_token()

        return {'token': token.decode('ascii')}
