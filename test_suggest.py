from elasticsearch import Elasticsearch, helpers
from elasticsearch_dsl import Search
from config import config
import json


if __name__ == '__main__':
    app_config = config['default']
    indice = 'rastarockets_customers'

    client = Elasticsearch([{'host': app_config.ELS_HOST, 'port': app_config.ELS_PORT}])

    search = client.search(
        index=indice,
        doc_type='customer',
        body={
            'query': {
                'match': {'Name': 'BNP'}
            }
        }
    )

    print(json.dumps(search, indent=4))