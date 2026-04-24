from rest_framework import serializers
from .models import Match


class MatchSerializer(serializers.ModelSerializer):
    id = serializers.CharField(source='external_id')

    class Meta:
        model = Match
        fields = [
            'id', 'sport', 'competition', 'league_id',
            'equipe_a', 'equipe_b',
            'pays_a', 'pays_b',
            'date_heure', 'statut',
            'score_a', 'score_b',
            'logo_a', 'logo_b',
            'venue', 'thumb_url',
        ]


class LivescoreUpdateSerializer(serializers.Serializer):
    external_id = serializers.CharField()
    statut      = serializers.CharField()
    score_a     = serializers.IntegerField(allow_null=True)
    score_b     = serializers.IntegerField(allow_null=True)
