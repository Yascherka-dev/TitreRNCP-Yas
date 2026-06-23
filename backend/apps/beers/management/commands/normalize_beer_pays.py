from django.core.management.base import BaseCommand
from apps.beers.models import Beer

FIXES = {
    'angleterre': 'england',
    'allemagne':  'germany',
    'espagne':    'spain',
    'italie':     'italy',
    'pays-bas':   'netherlands',
    'belgique':   'belgium',
    'brésil':     'brazil',
    'argentine':  'argentina',
    'maroc':      'morocco',
    'sénégal':    'senegal',
    'japon':      'japan',
    'mexique':    'mexico',
    'australie':  'australia',
    'usa':        'united states',
}


class Command(BaseCommand):
    help = 'Normalise les pays des bières (noms FR → EN)'

    def handle(self, *args, **options):
        total = 0
        for fr, en in FIXES.items():
            n = Beer.objects.filter(pays=fr).update(pays=en)
            if n:
                self.stdout.write(f'  {fr} → {en} : {n} bière(s)')
                total += n
        self.stdout.write(self.style.SUCCESS(f'Done — {total} bière(s) mises à jour'))
