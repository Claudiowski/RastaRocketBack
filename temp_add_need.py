from datetime import datetime
from elasticsearch import Elasticsearch
from config import config
import json


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
        'Author': 'AV7hRlqWL6CcnUT1H2Gt',
        'Title': 'My First need',
        'Description': 'My first need description',
        'SuccessKeys': [
            {'Key': 'Hard work'},
            {'Key': 'Good frequency'},
            {'Key': 'Coffee, lot of coffee'}
        ],
        'StartAtLatest': '2017-10-08T00:00:00',
        'MonthDuration': 0.5,
        'WeekFrequency': 5,
        'Rate': 10000.0,
        'Consultants': [
            {'Id': 'AV7hRneLL6CcnUT1H2Gu'}
        ],
        'Status': 'open'
    }

    response = client.index(
        index=indice,
        doc_type='need',
        body=need
    )

    print(json.dumps(response, indent=4))