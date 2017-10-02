from elasticsearch import Elasticsearch
from config import config
from app.utils import hash_sha256


if __name__ == '__main__':
    app_config = config['default']
    indice = 'rastarockets_users'

    client = Elasticsearch([{'host': app_config.ELS_HOST, 'port': app_config.ELS_PORT}])

    if not client.indices.exists(indice):
        client.indices.create(
            index=indice,
            body={
                "settings": {
                    "number_of_shards": 1,
                    "number_of_replicas": 0
                }
            }
        )

    user = {
        'Email': 'averdier@gfi.fr',
        'PasswordHash': hash_sha256('averdier')
    }

    user_search = client.search(
        index=indice,
        doc_type='user',
        body={
            'query': {
                'match_phrase': {'Email': user['Email']}
            }
        }
    )

    user_already_exist = user_search['hits']['max_score'] is not None

    if not user_already_exist:
        client.index(
            index=indice,
            doc_type='user',
            body=user
        )

        print('user {0} added'.format(user['Email']))

    else:
        print('user {0} already exist'.format(user['Email']))