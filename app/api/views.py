import time
from api.services import ApiMetricsService
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
from elasticsearch.exceptions import TransportError, ConnectionError, NotFoundError

from api.serializers import LiteratureSerializer
from api.documents import LiteratureDocument
from api.models import Literature
from django.conf import settings
import requests
import logging
from requests.exceptions import RequestException
from rest_framework.views import APIView

logger = logging.getLogger(__name__)


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
        return Q("multi_match", query=query, fields=["title", "abstract"])

    def get(self, request, *args, **kwargs):
        """
        Extend the GET method to include summarization after retrieving search results.
        """
        try:
            query = request.query_params.get("query", "")
            ApiMetricsService.log_user_query(query)
            response = super().get(request, *args, **kwargs)
        except (TransportError, ConnectionError, NotFoundError) as e:
            logger.error(f"Elasticsearch query error: {str(e)}")
            return Response(
                {"error": "Error querying Elasticsearch.", "details": str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )
        except Exception as e:
            logger.error(f"Unexpected error during search: {str(e)}")
            return Response(
                {"error": "An unexpected error occurred during the search."},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )
        if not (200 <= response.status_code < 300):
            return response
        
        results = response.data.get("results", [])
        if response.status_code == 200 and results:
            titles_and_abstracts = []
            for item in results:
                title = item.get("title", "")
                abstract = item.get("abstract", "")
                titles_and_abstracts.append(f"Title: {title}\nAbstract: {abstract}")
                text_to_summarize = "\n\n".join(titles_and_abstracts)
            try:
                start_time = time.time()
                summary = self.summarize_text(text_to_summarize)
                end_time = time.time()
                response_time = end_time - start_time
                ApiMetricsService.log_openai_metrics(text_to_summarize, response_time)

            except RequestException as e:
                logger.error(f"Error communicating with the OpenAI API: {str(e)}")
                return Response(
                    {"error": "Error communicating with the OpenAI API."},
                    status=status.HTTP_502_BAD_GATEWAY,
                )
            except Exception as e:
                logger.error(f"Unexpected error during summarization: {str(e)}")
                return Response(
                    {"error": "An unexpected error occurred during summarization."},
                    status=status.HTTP_500_INTERNAL_SERVER_ERROR,
                )
            response.data = {
                "summary": summary,
                "results": results,
                "total": response.data.get("total", 0),
                "offset": response.data.get("offset", 0),
                "limit": response.data.get("limit", 10),
            }

        return response

    def summarize_text(self, text):
        """
        Summarize the provided text using OpenAI API or a mock summarization.
        """
        if settings.USE_OPENAI:
            try:
                response = requests.post(
                    "https://api.openai.com/v1/completions",
                    headers={
                        "Authorization": f"Bearer {settings.OPENAI_API_KEY}",
                        "Content-Type": "application/json",
                    },
                    json={
                        "model": "gpt-4",
                        "messages": [
                            {
                                "role": "user",
                                "content": "Provide a concise summary of the following data, summarize it in one paragraph:"
                                + text,
                            }
                        ],
                        "temperature": 0.7,
                    },
                    timeout=10,
                )
                response.raise_for_status()
                return (
                    response.json()
                    .get("choices", [{}])[0]
                    .get("message", {})
                    .get("content", "Error during summarization.")
                )
            except RequestException as e:
                logger.error(f"OpenAI API request failed: {str(e)}")
                raise e
            except Exception as e:
                logger.error(f"Unexpected error while summarizing: {str(e)}")
                raise e

        # Fallback to a mock summary
        return "Lorem ipsum dolor sit amet, consectetur adipiscing elit. Sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum."


class CommonUserQueriesView(APIView):
    def get(self, request):
        common_queries = ApiMetricsService.get_most_common_user_queries()
        return Response(common_queries, status=status.HTTP_200_OK)


class OpenAIMetricsView(APIView):
    def get(self, request):
        performance_metrics = ApiMetricsService.get_openai_performance_metrics()
        return Response(performance_metrics, status=status.HTTP_200_OK)
