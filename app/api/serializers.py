from rest_framework import serializers


class LiteratureSerializer(serializers.Serializer):

    title = serializers.CharField()
    abstract = serializers.CharField()
    publication_date = serializers.DateField()
    arxiv_id = serializers.CharField(required=False, allow_null=True, allow_blank=True)

    class Meta:
        fields = (
            "title",
            "abstract",
            "publication_date",
        )
 