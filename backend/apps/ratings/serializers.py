from rest_framework import serializers
from .models import Rating
from apps.references import validate_reference


class RatingSerializer(serializers.ModelSerializer):
    valeur = serializers.IntegerField(min_value=1, max_value=5)

    class Meta:
        model = Rating
        fields = ['id', 'type', 'reference_id', 'valeur', 'date']
        read_only_fields = ['date']

    def validate(self, attrs):
        # La base ne peut pas garantir l'existence d'une référence polymorphe :
        # c'est ici que ça se joue. Voir apps/references.py.
        return validate_reference(attrs)
