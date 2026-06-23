from django.core.management.base import BaseCommand
from apps.matches.sports_api import fetch_fixtures
from apps.matches.models import Match


class Command(BaseCommand):
    help = 'Synchronise les fixtures depuis TheSportsDB et les sauvegarde en base.'

    def add_arguments(self, parser):
        parser.add_argument('--date', type=str, default=None, help='YYYY-MM-DD')

    def handle(self, *args, **options):
        date = options.get('date')
        fixtures = fetch_fixtures(date)
        count = 0
        for data in fixtures:
            if data.get('date_heure') is None:
                continue
            Match.objects.update_or_create(
                external_id=data['external_id'],
                defaults=data,
            )
            count += 1
        self.stdout.write(self.style.SUCCESS(f'{count} match(s) synchronisé(s).'))
