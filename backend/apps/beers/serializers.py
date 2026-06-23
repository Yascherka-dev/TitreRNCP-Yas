from rest_framework import serializers
from .models import Beer


class BeerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Beer
        fields = [
            'id', 'nom', 'brasserie', 'pays', 'region', 'equipe',
            'style', 'description', 'degre_alcool', 'image_url',
        ]
