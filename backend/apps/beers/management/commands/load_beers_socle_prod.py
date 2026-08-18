"""
Bières manquantes pour la production.

Deux trous distincts, mesurés sur les 274 matchs à venir :

- Cinq pays n'avaient aucune bière (Norvège, Bulgarie, Grèce, Israël,
  Azerbaïdjan) : la carte sortait vide d'un côté.
- Les États-Unis et la France n'en avaient qu'une chacun, pour 155 et 105
  matchs domestiques : les deux camps recevaient forcément la même.

Les bières américaines sont enregistrées sous 'united states', pas 'usa' —
_pick_beer applique ce repli via _FR_TO_EN. Ne pas changer cette clé.
"""

from django.core.management.base import BaseCommand
from apps.beers.models import Beer

BEERS = [
    # ── ÉTATS-UNIS — 155 matchs domestiques, une seule bière en base ─────────
    {'nom': 'Brooklyn Lager', 'brasserie': 'Brooklyn Brewery', 'pays': 'united states',
     'region': 'New York', 'equipe': '', 'style': 'Amber Lager', 'degre_alcool': '5.2',
     'description': "Lager ambrée new-yorkaise au houblonnage à cru, note caramel et finale sèche.",
     'image_url': ''},
    {'nom': 'Anchor Steam Beer', 'brasserie': 'Anchor Brewing', 'pays': 'united states',
     'region': 'San Francisco', 'equipe': '', 'style': 'California Common', 'degre_alcool': '4.9',
     'description': "Le style californien historique : fermentation haute conduite à température de lager, malt grillé et amertume franche.",
     'image_url': ''},
    {'nom': 'Samuel Adams Boston Lager', 'brasserie': 'Boston Beer Company', 'pays': 'united states',
     'region': 'Boston', 'equipe': '', 'style': 'Vienna Lager', 'degre_alcool': '5.0',
     'description': "Lager viennoise de Nouvelle-Angleterre, malt riche équilibré par des houblons nobles allemands.",
     'image_url': ''},

    # ── FRANCE — 105 matchs domestiques, une seule bière en base ─────────────
    {'nom': 'Jenlain Ambrée', 'brasserie': 'Brasserie Duyck', 'pays': 'france',
     'region': 'Nord', 'equipe': '', 'style': 'Bière de garde', 'degre_alcool': '7.5',
     'description': "La bière de garde du Nord, ambrée et maltée, longtemps servie en bouteille champenoise.",
     'image_url': ''},
    {'nom': 'Pelforth Brune', 'brasserie': 'Pelforth', 'pays': 'france',
     'region': 'Nord', 'equipe': '', 'style': 'Brune', 'degre_alcool': '6.5',
     'description': "Brune lilloise aux malts torréfiés, notes de café et de caramel, amertume discrète.",
     'image_url': ''},
    {'nom': '3 Monts', 'brasserie': 'Brasserie de Saint-Sylvestre', 'pays': 'france',
     'region': 'Flandre', 'equipe': '', 'style': 'Bière de garde blonde', 'degre_alcool': '8.5',
     'description': "Blonde flamande puissante et sèche, refermentée en bouteille, finale poivrée.",
     'image_url': ''},

    # ── NORVÈGE — aucune bière ──────────────────────────────────────────────
    {'nom': 'Ringnes Pilsner', 'brasserie': 'Ringnes', 'pays': 'norway',
     'region': 'Oslo', 'equipe': '', 'style': 'Pilsner', 'degre_alcool': '4.7',
     'description': "La pilsner la plus répandue de Norvège, claire et désaltérante, amertume légère.",
     'image_url': ''},
    {'nom': 'Aass Bock', 'brasserie': 'Aass Bryggeri', 'pays': 'norway',
     'region': 'Drammen', 'equipe': '', 'style': 'Bock', 'degre_alcool': '6.5',
     'description': "Bock de la plus ancienne brasserie norvégienne, malt foncé et douceur caramélisée.",
     'image_url': ''},

    # ── BULGARIE — aucune bière ─────────────────────────────────────────────
    {'nom': 'Zagorka', 'brasserie': 'Zagorka AD', 'pays': 'bulgaria',
     'region': 'Stara Zagora', 'equipe': '', 'style': 'Lager', 'degre_alcool': '5.0',
     'description': "Lager bulgare classique, maltée et douce, la plus consommée du pays.",
     'image_url': ''},
    {'nom': 'Kamenitza', 'brasserie': 'Kamenitza AD', 'pays': 'bulgaria',
     'region': 'Plovdiv', 'equipe': '', 'style': 'Pale Lager', 'degre_alcool': '4.4',
     'description': "La doyenne des brasseries bulgares : blonde légère, finale nette.",
     'image_url': ''},

    # ── GRÈCE — aucune bière ────────────────────────────────────────────────
    {'nom': 'Mythos', 'brasserie': 'Mythos Brewery', 'pays': 'greece',
     'region': 'Thessalonique', 'equipe': '', 'style': 'Lager', 'degre_alcool': '5.0',
     'description': "Lager grecque légère et rafraîchissante, l'accompagnement habituel des mezze.",
     'image_url': ''},
    {'nom': 'Fix Hellas', 'brasserie': 'Olympic Brewery', 'pays': 'greece',
     'region': 'Athènes', 'equipe': '', 'style': 'Pale Lager', 'degre_alcool': '5.0',
     'description': "La plus ancienne marque de bière grecque, blonde sèche à l'amertume mesurée.",
     'image_url': ''},

    # ── ISRAËL — aucune bière ───────────────────────────────────────────────
    {'nom': 'Goldstar', 'brasserie': 'Tempo Beer Industries', 'pays': 'israel',
     'region': 'Netanya', 'equipe': '', 'style': 'Dark Lager', 'degre_alcool': '4.9',
     'description': "Lager ambrée israélienne, malt torréfié léger et finale douce-amère.",
     'image_url': ''},
    {'nom': 'Maccabee', 'brasserie': 'Tempo Beer Industries', 'pays': 'israel',
     'region': 'Netanya', 'equipe': '', 'style': 'Pale Lager', 'degre_alcool': '4.9',
     'description': "Blonde légère et sèche, longtemps la bière d'exportation du pays.",
     'image_url': ''},

    # ── AZERBAÏDJAN — aucune bière ──────────────────────────────────────────
    {'nom': 'Xırdalan', 'brasserie': 'Baki-Kastel', 'pays': 'azerbaijan',
     'region': 'Bakou', 'equipe': '', 'style': 'Lager', 'degre_alcool': '4.5',
     'description': "La bière la plus vendue d'Azerbaïdjan, blonde souple et peu amère.",
     'image_url': ''},
    {'nom': 'NZS Original', 'brasserie': 'Naxçıvan Brewery', 'pays': 'azerbaijan',
     'region': 'Naxçıvan', 'equipe': '', 'style': 'Pale Lager', 'degre_alcool': '4.8',
     'description': "Blonde du Nakhitchevan, céréalière et sèche, brassée à l'eau de montagne.",
     'image_url': ''},
]


class Command(BaseCommand):
    help = "Bières des pays sans couverture, et variété pour les ligues domestiques"

    def handle(self, *args, **options):
        created, updated = 0, 0
        for data in BEERS:
            _, was_created = Beer.objects.update_or_create(
                nom=data['nom'],
                pays=data['pays'],
                defaults=data,
            )
            if was_created:
                created += 1
            else:
                updated += 1
        self.stdout.write(self.style.SUCCESS(
            f'Done — {created} created, {updated} updated ({created + updated} total)'
        ))
