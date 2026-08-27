from rest_framework import serializers
from .models import Comment
from apps.references import validate_reference


class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ['id', 'type', 'reference_id', 'contenu', 'date_soumission']
        read_only_fields = ['date_soumission']

    def validate(self, attrs):
        # La base ne peut pas garantir l'existence d'une référence polymorphe :
        # c'est ici que ça se joue. Voir apps/references.py.
        return validate_reference(attrs)
