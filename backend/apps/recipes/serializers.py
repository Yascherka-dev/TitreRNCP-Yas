from rest_framework import serializers
from .models import Recipe


class RecipeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Recipe
        fields = [
            'id', 'titre', 'pays', 'region', 'equipe', 'type_plat',
            'description', 'temps_preparation', 'temps_cuisson',
            'nb_personnes', 'difficulte', 'ingredients', 'etapes',
            'tags', 'image_url',
        ]
