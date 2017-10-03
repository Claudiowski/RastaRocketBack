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