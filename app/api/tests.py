from django.test import TestCase
from unittest.mock import patch
from api.tasks import harvest_inspirehep_data
from api.models import Literature
from api.services import ApiMetricsService
from api.models import ApiMetricsEntry
from rest_framework.exceptions import ValidationError
from api.serializers import LiteratureSerializer
from api.documents import LiteratureDocument

class HarvestInspirehepDataTestCase(TestCase):
    
    @patch('requests.get')
    def test_harvest_inspirehep_data(self, mock_get):
        # Simulate API response
        api_response = {
            'hits': {
                'hits': [
                    {
                        'metadata': {
                            'titles': [{'title': 'Test Paper'}],
                            'abstracts': [{'value': 'Test Abstract'}],
                            'arxiv_eprints': [{'value': 'arXiv:1234.56789'}],
                            'imprints': [{'date': '2021-12-01'}]
                        }
                    }
                ]
            }
        }

        mock_get.return_value.status_code = 200
        mock_get.return_value.json.return_value = api_response

        harvest_inspirehep_data()

        self.assertEqual(Literature.objects.count(), 1)
        literature = Literature.objects.first()
        self.assertEqual(literature.title, 'Test Paper')
        self.assertEqual(literature.abstract, 'Test Abstract')
        self.assertEqual(literature.arxiv_id, 'arXiv:1234.56789')
        self.assertEqual(literature.publication_date.strftime('%Y-%m-%d'), '2021-12-01')

class ApiMetricsServiceTestCase(TestCase):
    
    def test_log_user_query(self):
        ApiMetricsService.log_user_query("Test Query")
        self.assertEqual(ApiMetricsEntry.objects.count(), 1)
        entry = ApiMetricsEntry.objects.first()
        self.assertEqual(entry.query, "Test Query")
        self.assertEqual(entry.query_type, 'user')

    def test_log_openai_metrics(self):
        ApiMetricsService.log_openai_metrics("Summarization Query", 1.234)
        self.assertEqual(ApiMetricsEntry.objects.count(), 1)
        entry = ApiMetricsEntry.objects.first()
        self.assertEqual(entry.query, "Summarization Query")
        self.assertEqual(entry.response_time, 1.234)
        self.assertEqual(entry.query_type, 'openai')

class LiteratureSerializerTestCase(TestCase):

    def test_literature_serializer_valid(self):
        data = {
            'title': 'Test Paper',
            'abstract': 'This is a test abstract.',
            'publication_date': '2021-12-01'
        }
        serializer = LiteratureSerializer(data=data)
        self.assertTrue(serializer.is_valid())

    def test_literature_serializer_invalid(self):
        data = {
            'title': '',
            'abstract': 'This is a test abstract.',
            'publication_date': '2021-12-01'
        }
        serializer = LiteratureSerializer(data=data)
        with self.assertRaises(ValidationError):
            serializer.is_valid(raise_exception=True)

class LiteratureBulkCreateTestCase(TestCase):

    def test_bulk_create_with_validation(self):
        data_list = [
            {
                'title': 'Test Paper 1',
                'abstract': 'Abstract 1',
                'publication_date': '2021-12-01',
            },
            {
                'title': 'Test Paper 2',
                'abstract': 'Abstract 2',
                'publication_date': '2021-12-02',
            },
        ]

        succeeded, errors = Literature.bulk_create_with_validation(data_list)
        self.assertEqual(len(succeeded), 2)
        self.assertEqual(len(errors), 0)
        self.assertEqual(Literature.objects.count(), 2)

class LiteratureDocumentBulkCreateTestCase(TestCase):

    def test_bulk_create_with_validation(self):
        data_list = [
            {
                'title': 'Test Paper 1',
                'abstract': 'Abstract 1',
                'publication_date': '2021-12-01',
            },
            {
                'title': 'Test Paper 2',
                'abstract': 'Abstract 2',
                'publication_date': '2021-12-02',
            },
        ]

        succeeded, errors = LiteratureDocument.bulk_create_with_validation(data_list)
        self.assertEqual(len(succeeded), 2)
        self.assertEqual(len(errors), 0)
