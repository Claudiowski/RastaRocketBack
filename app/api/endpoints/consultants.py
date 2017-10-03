# -*- coding: utf-8 -*-

from flask import request, g
from flask_restplus import Namespace, Resource, abort
from flask_httpauth import HTTPTokenAuth
from app.elastic import get_user_from_id, get_possible_consultants
from app.models import User
from ..serializers.consultants import consultant_data_container
from ..parsers import name_autocomplete_parser


ns = Namespace('consultants', description='Consultants related operations')

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
#   API consultants endpoints
#
# ================================================================================================

@ns.route('/')
class ConsultantsAutocomplete(Resource):
    decorators = [auth.login_required]

    @ns.marshal_with(consultant_data_container)
    @ns.expect(name_autocomplete_parser)
    def get(self):
        """
        Consultants autocomplete
        """

        args = name_autocomplete_parser.parse_args()

        name_prefix = args.get('name')

        if name_prefix is not None and name_prefix != '':
            possible_contacts = get_possible_consultants(name_prefix)

            return {'consultants': possible_contacts}

        else:
            abort('400', error="name can't be empty")
