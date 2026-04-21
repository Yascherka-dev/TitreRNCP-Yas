from datetime import date as today_date
from django.db.models import Case, When, Value, IntegerField
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from .models import Match
from .serializers import MatchSerializer
from .football_api import fetch_fixtures


class MatchListView(APIView):
    """Retourne les matchs stockés en base, filtrables par date."""
    permission_classes = [AllowAny]

    def get(self, request):
        qs = Match.objects.all()

        date = request.query_params.get('date')
        if date:
            qs = qs.filter(date_heure__date=date)

        # Tri : live en premier (0), à venir ensuite (1), terminés à la fin (2)
        qs = qs.annotate(
            ordre=Case(
                When(statut__in=['IN_PLAY', 'PAUSED', 'HALFTIME'], then=Value(0)),
                When(statut__in=['SCHEDULED', 'TIMED'], then=Value(1)),
                default=Value(2),
                output_field=IntegerField(),
            )
        ).order_by('ordre', 'date_heure')

        return Response(MatchSerializer(qs, many=True).data)


class SynchronizeView(APIView):
    """
    POST /api/matches/synchroniser/
    Appelle le service football_api, récupère les matchs du jour,
    et les sauvegarde en base (update_or_create).
    """
    permission_classes = [AllowAny]

    def post(self, _request):
        # Si ?date=YYYY-MM-DD est passé → synchro du jour seulement
        # Si pas de date → synchro de toute la saison
        date = _request.query_params.get('date', None)

        matches = fetch_fixtures(date)

        # Pour chaque match retourné par le service, on insère ou met à jour en base
        # update_or_create : si external_id existe déjà → on met à jour, sinon → on crée
        count = 0
        for match_data in matches:
            Match.objects.update_or_create(
                external_id=match_data['external_id'],  # clé de recherche
                defaults=match_data,                    # champs à insérer/mettre à jour
            )
            count += 1

        return Response({'status': 'ok', 'total': count})
