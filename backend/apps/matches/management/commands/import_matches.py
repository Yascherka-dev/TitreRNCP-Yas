import requests
from django.core.management.base import BaseCommand
from django.conf import settings
from apps.matches.models import Match
from django.utils.dateparse import parse_datetime

FOOTBALL_LEAGUE_IDS = {2, 3, 39, 61, 78, 135, 140}
API_TIMEOUT = 10


class Command(BaseCommand):
    help = 'Importe les 50 prochains matchs football depuis l\'API'

    def handle(self, *args, **options):
        total = self._import_football()
        self.stdout.write(self.style.SUCCESS(f'{total} matchs importés/mis à jour'))

    def _import_football(self):
        self.stdout.write('Récupération football...')
        try:
            r = requests.get(
                'https://v3.football.api-sports.io/fixtures',
                headers={'x-apisports-key': settings.API_FOOTBALL_KEY},
                params={'next': 50},
                timeout=API_TIMEOUT
            )
            fixtures = r.json().get('response', [])
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'Erreur football: {e}'))
            return 0

        count = 0
        for f in fixtures:
            if f.get('league', {}).get('id') not in FOOTBALL_LEAGUE_IDS:
                continue
            fixture = f.get('fixture', {})
            teams = f.get('teams', {})
            league = f.get('league', {})
            goals = f.get('goals', {})

            Match.objects.update_or_create(
                external_id=f'football_{fixture.get("id")}',
                defaults={
                    'sport': 'football',
                    'competition': league.get('name', ''),
                    'equipe_a': teams.get('home', {}).get('name', ''),
                    'equipe_b': teams.get('away', {}).get('name', ''),
                    'pays_a': teams.get('home', {}).get('country', '').lower(),
                    'pays_b': teams.get('away', {}).get('country', '').lower(),
                    'date_heure': parse_datetime(fixture.get('date', '')),
                    'statut': fixture.get('status', {}).get('short', 'NS'),
                    'score_a': goals.get('home'),
                    'score_b': goals.get('away'),
                    'logo_a': teams.get('home', {}).get('logo', ''),
                    'logo_b': teams.get('away', {}).get('logo', ''),
                }
            )
            count += 1
        self.stdout.write(f'  Football: {count} matchs')
        return count
