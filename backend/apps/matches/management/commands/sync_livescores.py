from datetime import timedelta, date

import requests
from django.core.management.base import BaseCommand
from django.utils import timezone

from apps.matches.models import Match
from apps.matches.sports_api import (
    API_V1, API_V2, LEAGUES, TIMEOUT,
    _key, _map_status, _parse_score,
    fetch_livescores,
)

_LIVE_STATUTS = ['1H', '2H', 'HT', 'ET', 'P', 'BT']


class Command(BaseCommand):
    help = 'Met à jour les scores live depuis TheSportsDB.'

    def add_arguments(self, parser):
        parser.add_argument(
            '--debug',
            action='store_true',
            help='Affiche le detail des appels API (URL, status HTTP, reponse brute)',
        )

    def handle(self, *args, **options):
        cutoff = timezone.now() - timedelta(hours=3)
        Match.objects.filter(statut__in=_LIVE_STATUTS, date_heure__lt=cutoff).update(statut='FT')

        if options['debug']:
            self._debug_run()
            return

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
        self.stdout.write(self.style.SUCCESS(f'{count} score(s) mis a jour.'))

    # ------------------------------------------------------------------
    # Mode diagnostic
    # ------------------------------------------------------------------

    def _debug_run(self):
        key = _key()
        tracked_ids = {cfg['id'] for cfg in LEAGUES}
        today = date.today().strftime('%Y-%m-%d')

        self.stdout.write(f'\n=== SPORTSDB_KEY = "{key}" ===')
        self.stdout.write(f'Ligues suivies : {sorted(tracked_ids)}\n')

        # 1. V2 livescores (premium)
        url = f'{API_V2}/livescore/all'
        self.stdout.write(f'[V2] GET {url}')
        try:
            r = requests.get(url, headers={'X-API-KEY': key}, timeout=TIMEOUT)
            self.stdout.write(f'  -> HTTP {r.status_code}')
            data = r.json()
            events = data.get('livescore') or []
            self.stdout.write(f'  -> {len(events)} evenement(s) live total')
            for e in events:
                lid = int(e.get('idLeague') or 0)
                tag = '[SUIVI]' if lid in tracked_ids else '[ignore]'
                ext_id = f'sdb_{e.get("idEvent", "?")}'
                in_db = Match.objects.filter(external_id=ext_id).exists()
                self.stdout.write(
                    f'  {tag} leagueId={lid} idEvent={e.get("idEvent")} '
                    f'status="{e.get("strStatus")}" '
                    f'score={e.get("intHomeScore")}-{e.get("intAwayScore")} '
                    f'inDB={in_db}'
                )
        except Exception as exc:
            self.stdout.write(f'  -> ERREUR V2 : {exc}')

        # 2. V1 eventsday par sport
        for sport_label in ['Soccer', 'Basketball', 'Ice Hockey', 'Rugby',
                             'American Football']:
            url = f'{API_V1}/{key}/eventsday.php?d={today}&s={sport_label}'
            self.stdout.write(f'\n[V1 {sport_label}] GET {url}')
            try:
                r = requests.get(url, timeout=TIMEOUT)
                self.stdout.write(f'  -> HTTP {r.status_code}')
                events = r.json().get('events') or []
                self.stdout.write(f'  -> {len(events)} evenement(s) total')
                for e in events:
                    lid = int(e.get('idLeague') or 0)
                    if lid not in tracked_ids:
                        continue
                    ext_id = f'sdb_{e.get("idEvent", "?")}'
                    in_db = Match.objects.filter(external_id=ext_id).exists()
                    statut_mappe = _map_status(e.get('strStatus', ''))
                    self.stdout.write(
                        f'  [SUIVI] leagueId={lid} idEvent={e.get("idEvent")} '
                        f'raw_status="{e.get("strStatus")}" -> mappe="{statut_mappe}" '
                        f'score={e.get("intHomeScore")}-{e.get("intAwayScore")} '
                        f'inDB={in_db} ext_id={ext_id}'
                    )
            except Exception as exc:
                self.stdout.write(f'  -> ERREUR V1 : {exc}')

        self.stdout.write('\n=== FIN DIAGNOSTIC ===')
