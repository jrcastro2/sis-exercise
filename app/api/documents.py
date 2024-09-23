from django_elasticsearch_dsl import Document, fields
from django_elasticsearch_dsl.registries import registry

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
