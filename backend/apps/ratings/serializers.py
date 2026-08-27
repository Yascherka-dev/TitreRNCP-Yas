from rest_framework import serializers

from apps.cible_serializer import CibleReferenceSerializerMixin
from .models import Rating


class RatingSerializer(CibleReferenceSerializerMixin, serializers.ModelSerializer):
    valeur = serializers.IntegerField(min_value=1, max_value=5)

    class Meta:
        model = Rating
        fields = ['id', 'user', 'type', 'reference_id', 'valeur', 'date']
        read_only_fields = ['user', 'date']
