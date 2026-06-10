from django.core.management.base import BaseCommand
from apps.beers.models import Beer

BEERS = [
    # ── FRANCE ──────────────────────────────────────────────────────────────
    {
        'nom': 'Kronenbourg 1664',
        'brasserie': 'Brasseries Kronenbourg',
        'pays': 'france',
        'style': 'Lager',
        'description': "La bière alsacienne iconique, brassée depuis 1664 à Strasbourg. Légère et désaltérante avec des notes maltées douces.",
        'degre_alcool': 5.0,
        'ibu': 20,
        'volume': 330,
        'image_url': 'https://images.unsplash.com/photo-1608270586620-248524c67de9?w=800&q=80',
    },
    {
        'nom': 'Leffe Blonde',
        'brasserie': 'Abbaye de Leffe (AB InBev)',
        'pays': 'france',
        'style': 'Bière d\'abbaye',
        'description': "Bière d'abbaye blonde aux arômes fruités et épicés, avec une légère douceur maltée. Brassée selon une tradition séculaire.",
        'degre_alcool': 6.6,
        'ibu': 25,
        'volume': 330,
        'image_url': 'https://images.unsplash.com/photo-1535958636474-b021ee887b13?w=800&q=80',
    },
    # ── ANGLETERRE ──────────────────────────────────────────────────────────
    {
        'nom': 'Fuller\'s London Pride',
        'brasserie': 'Fuller, Smith & Turner',
        'pays': 'angleterre',
        'style': 'Bitter',
        'description': "L'ale emblématique de Londres depuis 1959. Equilibre parfait entre malts caramel et houblons floraux, avec une finale sèche et agréable.",
        'degre_alcool': 4.7,
        'ibu': 35,
        'volume': 500,
        'image_url': 'https://images.unsplash.com/photo-1566633806827-98b36f798880?w=800&q=80',
    },
    {
        'nom': 'Newcastle Brown Ale',
        'brasserie': 'Heineken UK',
        'pays': 'angleterre',
        'style': 'Brown Ale',
        'description': "La brown ale du Nord-Est de l'Angleterre, fondée à Newcastle en 1927. Couleur ambrée profonde, arômes de caramel et de noisette.",
        'degre_alcool': 4.7,
        'ibu': 18,
        'volume': 550,
        'image_url': 'https://images.unsplash.com/photo-1561642769-1e4614f9a9f4?w=800&q=80',
    },
    # ── ESPAGNE ─────────────────────────────────────────────────────────────
    {
        'nom': 'Estrella Damm',
        'brasserie': 'Damm',
        'pays': 'espagne',
        'style': 'Lager',
        'description': "La bière de Barcelone depuis 1876. Brassée avec du malt d'orge, riz et houblon, elle est légère, dorée et parfaitement rafraîchissante.",
        'degre_alcool': 5.4,
        'ibu': 20,
        'volume': 330,
        'image_url': 'https://images.unsplash.com/photo-1570598912132-0ba1dc952b7d?w=800&q=80',
    },
    # ── ALLEMAGNE ───────────────────────────────────────────────────────────
    {
        'nom': 'Weihenstephaner Hefeweissbier',
        'brasserie': 'Bayerische Staatsbrauerei Weihenstephan',
        'pays': 'allemagne',
        'style': 'Hefeweizen',
        'description': "La plus ancienne brasserie du monde en activité (1040). Une Hefeweizen bavaroise classique avec des arômes de banane et de clou de girofle.",
        'degre_alcool': 5.4,
        'ibu': 14,
        'volume': 500,
        'image_url': 'https://images.unsplash.com/photo-1558642891-54be180ea339?w=800&q=80',
    },
    {
        'nom': 'Paulaner Münchner Hell',
        'brasserie': 'Paulaner Brauerei',
        'pays': 'allemagne',
        'style': 'Helles Lager',
        'description': "La Münchner Hell de référence, brassée à Munich. Légère, maltée et équilibrée, elle est l'accompagnement idéal d'une bratwurst.",
        'degre_alcool': 4.9,
        'ibu': 17,
        'volume': 500,
        'image_url': 'https://images.unsplash.com/photo-1559526323-cb2f2fe2591b?w=800&q=80',
    },
    # ── ITALIE ──────────────────────────────────────────────────────────────
    {
        'nom': 'Peroni Nastro Azzurro',
        'brasserie': 'Birra Peroni',
        'pays': 'italie',
        'style': 'Lager Premium',
        'description': "La bière italienne la plus exportée. Brassée à Rome depuis 1963, elle est crisp, légère et rafraîchissante avec une amertume subtile.",
        'degre_alcool': 5.1,
        'ibu': 18,
        'volume': 330,
        'image_url': 'https://images.unsplash.com/photo-1547595628-c61a29f496f0?w=800&q=80',
    },
    # ── PORTUGAL ────────────────────────────────────────────────────────────
    {
        'nom': 'Super Bock',
        'brasserie': 'Super Bock Group',
        'pays': 'portugal',
        'style': 'Lager',
        'description': "La bière nationale portugaise depuis 1927. Légère et rafraîchissante, avec des notes maltées douces et une mousse crémeuse persistante.",
        'degre_alcool': 5.2,
        'ibu': 12,
        'volume': 330,
        'image_url': 'https://images.unsplash.com/photo-1527689368864-3a821dbccc34?w=800&q=80',
    },
    # ── PAYS-BAS ────────────────────────────────────────────────────────────
    {
        'nom': 'Heineken',
        'brasserie': 'Heineken International',
        'pays': 'pays-bas',
        'style': 'Pale Lager',
        'description': "Fondée à Amsterdam en 1873 par Gérard Heineken. Une lager internationale au goût équilibré entre malt et houblon, reconnue dans le monde entier.",
        'degre_alcool': 5.0,
        'ibu': 19,
        'volume': 330,
        'image_url': 'https://images.unsplash.com/photo-1574027542338-98e75acfd385?w=800&q=80',
    },
    # ── BELGIQUE ────────────────────────────────────────────────────────────
    {
        'nom': 'Duvel',
        'brasserie': 'Duvel Moortgat',
        'pays': 'belgique',
        'style': 'Belgian Strong Ale',
        'description': "Le 'diable' belge — une blonde forte brassée depuis 1871. Arômes fruités complexes d'agrumes et de poire, avec une effervescence vive et une finale sèche.",
        'degre_alcool': 8.5,
        'ibu': 32,
        'volume': 330,
        'image_url': 'https://images.unsplash.com/photo-1571767454098-246b94fbcf70?w=800&q=80',
    },
    # ── BRÉSIL ──────────────────────────────────────────────────────────────
    {
        'nom': 'Brahma Chopp',
        'brasserie': 'Ambev',
        'pays': 'brésil',
        'style': 'Pale Lager',
        'description': "L'une des bières les plus vendues du Brésil. Légère et dorée, brassée depuis 1888 à Rio de Janeiro, parfaite pour accompagner la feijoada.",
        'degre_alcool': 4.8,
        'ibu': 10,
        'volume': 350,
        'image_url': 'https://images.unsplash.com/photo-1561642769-1e4614f9a9f4?w=800&q=80',
    },
    # ── ARGENTINE ───────────────────────────────────────────────────────────
    {
        'nom': 'Quilmes',
        'brasserie': 'Cervecería y Maltería Quilmes',
        'pays': 'argentine',
        'style': 'Pale Lager',
        'description': "La bière nationale argentine depuis 1890. Crisp et légère, avec une amertume douce et des notes de grain, idéale avec un asado.",
        'degre_alcool': 4.9,
        'ibu': 12,
        'volume': 340,
        'image_url': 'https://images.unsplash.com/photo-1535958636474-b021ee887b13?w=800&q=80',
    },
    # ── MAROC ───────────────────────────────────────────────────────────────
    {
        'nom': 'Casablanca',
        'brasserie': 'Brasseries du Maroc',
        'pays': 'maroc',
        'style': 'Lager',
        'description': "La bière emblématique du Maroc, brassée à Casablanca depuis 1919. Légère et rafraîchissante, parfaitement adaptée au climat méditerranéen.",
        'degre_alcool': 5.0,
        'ibu': 14,
        'volume': 330,
        'image_url': 'https://images.unsplash.com/photo-1608270586620-248524c67de9?w=800&q=80',
    },
    # ── SÉNÉGAL ─────────────────────────────────────────────────────────────
    {
        'nom': 'Flag Spéciale',
        'brasserie': 'Grandes Brasseries Africaines',
        'pays': 'sénégal',
        'style': 'Pale Lager',
        'description': "La bière la plus populaire du Sénégal depuis 1969. Légère, dorée et désaltérante, elle accompagne parfaitement le thiéboudiène.",
        'degre_alcool': 5.6,
        'ibu': 15,
        'volume': 600,
        'image_url': 'https://images.unsplash.com/photo-1566633806827-98b36f798880?w=800&q=80',
    },
    # ── JAPON ───────────────────────────────────────────────────────────────
    {
        'nom': 'Sapporo Premium',
        'brasserie': 'Sapporo Breweries',
        'pays': 'japon',
        'style': 'Pale Lager',
        'description': "La plus ancienne brasserie du Japon fondée à Sapporo en 1876. Bière crisp et propre aux notes légères de malt, parfaite avec les sushis.",
        'degre_alcool': 4.9,
        'ibu': 18,
        'volume': 350,
        'image_url': 'https://images.unsplash.com/photo-1570598912132-0ba1dc952b7d?w=800&q=80',
    },
    # ── USA ─────────────────────────────────────────────────────────────────
    {
        'nom': 'Sierra Nevada Pale Ale',
        'brasserie': 'Sierra Nevada Brewing Co.',
        'pays': 'usa',
        'style': 'American Pale Ale',
        'description': "La pale ale qui a lancé la révolution craft américaine en 1980. Arômes prononcés de houblons Cascade : pamplemousse, pin et fleurs. Un classique.",
        'degre_alcool': 5.6,
        'ibu': 38,
        'volume': 355,
        'image_url': 'https://images.unsplash.com/photo-1558642891-54be180ea339?w=800&q=80',
    },
    # ── MEXIQUE ─────────────────────────────────────────────────────────────
    {
        'nom': 'Corona Extra',
        'brasserie': 'Grupo Modelo',
        'pays': 'mexique',
        'style': 'Pale Lager',
        'description': "La bière mexicaine la plus exportée dans le monde. Légère et pétillante, elle se déguste traditionnellement avec un quartier de citron vert.",
        'degre_alcool': 4.5,
        'ibu': 19,
        'volume': 355,
        'image_url': 'https://images.unsplash.com/photo-1527689368864-3a821dbccc34?w=800&q=80',
    },
    # ── CANADA ──────────────────────────────────────────────────────────────
    {
        'nom': 'Molson Canadian',
        'brasserie': 'Molson Coors',
        'pays': 'canada',
        'style': 'Lager',
        'description': "Fondée en 1786 à Montréal, Molson est la plus ancienne brasserie d'Amérique du Nord. La Canadian est légère, propre et revigorante comme l'air du Québec.",
        'degre_alcool': 5.0,
        'ibu': 15,
        'volume': 355,
        'image_url': 'https://images.unsplash.com/photo-1559526323-cb2f2fe2591b?w=800&q=80',
    },
    # ── AUSTRALIE ───────────────────────────────────────────────────────────
    {
        'nom': 'Victoria Bitter (VB)',
        'brasserie': 'Carlton & United Breweries',
        'pays': 'australie',
        'style': 'Pale Lager',
        'description': "L'icône australienne depuis 1854. La bière la plus vendue en Australie — légère, dorée, légèrement amère et rafraîchissante comme un barbie au bord de la plage.",
        'degre_alcool': 4.9,
        'ibu': 22,
        'volume': 375,
        'image_url': 'https://images.unsplash.com/photo-1574027542338-98e75acfd385?w=800&q=80',
    },
    # ── TURQUIE ─────────────────────────────────────────────────────────────
    {
        'nom': 'Efes Pilsen',
        'brasserie': 'Anadolu Efes',
        'pays': 'turquie',
        'style': 'Pilsner',
        'description': "La bière nationale turque depuis 1969, nommée d'après la cité antique d'Ephèse. Bière dorée et légère avec des notes florales de houblon.",
        'degre_alcool': 5.0,
        'ibu': 16,
        'volume': 500,
        'image_url': 'https://images.unsplash.com/photo-1547595628-c61a29f496f0?w=800&q=80',
    },
    # ── POLOGNE ─────────────────────────────────────────────────────────────
    {
        'nom': 'Żywiec',
        'brasserie': 'Browar Żywiec',
        'pays': 'pologne',
        'style': 'Pale Lager',
        'description': "La bière polonaise de référence depuis 1856, brassée dans les Carpates. Légère et maltée avec une amertume douce, parfaite avec le bigos traditionnel.",
        'degre_alcool': 5.6,
        'ibu': 16,
        'volume': 500,
        'image_url': 'https://images.unsplash.com/photo-1561642769-1e4614f9a9f4?w=800&q=80',
    },
    # ── CROATIE ─────────────────────────────────────────────────────────────
    {
        'nom': 'Ožujsko Pivo',
        'brasserie': 'Zagrebačka Pivovara',
        'pays': 'croatie',
        'style': 'Pale Lager',
        'description': "La bière croate numéro un depuis 1892, brassée à Zagreb. Son nom signifie 'bière de mars'. Légère, rafraîchissante, idéale en terrasse sur la côte dalmate.",
        'degre_alcool': 5.0,
        'ibu': 18,
        'volume': 500,
        'image_url': 'https://images.unsplash.com/photo-1571767454098-246b94fbcf70?w=800&q=80',
    },
]


class Command(BaseCommand):
    help = "Charge les bières en base (update_or_create sur le nom)"

    def handle(self, *args, **options):
        created_count = 0
        updated_count = 0

        for data in BEERS:
            nom = data.pop('nom')
            _, created = Beer.objects.update_or_create(
                nom=nom,
                defaults=data,
            )
            data['nom'] = nom  # restore for potential re-runs

            if created:
                created_count += 1
                self.stdout.write(self.style.SUCCESS(f"  ✓ Créée  : {nom}"))
            else:
                updated_count += 1
                self.stdout.write(f"  ~ Mise à jour : {nom}")

        self.stdout.write(
            self.style.SUCCESS(
                f"\n{created_count} bière(s) créée(s), {updated_count} mise(s) à jour. "
                f"Total en base : {Beer.objects.count()}"
            )
        )
