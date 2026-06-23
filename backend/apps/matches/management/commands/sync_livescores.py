from datetime import timedelta

from django.core.management.base import BaseCommand
from django.utils import timezone

from apps.matches.models import Match
from apps.matches.sports_api import fetch_livescores

_LIVE_STATUTS = ['1H', '2H', 'HT', 'ET', 'P', 'BT']


class Command(BaseCommand):
    help = 'Met à jour les scores live depuis TheSportsDB.'

    def handle(self, *args, **options):
        cutoff = timezone.now() - timedelta(hours=3)
        Match.objects.filter(statut__in=_LIVE_STATUTS, date_heure__lt=cutoff).update(statut='FT')

        updates = fetch_livescores()
        count = 0
        for upd in updates:
            updated = Match.objects.filter(external_id=upd['external_id']).update(
                statut=upd['statut'],
                score_a=upd['score_a'],
                score_b=upd['score_b'],
            )
            if updated:
                count += 1
        self.stdout.write(self.style.SUCCESS(f'{count} score(s) mis à jour.'))
