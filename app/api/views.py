from sis_exercise.views import ElasticSearchAPIView
from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import action
from django_elasticsearch_dsl_drf.viewsets import DocumentViewSet
from django_elasticsearch_dsl_drf.filter_backends import (
    FilteringFilterBackend,
    OrderingFilterBackend,
    DefaultOrderingFilterBackend,
    SearchFilterBackend,
)
from elasticsearch_dsl import Q

from api.serializers import LiteratureSerializer
from api.documents import LiteratureDocument
from api.models import Literature


class LiteratureDocumentViewSet(DocumentViewSet):
    document = LiteratureDocument
    serializer_class = LiteratureSerializer
    lookup_field = "id"
    filter_backends = []
    ordering = ("_score",)
    filter_backends = [
        OrderingFilterBackend,
        DefaultOrderingFilterBackend,
        SearchFilterBackend,
    ]
    search_fields = ("title",)

    ordering_fields = {
        "id": "id",
        "title": "title.raw",
        "publication_date": "publication_date",
    }

class LiteratureSearchView(ElasticSearchAPIView):
    serializer_class = LiteratureSerializer
    document_class = LiteratureDocument

    def elasticsearch_query_expression(self, query):
        """
        Define the search query that searches for the query string
        in the 'title' and 'abstract' fields of the document.
        """
        return Q("multi_match", query=query, fields=['title', 'abstract'])