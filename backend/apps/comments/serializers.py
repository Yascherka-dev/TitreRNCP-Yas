from rest_framework import serializers

from apps.cible_serializer import CibleReferenceSerializerMixin
from .models import Comment


class CommentSerializer(CibleReferenceSerializerMixin, serializers.ModelSerializer):
    # Le prénom seul : il suffit à signer un commentaire public, là où
    # l'email identifierait la personne.
    auteur = serializers.CharField(source='user.prenom', read_only=True)

    class Meta:
        model = Comment
        fields = ['id', 'user', 'auteur', 'type', 'reference_id',
                  'contenu', 'date_soumission']
        read_only_fields = ['user', 'auteur', 'date_soumission']
