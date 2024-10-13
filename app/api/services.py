from api.models import ApiMetricsEntry
from django.db.models import Count, Avg, Max, Min

class ApiMetricsService:
    
    @staticmethod
    def log_user_query(query):
        """Logs the user query in the database."""
        ApiMetricsEntry.objects.create(query=query, query_type='user')

    @staticmethod
    def log_openai_metrics(query, response_time):
        """Logs the OpenAI API query and response time in the database."""
        ApiMetricsEntry.objects.create(query=query, response_time=response_time, query_type='openai')

    @staticmethod
    def get_most_common_user_queries(limit=10):
        """Fetches the most common user queries."""
        return ApiMetricsEntry.objects.filter(query_type='user')\
                                   .values('query')\
                                   .annotate(query_count=Count('query'))\
                                   .order_by('-query_count')[:limit]

    @staticmethod
    def get_openai_performance_metrics():
        """Fetches the performance metrics for OpenAI API requests in milliseconds, rounded to 6 decimal places."""
        metrics = ApiMetricsEntry.objects.filter(query_type='openai')

        average_response_time = metrics.aggregate(Avg('response_time'))['response_time__avg']
        fastest_response_time = metrics.aggregate(Min('response_time'))['response_time__min']
        slowest_response_time = metrics.aggregate(Max('response_time'))['response_time__max']

        return {
            'average_response_time': round(average_response_time * 1000, 6) if average_response_time is not None else None,
            'fastest_response_time': round(fastest_response_time * 1000, 6) if fastest_response_time is not None else None,
            'slowest_response_time': round(slowest_response_time * 1000, 6) if slowest_response_time is not None else None,
        }