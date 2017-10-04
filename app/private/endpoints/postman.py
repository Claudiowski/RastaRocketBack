# -*- coding: utf-8 -*-

from flask import json, g
from flask_httpauth import HTTPTokenAuth
from flask_restplus import Resource
from app.elastic import get_user_from_id
from app.models import User
from app.private import api

ns = api.namespace('postman', description='Postman export.')


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
#   API postman endpoint
#
# ================================================================================================

@ns.route('/')
class PostmanExport(Resource):
    decorators = [auth.login_required]

    def get(self) -> object:
        """
        Get postman dump
        """

        urlvars = False  # Build query strings in URLs
        swagger = True  # Export Swagger specifications
        data = api.as_postman(urlvars=urlvars, swagger=swagger)

        return json.dumps(data)
