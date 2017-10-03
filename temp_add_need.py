from datetime import datetime
from elasticsearch import Elasticsearch
from config import config


if __name__ == '__main__':
    app_config = config['default']
    indice = 'rastarockets_needs'

    client = Elasticsearch([{'host': app_config.ELS_HOST, 'port': app_config.ELS_PORT}])

    if not client.indices.exists(indice):
        client.indices.create(
            index=indice,
            body={
                "settings": {
                    "number_of_shards": 1,
                    "number_of_replicas": 0,
                    "analysis": {
                      "filter": {
                        "autocomplete_filter": {
                          "type": "edge_ngram",
                          "min_gram": 1,
                          "max_gram": 20
                        }
                      },
                      "analyzer": {
                        "autocomplete": {
                          "type": "custom",
                          "tokenizer": "standard",
                          "filter": [
                            "lowercase",
                            "autocomplete_filter"
                          ]
                        }
                      }
                    }
                },
                "mappings": {
                    'need': {
                        'properties': {
                            'CreatedAt': {'type': 'date'},
                            'Author': {'type': 'text'},
                            'Customer': {'type': 'text'},
                            'Contact': {'type': 'text'},
                            'Title': {
                                'type': 'text',
                                'analyzer': 'autocomplete',
                                'search_analyzer': 'standard'
                            },
                            'Description': {'type': 'text'},
                            'SuccessKeys': {'type': 'nested'},
                            'StartAtLatest': {'type': 'date'},
                            'MonthDuration': {'type': 'float'},
                            'WeekFrequency': {'type':  'float'},
                            'Rate': {'type': 'float'},
                            'Consultants': {'type': 'nested'},
                            'Status': {'type': 'text'},
                        }
                    },
                }
            }
        )

    need = {
        'CreatedAt': datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%S'),
        'Customer': 'AV7hICkGL6CcnUT1H2Gf',
        'Contact': 'AV7hID2XL6CcnUT1H2Gq',
        'Author': 'AV7hRlqWL6CcnUT1H2Gt'
    }