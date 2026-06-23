from rest_framework import serializers
from .models import Comment


class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ['id', 'type', 'reference_id', 'contenu', 'date_soumission']
        read_only_fields = ['date_soumission']
