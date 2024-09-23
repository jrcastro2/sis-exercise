from rest_framework import serializers

from api.models import Literature


class LiteratureSerializer(serializers.Serializer):

    title = serializers.CharField()
    abstract = serializers.CharField()
    publication_date = serializers.DateField(read_only=True)

    class Meta:
        fields = (
            "title",
            "abstract",
            "publication_date",
        )
