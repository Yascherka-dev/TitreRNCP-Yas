from django.core.management.base import BaseCommand
from apps.beers.models import Beer

BEERS = [
    # ── BRAZIL ──────────────────────────────────────────────────────────────
    {
        'nom': 'Brahma',
        'brasserie': 'Ambev',
        'pays': 'brazil',
        'region': 'São Paulo',
        'equipe': '',
        'style': 'Lager',
        'description': 'La bière blonde légère et rafraîchissante emblématique du Brésil. Incontournable dans les bars et sur les plages de Rio.',
        'degre_alcool': '4.8',
        'image_url': '',
        'generated_by': 'manual',
    },
    # ── ARGENTINA ────────────────────────────────────────────────────────────
    {
        'nom': 'Quilmes',
        'brasserie': 'Quilmes Industrial',
        'pays': 'argentina',
        'region': 'Buenos Aires',
        'equipe': '',
        'style': 'Lager',
        'description': 'La bière nationale argentine, blonde et légère. Rituellement associée à l\'asado et aux matchs de football.',
        'degre_alcool': '4.9',
        'image_url': '',
        'generated_by': 'manual',
    },
    # ── MEXICO ────────────────────────────────────────────────────────────────
    {
        'nom': 'Corona Extra',
        'brasserie': 'Grupo Modelo',
        'pays': 'mexico',
        'region': 'Mexico City',
        'equipe': '',
        'style': 'Pale Lager',
        'description': 'La bière mexicaine la plus exportée dans le monde. Se boit traditionnellement avec une rondelle de citron vert.',
        'degre_alcool': '4.6',
        'image_url': '',
        'generated_by': 'manual',
    },
    # ── UNITED STATES ────────────────────────────────────────────────────────
    {
        'nom': 'Sierra Nevada Pale Ale',
        'brasserie': 'Sierra Nevada Brewing Co.',
        'pays': 'united states',
        'region': 'California',
        'equipe': '',
        'style': 'American Pale Ale',
        'description': 'Pionnière de la craft beer américaine depuis 1980. Notes d\'agrumes et de résine de houblon Cascade — l\'APA qui a tout changé.',
        'degre_alcool': '5.6',
        'image_url': '',
        'generated_by': 'manual',
    },
    # ── CANADA ────────────────────────────────────────────────────────────────
    {
        'nom': 'Molson Canadian',
        'brasserie': 'Molson Coors',
        'pays': 'canada',
        'region': 'Ontario',
        'equipe': '',
        'style': 'Lager',
        'description': 'La bière canadienne par excellence depuis 1959. Légère, propre, symbole de la fierté nationale.',
        'degre_alcool': '5.0',
        'image_url': '',
        'generated_by': 'manual',
    },
    # ── COLOMBIA ──────────────────────────────────────────────────────────────
    {
        'nom': 'Club Colombia',
        'brasserie': 'Bavaria SABMiller',
        'pays': 'colombia',
        'region': 'Bogotá',
        'equipe': '',
        'style': 'Märzen',
        'description': 'La bière premium de Colombie, brassée selon des recettes bavaroises. Dorée, équilibrée, très populaire pour les occasions festives.',
        'degre_alcool': '4.7',
        'image_url': '',
        'generated_by': 'manual',
    },
    # ── URUGUAY ───────────────────────────────────────────────────────────────
    {
        'nom': 'Patricia',
        'brasserie': 'Fábricas Nacionales de Cerveza',
        'pays': 'uruguay',
        'region': 'Montevideo',
        'equipe': '',
        'style': 'Pale Lager',
        'description': 'La bière nationale uruguayenne depuis 1894. Légère et pétillante, incontournable dans les bars de Montevideo.',
        'degre_alcool': '4.8',
        'image_url': '',
        'generated_by': 'manual',
    },
    # ── ECUADOR ───────────────────────────────────────────────────────────────
    {
        'nom': 'Club Verde',
        'brasserie': 'Cervecería Nacional',
        'pays': 'ecuador',
        'region': 'Guayaquil',
        'equipe': '',
        'style': 'Pale Lager',
        'description': 'La bière blonde incontournable d\'Équateur, brassée depuis 1887 à Guayaquil. Fraîche et légère, idéale sous le soleil équatorial.',
        'degre_alcool': '4.7',
        'image_url': '',
        'generated_by': 'manual',
    },
    # ── MOROCCO ───────────────────────────────────────────────────────────────
    {
        'nom': 'Casablanca',
        'brasserie': 'Société de Brasseries du Maroc (SBM)',
        'pays': 'morocco',
        'region': 'Casablanca',
        'equipe': '',
        'style': 'Pale Lager',
        'description': 'La bière emblématique du Maroc depuis 1919. Blonde, légère et rafraîchissante, brassée dans la métropole économique du pays.',
        'degre_alcool': '5.0',
        'image_url': '',
        'generated_by': 'manual',
    },
    # ── SENEGAL ───────────────────────────────────────────────────────────────
    {
        'nom': 'Flag Special',
        'brasserie': 'Brasseries du Sénégal (Gazelle)',
        'pays': 'senegal',
        'region': 'Dakar',
        'equipe': '',
        'style': 'Pale Lager',
        'description': 'La bière blonde locale de Dakar, légère et désaltérante. À consommer bien fraîche avec du thiéboudienne.',
        'degre_alcool': '4.9',
        'image_url': '',
        'generated_by': 'manual',
    },
    # ── NIGERIA ───────────────────────────────────────────────────────────────
    {
        'nom': 'Star Lager',
        'brasserie': 'Nigerian Breweries (Heineken)',
        'pays': 'nigeria',
        'region': 'Lagos',
        'equipe': '',
        'style': 'Pale Lager',
        'description': 'La bière la plus populaire du Nigeria depuis 1949. Blonde, légère et rafraîchissante, fidèle compagne du Jollof Rice.',
        'degre_alcool': '5.1',
        'image_url': '',
        'generated_by': 'manual',
    },
    # ── EGYPT ─────────────────────────────────────────────────────────────────
    {
        'nom': 'Sakara Gold',
        'brasserie': 'Al Ahram Beverages',
        'pays': 'egypt',
        'region': 'Le Caire',
        'equipe': '',
        'style': 'Lager',
        'description': 'La bière premium égyptienne au goût doux et équilibré. Nommée d\'après le site archéologique de Saqqara.',
        'degre_alcool': '5.0',
        'image_url': '',
        'generated_by': 'manual',
    },
    # ── CAMEROON ──────────────────────────────────────────────────────────────
    {
        'nom': '33 Export',
        'brasserie': 'Brasseries du Cameroun (SABC)',
        'pays': 'cameroon',
        'region': 'Douala',
        'equipe': '',
        'style': 'Pale Lager',
        'description': 'La bière blonde camerounaise par excellence, légère et facile à boire. Très populaire dans toute l\'Afrique centrale.',
        'degre_alcool': '4.8',
        'image_url': '',
        'generated_by': 'manual',
    },
    # ── SOUTH AFRICA ──────────────────────────────────────────────────────────
    {
        'nom': 'Castle Lager',
        'brasserie': 'South African Breweries (AB InBev)',
        'pays': 'south africa',
        'region': 'Johannesburg',
        'equipe': '',
        'style': 'Pale Lager',
        'description': 'La bière nationale sud-africaine depuis 1895. Blonde, légère et symbole de la Rainbow Nation.',
        'degre_alcool': '5.0',
        'image_url': '',
        'generated_by': 'manual',
    },
    # ── ALGERIA ───────────────────────────────────────────────────────────────
    {
        'nom': 'Tango',
        'brasserie': 'SPA (Société de Production Alimentaire)',
        'pays': 'algeria',
        'region': 'Alger',
        'equipe': '',
        'style': 'Lager',
        'description': 'La bière algérienne la plus connue. Douce et légèrement houblonnée, brassée localement depuis des décennies.',
        'degre_alcool': '4.8',
        'image_url': '',
        'generated_by': 'manual',
    },
    # ── IVORY COAST ───────────────────────────────────────────────────────────
    {
        'nom': 'Bock Ivoire',
        'brasserie': 'Brasseries d\'Abidjan (SOLIBRA)',
        'pays': 'ivory coast',
        'region': 'Abidjan',
        'equipe': '',
        'style': 'Pale Lager',
        'description': 'La bière emblématique de Côte d\'Ivoire, légère et rafraîchissante. Compagne incontournable de l\'attiéké au poisson braisé.',
        'degre_alcool': '5.0',
        'image_url': '',
        'generated_by': 'manual',
    },
    # ── GHANA ─────────────────────────────────────────────────────────────────
    {
        'nom': 'Club Beer',
        'brasserie': 'Accra Brewery (ABL)',
        'pays': 'ghana',
        'region': 'Accra',
        'equipe': '',
        'style': 'Pale Lager',
        'description': 'La bière blonde du Ghana depuis 1931. Légère, fraîche et symbole de convivialité dans les bars d\'Accra.',
        'degre_alcool': '5.0',
        'image_url': '',
        'generated_by': 'manual',
    },
    # ── JAPAN ─────────────────────────────────────────────────────────────────
    {
        'nom': 'Sapporo Black Label',
        'brasserie': 'Sapporo Breweries',
        'pays': 'japan',
        'region': 'Hokkaido',
        'equipe': '',
        'style': 'Pale Lager',
        'description': 'La plus ancienne brasserie du Japon fondée en 1876 à Sapporo. Lager propre et équilibrée, notes de malt doux.',
        'degre_alcool': '5.0',
        'image_url': '',
        'generated_by': 'manual',
    },
    # ── SOUTH KOREA ───────────────────────────────────────────────────────────
    {
        'nom': 'Hite Extra Cold',
        'brasserie': 'HITE-Jinro',
        'pays': 'south korea',
        'region': 'Séoul',
        'equipe': '',
        'style': 'Pale Lager',
        'description': 'La bière coréenne la plus populaire, ultra-filtrée pour une fraîcheur maximale. Idéale avec le bibimbap et les barbecues coréens.',
        'degre_alcool': '4.5',
        'image_url': '',
        'generated_by': 'manual',
    },
    # ── IRAN ──────────────────────────────────────────────────────────────────
    {
        'nom': 'Delster Malt (sans alcool)',
        'brasserie': 'Iran Bahnoosh',
        'pays': 'iran',
        'region': 'Téhéran',
        'equipe': '',
        'style': 'Malt sans alcool',
        'description': 'La boisson maltée pétillante iranienne sans alcool, aux saveurs de pêche ou d\'ananas. Alternative festive très populaire en Iran.',
        'degre_alcool': '0.0',
        'image_url': '',
        'generated_by': 'manual',
    },
    # ── AUSTRALIA ─────────────────────────────────────────────────────────────
    {
        'nom': 'Victoria Bitter (VB)',
        'brasserie': 'Carlton & United Breweries',
        'pays': 'australia',
        'region': 'Melbourne',
        'equipe': '',
        'style': 'Pale Lager',
        'description': 'La bière australienne la plus vendue depuis 1958. Légèrement amère, désaltérante — l\'incontournable du barbecue australien.',
        'degre_alcool': '4.9',
        'image_url': '',
        'generated_by': 'manual',
    },
    # ── SAUDI ARABIA ──────────────────────────────────────────────────────────
    {
        'nom': 'Barbican Malt (sans alcool)',
        'brasserie': 'Bass Brewers / AB InBev',
        'pays': 'saudi arabia',
        'region': 'Riyad',
        'equipe': '',
        'style': 'Malt sans alcool',
        'description': 'Boisson maltée pétillante sans alcool, très appréciée dans les pays du Golfe. Notes de malt, de caramel et léger fruité.',
        'degre_alcool': '0.0',
        'image_url': '',
        'generated_by': 'manual',
    },
    # ── CROATIA ───────────────────────────────────────────────────────────────
    {
        'nom': 'Ožujsko Pivo',
        'brasserie': 'Zagrebačka pivovara (Heineken)',
        'pays': 'croatia',
        'region': 'Zagreb',
        'equipe': '',
        'style': 'Pale Lager',
        'description': 'La bière nationale croate la plus vendue depuis 1892. Légère et dorée, elle accompagne les cevapi dans tous les bars de Zagreb.',
        'degre_alcool': '5.0',
        'image_url': '',
        'generated_by': 'manual',
    },
]


class Command(BaseCommand):
    help = 'Charge les bières Coupe du Monde 2026 (23 pays)'

    def handle(self, *args, **options):
        created, updated = 0, 0
        for data in BEERS:
            obj, was_created = Beer.objects.update_or_create(
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
