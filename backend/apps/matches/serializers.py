from rest_framework import serializers
from .models import Match


class MatchSerializer(serializers.ModelSerializer):
    id = serializers.CharField(source='external_id')

    class Meta:
        model = Match
        fields = [
            'id', 'sport', 'competition',
            'equipe_a', 'equipe_b',
            'pays_a', 'pays_b',
            'date_heure', 'statut',
            'score_a', 'score_b',
            'logo_a', 'logo_b',
        ]
