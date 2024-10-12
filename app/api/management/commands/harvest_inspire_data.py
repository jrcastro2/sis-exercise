from django.core.management.base import BaseCommand
from api.tasks import harvest_inspirehep_data

class Command(BaseCommand):
    help = 'Triggers the Celery task to harvest InspireHEP data'

    def handle(self, *args, **kwargs):
        result = harvest_inspirehep_data.delay()

        self.stdout.write(self.style.SUCCESS(f'Triggered task: {result.id}'))