from flask import current_app
from .models import User, Need
from elasticsearch_dsl import Search


def get_user_from_email(email, index='rastarockets_users'):
    """
    Return user from unique email address

    :param email: User email address
    :type email: str

    :param index: Index name (optional)
    :type index: str

    :return: User if exist
    :rtype: User|None
    """

    search = Search(
        using=current_app.els_client,
        index=index
    ).query('match_phrase', Email=email)

    response = search.execute()

    if response.hits.total > 0:
        return User(response.hits[0])

    else:
        return None


def get_user_from_id(user_id, index='rastarockets_users'):
    """
    Return user from unique ID

    :param user_id: User unique ID
    :type user_id: str

    :param index: Index name (optional)
    :type index: str

    :return: User if exist
    :rtype: User|None
    """

    search = Search(
        using=current_app.els_client,
        index=index
    ).query('term', _id=user_id)

    response = search.execute()

    if response.hits.total > 0:
        return User(response.hits[0])

    else:
        return None


def get_need_from_id(need_id, index='rastarockets_needs'):
    """
    Return need from unique ID
    
    :param need_id: Need unique ID
    :type need_id: str
    
    :param index: Index name (optional)
    :type index: str
    
    :return: Need if exist
    :rtype: Need|None
    """

    search = Search(
        using=current_app.els_client,
        index=index
    ).query('term', _id=need_id)

    response = search.execute()

    if response.hits.total > 0:
        return Need(response.hits[0])

    else:
        return None


def delete_need_from_id(need_id, index='rastarockets_needs'):
    """
    Delete need from unique ID

    :param need_id: Need unique ID
    :type need_id: str

    :param index: Index name (optional)
    :type index: str

    :return: True if success, else False
    :rtype: bool
    """

    response = current_app.els_client.delete_by_query(
        index=index,
        doc_type='need',
        body={
            'query': {
                'term': {'_id': need_id}
            }
        }
    )

    # TODO get response value
    return True
