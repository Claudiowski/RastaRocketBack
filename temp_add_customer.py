from elasticsearch import Elasticsearch, helpers
from elasticsearch_dsl import Search
from config import config


if __name__ == '__main__':
    app_config = config['default']
    indice = 'rastarockets_customers'

    customers = [
        {
            'Name': 'BNP PARIBAS'
        },
        {
            'Name': 'BNP NTM'
        },
        {
            'Name': 'ORANGE'
        },
        {
            'Name': 'SOCIÉTÉ GÉNÉRALE'
        },
        {
            'Name': 'BPCE'
        },
        {
            'Name': 'EDF'
        },
        {
            'Name': 'CRÉDIT AGRICOLE'
        },
        {
            'Name': 'THALES'
        },
        {
            'Name': 'SNCF'
        },
        {
            'Name': 'TELEFONICA'
        },
        {
            'Name': 'ALLIANZ'
        }
    ]
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
                    "customer": {
                        "properties": {
                            "Name": {
                                "type": "text",
                                "analyzer": "autocomplete",
                                "search_analyzer": "standard"
                            }
                        }
                    },
                    'contact': {
                        'properties': {
                            'Customer': {
                                'type': 'text'
                            },
                            'Name': {
                                'type': 'text',
                                'analyzer': 'autocomplete',
                                'search_analyzer': 'standard'
                            },
                            'Email': {
                                'type': 'text',
                                'analyzer': 'autocomplete',
                                'search_analyzer': 'standard'
                            }
                        }
                    }
                }
            }
        )

    bulk_commands = []
    for customer in customers:
        search = Search(
            using=client,
            index=indice
        ).query("match_phrase", Name=customer['Name'])

        response = search.execute()

        if response.hits.total == 0:
            print('{0} added to bulk'.format(customer['Name']))

            bulk_commands.append({
                '_type': 'customer',
                '_index': indice,
                '_source': customer
            })

        else:
            print('{0} already exist'.format(customer['Name']))

    if len(bulk_commands) > 0:
        helpers.bulk(client, bulk_commands)
        print('{0} customer(s) added'.format(len(bulk_commands)))