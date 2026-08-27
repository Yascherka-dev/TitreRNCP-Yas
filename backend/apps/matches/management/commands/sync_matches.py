from datetime import timedelta

from django.core.management.base import BaseCommand
from django.utils import timezone

from apps.matches.sports_api import fetch_fixtures
from apps.matches.models import Match
from apps.references import purge_dead_references

# Fenêtre conservée en base — alignée sur ce qu'affiche MatchListView (J-30 / J+60).
# Tout ce qui est hors fenêtre est invisible dans l'app : inutile de le stocker.
WINDOW_PAST_DAYS = 30
WINDOW_FUTURE_DAYS = 60


class Command(BaseCommand):
    help = 'Synchronise les fixtures TheSportsDB dans la fenêtre J-30/J+60 et purge le reste.'

    def add_arguments(self, parser):
        parser.add_argument('--date', type=str, default=None, help='YYYY-MM-DD (jour ciblé)')
        parser.add_argument('--no-purge', action='store_true',
                            help='Ne pas supprimer les matchs hors fenêtre.')

    def handle(self, *args, **options):
        date = options.get('date')
        today = timezone.now().date()
        start = today - timedelta(days=WINDOW_PAST_DAYS)
        end = today + timedelta(days=WINDOW_FUTURE_DAYS)

        fixtures = fetch_fixtures(date)

        count = skipped = 0
        for data in fixtures:
            dt = data.get('date_heure')
            if dt is None:
                continue
            # On n'écrit que les matchs de la fenêtre affichée
            if not (start <= dt.date() <= end):
                skipped += 1
                continue
            Match.objects.update_or_create(
                external_id=data['external_id'],
                defaults=data,
            )
            count += 1

        self.stdout.write(self.style.SUCCESS(
            f'{count} match(s) synchronisé(s) dans la fenêtre '
            f'[{start} → {end}] ({skipped} hors fenêtre ignoré(s)).'
        ))

        # Purge des matchs hors fenêtre (désactivée si on cible un jour précis)
        if not date and not options.get('no_purge'):
            purged, _ = Match.objects.exclude(
                date_heure__date__gte=start,
                date_heure__date__lte=end,
            ).delete()
            self.stdout.write(self.style.WARNING(f'{purged} match(s) hors fenêtre purgé(s).'))

            # Les favoris visant ces matchs viennent de perdre leur cible.
            # Aucune clé étrangère ne les supprime : on s'en charge ici.
            morts = purge_dead_references()
            total = sum(morts.values())
            if total:
                detail = ', '.join(f'{n} {libelle}' for libelle, n in morts.items() if n)
                self.stdout.write(self.style.WARNING(
                    f'{total} référence(s) devenue(s) orpheline(s) supprimée(s) : {detail}.'
                ))
