from flask import request, g, abort
from flask_restplus import Namespace, Resource
from flask_httpauth import HTTPTokenAuth
from app.elastic import get_user_from_id, get_possible_contacts
from app.models import User
from ..serializers.customers import contact_data_container
from ..parsers import contact_autocomplete_parser


ns = Namespace('contacts', description='Contacts related operations')

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
#   API contacts endpoints
#
# ================================================================================================

@ns.route('/')
class ContactsAutocomplete(Resource):
    decorators = [auth.login_required]

    @ns.marshal_with(contact_data_container)
    @ns.expect(contact_autocomplete_parser)
    def get(self):
        """
        Contacts autocomplete
        """

        args = contact_autocomplete_parser.parse_args()

        name_prefix = args.get('name')
        customer_id = args.get('customer_id')

        if name_prefix is not None and name_prefix != '':
            possible_contacts = get_possible_contacts(name_prefix, customer_id)

            return {'contacts': possible_contacts}

        else:
            abort('400', error="name can't be empty")
