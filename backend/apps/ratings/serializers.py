from rest_framework import serializers
from .models import Rating


class RatingSerializer(serializers.ModelSerializer):
    valeur = serializers.IntegerField(min_value=1, max_value=5)

    class Meta:
        model = Rating
        fields = ['id', 'type', 'reference_id', 'valeur', 'date']
        read_only_fields = ['date']
