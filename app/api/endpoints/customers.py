# -*- coding: utf-8 -*-

from flask import request, g
from flask_restplus import Namespace, Resource, abort
from flask_httpauth import HTTPTokenAuth
from app.elastic import get_user_from_id, get_possible_customers
from app.models import User
from ..serializers.customers import customer_data_container
from ..parsers import customer_autocomplete_parser


ns = Namespace('customers', description='Customers related operations')

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
#   API customers endpoints
#
# ================================================================================================

@ns.route('/')
class CustomerAutocomplete(Resource):
    decorators = [auth.login_required]

    @ns.marshal_with(customer_data_container)
    @ns.expect(customer_autocomplete_parser)
    def get(self):
        """
        Customers autocomplete
        """

        args = customer_autocomplete_parser.parse_args()

        name_prefix = args.get('name')

        if name_prefix is not None and name_prefix != '':
            possible_customers = get_possible_customers(name_prefix)

            return {'customers': possible_customers}

        else:
            abort('400', error="name can't be empty")
