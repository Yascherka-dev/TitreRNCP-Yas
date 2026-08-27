from rest_framework import serializers
from .models import Favorite
from apps.references import validate_reference


class FavoriteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Favorite
        fields = ['id', 'type', 'reference_id', 'date_ajout']
        read_only_fields = ['date_ajout']

    def validate(self, attrs):
        # La base ne peut pas garantir l'existence d'une référence polymorphe :
        # c'est ici que ça se joue. Voir apps/references.py.
        return validate_reference(attrs)
