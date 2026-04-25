from django.db.models import Case, When, Value, IntegerField
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from .models import Match
from .serializers import MatchSerializer
from .sports_api import fetch_fixtures, fetch_livescores


class MatchListView(APIView):
    """GET /api/matches/ — liste des matchs stockés, filtrables par date et sport."""
    permission_classes = [AllowAny]

    def get(self, request):
        qs = Match.objects.all()

        date = request.query_params.get('date')
        if date:
            qs = qs.filter(date_heure__date=date)

        sport = request.query_params.get('sport')
        if sport:
            qs = qs.filter(sport=sport)

        # Tri : live (0) → à venir (1) → terminés (2)
        qs = qs.annotate(
            ordre=Case(
                When(statut__in=['1H', '2H', 'HT', 'ET', 'P', 'BT'], then=Value(0)),
                When(statut__in=['NS', 'TBD'],                         then=Value(1)),
                default=Value(2),
                output_field=IntegerField(),
            )
        ).order_by('ordre', 'date_heure')

        return Response(MatchSerializer(qs, many=True).data)


class SynchronizeView(APIView):
    """
    POST /api/matches/synchroniser/
    Récupère les fixtures TheSportsDB et les sauvegarde en base.
    ?date=YYYY-MM-DD → synchro du jour
    Sans paramètre   → saison complète de toutes les ligues configurées
    """
    permission_classes = [AllowAny]

    def post(self, request):
        date = request.query_params.get('date', None)
        matches = fetch_fixtures(date)

        count = 0
        for match_data in matches:
            if match_data.get('date_heure') is None:
                continue
            Match.objects.update_or_create(
                external_id=match_data['external_id'],
                defaults=match_data,
            )
            count += 1

        return Response({'status': 'ok', 'total': count})


class LivescoresView(APIView):
    """
    GET /api/livescores/
    Appelle TheSportsDB V2 livescores, met à jour les matchs live en base,
    et retourne uniquement les matchs actuellement en cours.
    """
    permission_classes = [AllowAny]

    def get(self, _request):
        updates = fetch_livescores()

        updated_ids = []
        for upd in updates:
            Match.objects.filter(external_id=upd['external_id']).update(
                statut=upd['statut'],
                score_a=upd['score_a'],
                score_b=upd['score_b'],
            )
            updated_ids.append(upd['external_id'])

        # Retourne live + matchs terminés mis à jour (le frontend les merge)
        live_statuts = ['1H', '2H', 'HT', 'ET', 'P', 'BT']
        finished_statuts = ['FT', 'AET', 'PEN']
        qs = Match.objects.filter(
            statut__in=live_statuts
        ) | Match.objects.filter(
            external_id__in=updated_ids,
            statut__in=finished_statuts,
        )
        return Response(MatchSerializer(qs.order_by('date_heure'), many=True).data)
