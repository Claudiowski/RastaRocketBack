from elasticsearch import Elasticsearch, helpers
from elasticsearch_dsl import Search
from config import config
from app.utils import hash_sha256


if __name__ == '__main__':
    app_config = config['default']
    indice = 'rastarockets_customers'

    customers = ["BNP PARIBAS", "ORANGE", "SOCIÉTÉ GÉNÉRALE", "BPCE", "EDF", "CRÉDIT AGRICOLE", "THALES", "SNCF", "TELEFONICA", "ALLIANZ"]

    client = Elasticsearch([{'host': app_config.ELS_HOST, 'port': app_config.ELS_PORT}])

    if not client.indices.exists(indice):
        client.indices.create(
            index=indice,
            body={
                "settings": {
                    "number_of_shards": 1,
                    "number_of_replicas": 0
                },
                "mappings": {
                    "customer": {
                        "_all": {"enabled": False},
                        "properties": {
                            "Name": {"type": "text"},
                            "NameSuggest": {"type": "completion"}
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
        ).query("match_phrase", Name=customer)

        response = search.execute()

        if response.hits.total == 0:
            print('{0} added to bulk'.format(customer))

            bulk_commands.append({
                '_type': 'customer',
                '_index': indice,
                '_source': {
                    'Name': customer,
                    'NameSuggest': customer
                }
            })

        else:
            print('{0} already exist'.format(customer))

    if len(bulk_commands) > 0:
        helpers.bulk(client, bulk_commands)
        print('{0} customer(s) added'.format(len(bulk_commands)))