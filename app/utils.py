# -*- coding: utf-8 -*-

import hashlib


def hash_sha256(content):
    """
    Hash SHA256

    :param content: Content
    :type content: str

    :return: Hashed content
    :rtype: str
    """

    hasher = hashlib.sha256()
    hasher.update(content.encode('utf-8'))

    return hasher.hexdigest()


def get_name_without_extension(filename):
    """
    Return name of file

    :param filename: Filename
    :type filename: str

    :return: Name of file
    :rtype: str
    """
    name = ''
    if '.' in filename:
        name = filename.rsplit('.', 1)[0].lower()
    return name


def get_extension(filename):
    """
    Return extension of file

    :param filename: Filename
    :type filename: str

    :return: Extension of filename
    :rtype: str
    """
    extension = ''
    if '.' in filename:
        extension = filename.rsplit('.', 1)[1].lower()
    return extension


def allowed_file(config, filename):
    """
    Determine if file is allowed

    :param filename: Filename with extension
    :type filename: str

    :param config: Configuration object
    :type config: object

    :return: True si le fichier est valide
    :rtype: bool
    """
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in config
