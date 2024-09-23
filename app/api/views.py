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
