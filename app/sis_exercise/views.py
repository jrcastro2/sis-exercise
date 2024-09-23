import abc
from typing import Any
from typing import Dict

from django.urls import reverse
from django.views.generic import RedirectView
from elasticsearch_dsl import Q
from elasticsearch_dsl.query import Bool
from elasticsearch_dsl.response import Response
from elasticsearch_dsl.search import Search
from rest_framework import status
from rest_framework.response import Response as DRFResponse
from rest_framework.views import APIView

from sis_exercise.exceptions import APIViewError
from sis_exercise.serializers import SearchQuerySerializer


class IndexRedirectView(RedirectView):
    def get_redirect_url(self, *args, **kwargs):
        return str(reverse("api-search-search"))


class ElasticSearchAPIView(APIView):
    """
    An API view for paginating and retrieving search results from Elasticsearch.

    Attributes:
        serializer_class (type): The serializer class to use for formatting search results.
        document_class (type): The Elasticsearch document class representing the data.

    Subclasses must implement the 'elasticsearch_query_expression' method, which returns a query expression (Q()).

    Pagination Limitation:
    By default, you cannot use 'from' and 'size' to page through more than 10,000 hits.
    This limit is a safeguard set by the 'index.max_result_window' index setting.
    If you need to page through more than 10,000 hits, use more advanced solution.

    Elasticsearch docs: https://www.elastic.co/guide/en/elasticsearch/reference/current/paginate-search-results.html
    """

    serializer_class = None
    document_class = None
    query_serializer_class = SearchQuerySerializer

    @abc.abstractmethod
    def elasticsearch_query_expression(self, query):
        """This method should be overridden and return a Q() expression."""

    def get(self, request):
        """
        Handle GET requests for paginated search results.

        This endpoint allows paginated retrieval of search results from Elasticsearch.
        Pagination parameters are expected as query parameters.

        Parameters:
        - query (str): The search query string.
        - offset (int): The starting position of the search results.
        - limit (int): The number of results to retrieve in a single page.

        Returns:
        A paginated list of search results serialized according to 'serializer_class'.

        Raises:
        - HTTP 400 Bad Request: If query parameters are invalid.
        - HTTP 500 Internal Server Error: If an error occurs during data retrieval.
        """
        search_query_serializer = self.query_serializer_class(data=request.GET.dict())
        if not search_query_serializer.is_valid():
            return DRFResponse(
                f"Validation error: {search_query_serializer.errors}",
                status=status.HTTP_400_BAD_REQUEST
            )

        query_data = search_query_serializer.validated_data
        try:
            # Check if the 'query' parameter is provided and not empty
            if query_data.get("query"):
                # Build the search query using the user's input
                search_query = self.elasticsearch_query_expression(query_data["query"])
            else:
                # Use a 'match_all' query to retrieve all documents
                search_query = Q("match_all")

            search = self.document_class.search().query(search_query)

            # Apply pagination
            offset = query_data.get("offset", 0)
            limit = query_data.get("limit", 10)
            search = search[offset : offset + limit]

            response = search.execute()

            serializer = self.serializer_class(list(response.hits), many=True)
            return DRFResponse(serializer.data, status=status.HTTP_200_OK)
        except Exception as e:
            return DRFResponse(
                f"Error during fetching data: {str(e)}",
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
