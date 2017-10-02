from itsdangerous import (TimedJSONWebSignatureSerializer as Serializer, BadSignature, SignatureExpired)
from flask import current_app
from .utils import hash_sha256


class User:
    """
    Represent user,
    used for login
    """

    def __init__(self, els_object):
        """
        Constructor

        :param els_object: Elasticsearch object document
        :type els_object: object
        """
        self._id = els_object.meta.id
        self._email = els_object.Email
        self._password_hash = els_object.PasswordHash

    def hash_password(self, password):
        """
        Set new user passsword

        :param password: New password to hash
        :type password: str
        """
        self._password_hash = hash_sha256(password)

    def verify_password(self, password):
        """
        Verify if password is user password

        :param password: Password to test
        :type password: str

        :return: True if is user password, False else
        :rtype: bool
        """
        return self._password_hash == hash_sha256(password)

    def generate_auth_token(self, expiration=None):
        """
        Generate token for user authentification

        :param expiration: Auth expiration
        :type expiration: int

        :return: Auth token
        :rtype: str
        """

        if expiration is None:
            expiration = current_app.config['TOKEN_EXPIRATION_TIME']

        serializer = Serializer(current_app.config['SECRET_KEY'], expires_in=expiration)

        return serializer.dumps({'id': self._id})

    @staticmethod
    def verify_auth_token(token):
        """
        Return user form token

        :param token: Token
        :type token: str

        :return: User if valid token, else None
        :rtype: User|None
        """
        serializer = Serializer(current_app.config['SECRET_KEY'])

        try:
            data = serializer.loads(token)
        except SignatureExpired:
            print('SignatureExpired')
            return None
        except BadSignature:
            print('BadSignature')
            return None

        return data['id']