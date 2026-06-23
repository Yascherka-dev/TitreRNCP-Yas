from rest_framework import serializers
from .models import Favorite


class FavoriteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Favorite
        fields = ['id', 'type', 'reference_id', 'date_ajout']
        read_only_fields = ['date_ajout']
