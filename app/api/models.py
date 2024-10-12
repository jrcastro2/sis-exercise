from django.db import models

from api.serializers import LiteratureSerializer
from rest_framework.exceptions import ValidationError


class Literature(models.Model):
    title = models.CharField(max_length=200)
    abstract = models.TextField()
    arxiv_id = models.CharField(max_length=50, blank=True, null=True)
    publication_date = models.DateField()


    @classmethod
    def bulk_create_with_validation(cls, data_list):
        """Validates and creates multiple Literature objects from a list of dictionaries."""
        valid_objects = []
        errors = []

        for data in data_list:
            serializer = LiteratureSerializer(data=data)

            try:
                if serializer.is_valid(raise_exception=True):
                    valid_objects.append(cls(**serializer.validated_data))
            except ValidationError as e:
                errors.append({
                    'data': data,
                    'errors': serializer.errors
                })

        if valid_objects:
            succeeded = cls.objects.bulk_create(valid_objects)
        
        return succeeded, errors