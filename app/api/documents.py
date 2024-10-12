from django_elasticsearch_dsl import Document, fields
from django_elasticsearch_dsl.registries import registry
from elasticsearch_dsl.connections import connections
from elasticsearch.helpers import bulk

from api.models import Literature


@registry.register_document
class LiteratureDocument(Document):

    class Index:
        name = "literature"
        settings = {"number_of_shards": 1, "number_of_replicas": 0}

    class Django:
        model = Literature
        fields = [
            "id",
            "title",
            "abstract",
            "publication_date",
        ]

    @classmethod
    def bulk_create_with_validation(cls, data_list):
        """Bulk index LiteratureDocument objects from a list of Literatures."""
        succeded, error = Literature.bulk_create_with_validation(data_list)
        if succeded:
            es_actions = []
            for data in succeded:
                es_actions.append({
                    "_index": "literature",
                    "_source": {
                        "title": data.title,
                        "abstract": data.abstract,
                        "publication_date": data.publication_date
                    }
                })
            es_client = connections.get_connection()
            bulk(es_client, es_actions)
        return succeded, error