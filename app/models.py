# -*- coding: utf-8 -*-

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
        self._name = els_object.Name
        self._role = els_object.Role

        if hasattr(els_object, 'PasswordHash'):
            self._password_hash = els_object.PasswordHash

    @property
    def id(self):
        """
        Return user unique ID

        :return: ID
        :rtype: str
        """
        return self._id

    @property
    def name(self):
        """
        Return user name

        :return: User name
        :rtype: str
        """
        return self._name

    @property
    def role(self):
        """
        Return role of user

        :return: Role
        :rtype: role
        """
        return self._role

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

    def __eq__(self, other):
        return self._id == other.id


class Need:
    """
    Represent customer need
    """

    def __init__(self, els_object):
        """
        Constructor

        :param els_object: Elasticsearch object document
        :type els_object: object
        """
        self._id = els_object.meta.id
        self._author = els_object.Author
        self._title = els_object.Title
        self._created_at = els_object.CreatedAt
        self._contact = els_object.Contact
        self._customer = els_object.Customer
        self._status = els_object.Status

        if hasattr(els_object, 'StartAtLatest'):
            self._start_at_latest = els_object.StartAtLatest
        else:
            self._start_at_latest = None

        if hasattr(els_object, 'Description'):
            self._description = els_object.Description
        else:
            self._description = ""

        if hasattr(els_object, 'MonthDuration'):
            self._month_duration = els_object.MonthDuration
        else:
            self._month_duration = -1

        if hasattr(els_object, "WeekFrequency"):
            self._week_frequency = els_object.WeekFrequency
        else:
            self._week_frequency = -1

        if hasattr(els_object, "Rate"):
            self._rate = els_object.Rate
        else:
            self._rate = -1

        if hasattr(els_object, "Consultants"):
            self._consultants = []
            for consultant in els_object.Consultants:
                self._consultants.append(consultant.Id)
        else:
            self._consultants = []

        if hasattr(els_object, "SuccessKeys"):
            self._success_keys = []
            for key in els_object.SuccessKeys:
                self._success_keys.append(key.Key)

        else:
            self._success_keys = []

    @property
    def id(self):
        """
        Return need unique ID

        :return: ID
        :rtype: str
        """
        return self._id

    @property
    def author(self):
        """
        Return author of need

        :return: Author ID
        :rtype: str
        """
        return self._author

    @property
    def created_at(self):
        """
        Return date of creation

        :return: Date of creation
        :rtype: str
        """
        return self._created_at

    @property
    def start_at_latest(self):
        """
        Return start at latest date

        :return: Start at latest date
        :rtype: str
        """
        return self._start_at_latest

    @property
    def customer(self):
        """
        Return customer of need

        :return: Customer
        :rtype: str
        """
        return self._customer

    @property
    def contact(self):
        """
        Return contact of need

        :return: Contact
        :rtype: str
        """
        return self._contact

    @property
    def title(self):
        """
        Return title of need

        :return: Title
        :rtype: str
        """
        return self._title

    @property
    def status(self):
        """
        return status of need

        :return: Status
        :rtype: str
        """
        return self._status

    @property
    def description(self):
        return self._description

    @property
    def month_duration(self):
        return self._month_duration

    @property
    def week_frequency(self):
        return self._week_frequency

    @property
    def consultants(self):
        return self._consultants

    @property
    def success_keys(self):
        return self._success_keys

    @property
    def rate(self):
        return self._rate

class Customer:
    """
    Represent customer
    """

    def __init__(self, els_object):
        """
        Constructor

        :param els_object: Elasticsearch object document
        :type els_object: object
        """
        self._id = els_object.meta.id
        self._name = els_object.Name

    @property
    def id(self):
        """
        Return customer ID

        :return: Customer ID
        :rtype: str
        """
        return self._id

    @property
    def name(self):
        """
        Return customer name

        :return: Customer name
        :rtype: str
        """
        return self._name


class CustomerContact:
    """
    Represent customer contact
    """

    def __init__(self, els_object):
        """
        Constructor

        :param els_object: Elasticsearch object document
        :type els_object: object
        """
        self._id = els_object.meta.id
        self._name = els_object.Name
        self._email = els_object.Email

    @property
    def id(self):
        """
        Return contact unique ID

        :return: Contact unique ID
        :rtype: str
        """
        return self._id

    @property
    def name(self):
        """
        Return contact name

        :return: Contact name
        :rtype: str
        """
        return self._name

    @property
    def email(self):
        """
        Return contact email

        :return: Contact email
        :rtype str
        """
        return self._email


class NeedContent:
    """
    Represent file of need
    """

    def __init__(self, els_object):
        """
        Constructor

        :param els_object: Elasticsearch object document
        :type els_object: object
        """
        self._id = els_object.meta.id
        self._need = els_object.Need
        self._filename = els_object.Filename

    @property
    def id(self):
        """
        Return need content ID

        :return: Need content ID
        :rtype: str
        """
        return self._id

    @property
    def need(self):
        """
        Return need

        :return: Need ID
        :rtype: str
        """
        return self._need

    @property
    def filename(self):
        """
        Return filename

        :return: Filename
        :rtype: str
        """
        return self._filename
