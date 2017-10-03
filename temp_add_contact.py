from elasticsearch import Elasticsearch, helpers
from elasticsearch_dsl import Search
from config import config


if __name__ == '__main__':
    app_config = config['default']
    indice = 'rastarockets_customers'

    client = Elasticsearch([{'host': app_config.ELS_HOST, 'port': app_config.ELS_PORT}])
    customer_name = 'BNP PARIBAS'
    contact = {
        'Name': 'Jean Bon',
        'Email': 'jeanbon@bnp.fr'
    }

    search = Search(
        using=client,
        index=indice,
        doc_type='customer'
    ).query('match_phrase', Name=customer_name)

    response = search.execute()

    if response.hits.total > 0:
        customer = response.hits[0]

        contact['Customer'] = customer.meta.id

        response = client.index(
            index=indice,
            doc_type='contact',
            body=contact
        )

        print(response)