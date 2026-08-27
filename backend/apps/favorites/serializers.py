from rest_framework import serializers

from apps.cible_serializer import CibleReferenceSerializerMixin
from .models import Favorite


class FavoriteSerializer(CibleReferenceSerializerMixin, serializers.ModelSerializer):
    class Meta:
        model = Favorite
        fields = ['id', 'type', 'reference_id', 'date_ajout']
        read_only_fields = ['date_ajout']
