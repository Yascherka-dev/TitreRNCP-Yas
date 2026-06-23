from rest_framework import serializers
from .models import Rating


class RatingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Rating
        fields = ['id', 'type', 'reference_id', 'valeur', 'date']
        read_only_fields = ['date']
