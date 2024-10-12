from celery import shared_task
import requests
from api.documents import LiteratureDocument
from django.conf import settings
from api.errors import BulkSaveError

@shared_task
def harvest_inspirehep_data(size=40, sort="mostrecent"):
    """Harvest data from inspirehep API."""
    params = {"size": size, "sort": sort}
    response = requests.get(settings.INSPIRE_LITERATURE_API_URL, params=params)
    if response.status_code == 200:
        data = response.json().get('hits', {}).get('hits', [])
        data_list = []

        for record in data:
            metadata = record.get('metadata', {})

            title = metadata.get('titles', [{'title': ''}])[0].get('title', '')
            abstract = metadata.get('abstracts', [{'value': ''}])[0].get('value', '')
            arxiv_id = metadata.get('arxiv_eprints', [{'value': ''}])[0].get('value', '')
            publication_date = metadata.get('imprints', [{'date': None}])[0].get('date', None)

            data_list.append({
                'title': title,
                'abstract': abstract,
                'arxiv_id': arxiv_id,
                'publication_date': publication_date
            })

        _, errors = LiteratureDocument.bulk_create_with_validation(data_list)
            
        if errors:
            raise BulkSaveError(
                "Validation errors occurred during harvesting.",
                errors=errors
            )


