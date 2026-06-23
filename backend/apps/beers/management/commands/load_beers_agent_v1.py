from django.core.management.base import BaseCommand
from apps.beers.models import Beer

BEERS = [
    # ── ALBANIA ──────────────────────────────────────────────────────────────
    {'nom': 'Birra Tirana', 'brasserie': 'Birra Tirana', 'pays': 'albania', 'region': 'Tirana', 'equipe': '', 'style': 'Lager', 'description': "La bière historique de la capitale albanaise, une blonde légère et désaltérante.", 'degre_alcool': '4.2', 'image_url': '', 'generated_by': 'manual'},
    # ── ALGERIA ──────────────────────────────────────────────────────────────
    {'nom': 'Hamoud Boualem', 'brasserie': 'Hamoud Boualem', 'pays': 'algeria', 'region': 'Alger', 'equipe': '', 'style': 'Limonade', 'description': "La limonade emblématique d'Algérie depuis 1878, boisson nationale sans alcool très appréciée.", 'degre_alcool': '', 'image_url': '', 'generated_by': 'manual'},
    # ── ARGENTINA ────────────────────────────────────────────────────────────
    {'nom': 'Quilmes', 'brasserie': 'Cerveceria y Malteria Quilmes', 'pays': 'argentina', 'region': 'Buenos Aires', 'equipe': '', 'style': 'Lager', 'description': "La bière la plus consommée d'Argentine, une lager blonde aux couleurs du pays.", 'degre_alcool': '4.9', 'image_url': '', 'generated_by': 'manual'},
    # ── AUSTRALIA ────────────────────────────────────────────────────────────
    {'nom': 'Victoria Bitter', 'brasserie': 'Carlton and United Breweries', 'pays': 'australia', 'region': 'Melbourne', 'equipe': '', 'style': 'Lager', 'description': "Une lager australienne robuste, l'une des bières les plus vendues du pays.", 'degre_alcool': '4.9', 'image_url': '', 'generated_by': 'manual'},
    # ── AUSTRIA ──────────────────────────────────────────────────────────────
    {'nom': 'Stiegl Goldbräu', 'brasserie': 'Stieglbrauerei zu Salzburg', 'pays': 'austria', 'region': 'Salzbourg', 'equipe': '', 'style': 'Lager', 'description': "La bière phare de la plus ancienne brasserie privée d'Autriche, ronde et maltée.", 'degre_alcool': '4.9', 'image_url': '', 'generated_by': 'manual'},
    # ── BOLIVIA ──────────────────────────────────────────────────────────────
    {'nom': 'Paceña', 'brasserie': 'Cerveceria Boliviana Nacional', 'pays': 'bolivia', 'region': 'La Paz', 'equipe': '', 'style': 'Lager', 'description': "La bière nationale bolivienne, une blonde brassée en altitude à La Paz.", 'degre_alcool': '4.8', 'image_url': '', 'generated_by': 'manual'},
    # ── BRAZIL ───────────────────────────────────────────────────────────────
    {'nom': 'Brahma', 'brasserie': 'Ambev', 'pays': 'brazil', 'region': 'Rio de Janeiro', 'equipe': '', 'style': 'Lager', 'description': "Une des bières les plus populaires du Brésil, blonde et rafraîchissante.", 'degre_alcool': '4.8', 'image_url': '', 'generated_by': 'manual'},
    # ── CAMEROON ─────────────────────────────────────────────────────────────
    {'nom': '33 Export', 'brasserie': 'Brasseries du Cameroun', 'pays': 'cameroon', 'region': 'Douala', 'equipe': '', 'style': 'Lager', 'description': "Une lager légère très répandue au Cameroun et en Afrique centrale.", 'degre_alcool': '5.5', 'image_url': '', 'generated_by': 'manual'},
    # ── CHILE ────────────────────────────────────────────────────────────────
    {'nom': 'Cristal', 'brasserie': 'Compania Cervecerias Unidas', 'pays': 'chile', 'region': 'Santiago', 'equipe': '', 'style': 'Lager', 'description': "La bière blonde la plus vendue du Chili, légère et désaltérante.", 'degre_alcool': '4.6', 'image_url': '', 'generated_by': 'manual'},
    # ── COLOMBIA ─────────────────────────────────────────────────────────────
    {'nom': 'Águila', 'brasserie': 'Bavaria', 'pays': 'colombia', 'region': 'Barranquilla', 'equipe': '', 'style': 'Lager', 'description': "Une lager légère associée à la côte caraïbe colombienne.", 'degre_alcool': '4.0', 'image_url': '', 'generated_by': 'manual'},
    # ── COSTA RICA ───────────────────────────────────────────────────────────
    {'nom': 'Imperial', 'brasserie': 'Florida Ice and Farm Company', 'pays': 'costa rica', 'region': 'San José', 'equipe': '', 'style': 'Lager', 'description': "La bière nationale du Costa Rica, reconnaissable à son aigle noir.", 'degre_alcool': '4.6', 'image_url': '', 'generated_by': 'manual'},
    # ── CROATIA ──────────────────────────────────────────────────────────────
    {'nom': 'Ožujsko', 'brasserie': 'Zagrebacka pivovara', 'pays': 'croatia', 'region': 'Zagreb', 'equipe': '', 'style': 'Lager', 'description': "La bière croate la plus populaire, une blonde brassée à Zagreb.", 'degre_alcool': '5.0', 'image_url': '', 'generated_by': 'manual'},
    # ── DR CONGO ─────────────────────────────────────────────────────────────
    {'nom': 'Primus', 'brasserie': 'Bralima', 'pays': 'dr congo', 'region': 'Kinshasa', 'equipe': '', 'style': 'Lager', 'description': "La lager emblématique de la République démocratique du Congo.", 'degre_alcool': '5.0', 'image_url': '', 'generated_by': 'manual'},
    # ── ECUADOR ──────────────────────────────────────────────────────────────
    {'nom': 'Pilsener', 'brasserie': 'Cerveceria Nacional', 'pays': 'ecuador', 'region': 'Guayaquil', 'equipe': '', 'style': 'Lager', 'description': "La bière la plus consommée d'Équateur, blonde et légère.", 'degre_alcool': '4.2', 'image_url': '', 'generated_by': 'manual'},
    # ── EGYPT ────────────────────────────────────────────────────────────────
    {'nom': 'Stella', 'brasserie': 'Al Ahram Beverages Company', 'pays': 'egypt', 'region': 'Le Caire', 'equipe': '', 'style': 'Lager', 'description': "La plus ancienne bière d'Égypte, brassée depuis 1897, blonde et légère.", 'degre_alcool': '4.5', 'image_url': '', 'generated_by': 'manual'},
    # ── EL SALVADOR ──────────────────────────────────────────────────────────
    {'nom': 'Pilsener', 'brasserie': 'Industrias La Constancia', 'pays': 'el salvador', 'region': 'San Salvador', 'equipe': '', 'style': 'Lager', 'description': "La bière historique du Salvador, une blonde douce très répandue.", 'degre_alcool': '4.4', 'image_url': '', 'generated_by': 'manual'},
    # ── ETHIOPIA ─────────────────────────────────────────────────────────────
    {'nom': 'St. George', 'brasserie': 'BGI Ethiopia', 'pays': 'ethiopia', 'region': 'Addis-Abeba', 'equipe': '', 'style': 'Lager', 'description': "La plus ancienne bière d'Éthiopie, une lager dorée brassée depuis 1922.", 'degre_alcool': '5.0', 'image_url': '', 'generated_by': 'manual'},
    # ── GEORGIA ──────────────────────────────────────────────────────────────
    {'nom': 'Natakhtari', 'brasserie': 'Natakhtari Brewery', 'pays': 'georgia', 'region': 'Natakhtari', 'equipe': '', 'style': 'Lager', 'description': "Une bière géorgienne moderne très populaire, blonde et équilibrée.", 'degre_alcool': '5.0', 'image_url': '', 'generated_by': 'manual'},
    # ── GHANA ────────────────────────────────────────────────────────────────
    {'nom': 'Star', 'brasserie': 'Accra Brewery', 'pays': 'ghana', 'region': 'Accra', 'equipe': '', 'style': 'Lager', 'description': "La première lager brassée au Ghana, blonde et légère.", 'degre_alcool': '5.1', 'image_url': '', 'generated_by': 'manual'},
    # ── HAITI ────────────────────────────────────────────────────────────────
    {'nom': 'Prestige', 'brasserie': "Brasserie nationale d'Haïti", 'pays': 'haiti', 'region': 'Port-au-Prince', 'equipe': '', 'style': 'Lager', 'description': "La bière nationale haïtienne, blonde et légère, plusieurs fois primée.", 'degre_alcool': '5.0', 'image_url': '', 'generated_by': 'manual'},
    # ── HONDURAS ─────────────────────────────────────────────────────────────
    {'nom': 'Salva Vida', 'brasserie': 'Cerveceria Hondurena', 'pays': 'honduras', 'region': 'San Pedro Sula', 'equipe': '', 'style': 'Lager', 'description': "Une bière blonde douce, l'une des plus populaires du Honduras.", 'degre_alcool': '4.8', 'image_url': '', 'generated_by': 'manual'},
    # ── HUNGARY ──────────────────────────────────────────────────────────────
    {'nom': 'Dreher', 'brasserie': 'Dreher Sorgyarak', 'pays': 'hungary', 'region': 'Budapest', 'equipe': '', 'style': 'Lager', 'description': "Une lager hongroise historique au caractère malté.", 'degre_alcool': '5.2', 'image_url': '', 'generated_by': 'manual'},
    # ── INDONESIA ────────────────────────────────────────────────────────────
    {'nom': 'Bintang', 'brasserie': 'Multi Bintang Indonesia', 'pays': 'indonesia', 'region': 'Surabaya', 'equipe': '', 'style': 'Lager', 'description': "La bière blonde emblématique d'Indonésie, légère et rafraîchissante.", 'degre_alcool': '4.7', 'image_url': '', 'generated_by': 'manual'},
    # ── IRAN ─────────────────────────────────────────────────────────────────
    {'nom': 'Doogh', 'brasserie': 'Boisson traditionnelle', 'pays': 'iran', 'region': 'Téhéran', 'equipe': '', 'style': 'Boisson au yaourt', 'description': "Une boisson iranienne au yaourt fermenté, salée et parfumée à la menthe, servie bien fraîche.", 'degre_alcool': '', 'image_url': '', 'generated_by': 'manual'},
    # ── JAMAICA ──────────────────────────────────────────────────────────────
    {'nom': 'Red Stripe', 'brasserie': 'Desnoes and Geddes', 'pays': 'jamaica', 'region': 'Kingston', 'equipe': '', 'style': 'Lager', 'description': "La bière jamaïcaine la plus connue, une lager blonde à la bouteille trapue.", 'degre_alcool': '4.7', 'image_url': '', 'generated_by': 'manual'},
    # ── JAPAN ────────────────────────────────────────────────────────────────
    {'nom': 'Asahi Super Dry', 'brasserie': 'Asahi Breweries', 'pays': 'japan', 'region': 'Tokyo', 'equipe': '', 'style': 'Lager', 'description': "Une lager japonaise sèche et nette, très populaire dans le monde.", 'degre_alcool': '5.0', 'image_url': '', 'generated_by': 'manual'},
    # ── JORDAN ───────────────────────────────────────────────────────────────
    {'nom': 'Carakale', 'brasserie': 'Carakale Brewing Company', 'pays': 'jordan', 'region': 'Fuheis', 'equipe': '', 'style': 'Pale Ale', 'description': "La première microbrasserie de Jordanie, une bière artisanale houblonnée.", 'degre_alcool': '5.5', 'image_url': '', 'generated_by': 'manual'},
    # ── MALI ─────────────────────────────────────────────────────────────────
    {'nom': 'Dabileni', 'brasserie': 'Boisson traditionnelle', 'pays': 'mali', 'region': 'Bamako', 'equipe': '', 'style': "Boisson d'hibiscus", 'description': "Une boisson malienne à base de fleurs d'hibiscus infusées et sucrées, servie très fraîche.", 'degre_alcool': '', 'image_url': '', 'generated_by': 'manual'},
    # ── MEXICO ───────────────────────────────────────────────────────────────
    {'nom': 'Corona Extra', 'brasserie': 'Grupo Modelo', 'pays': 'mexico', 'region': 'Mexico', 'equipe': '', 'style': 'Lager', 'description': "La lager mexicaine la plus exportée au monde, légère et servie avec du citron vert.", 'degre_alcool': '4.5', 'image_url': '', 'generated_by': 'manual'},
    # ── MOROCCO ──────────────────────────────────────────────────────────────
    {'nom': 'Thé à la menthe', 'brasserie': 'Boisson nationale', 'pays': 'morocco', 'region': 'Marrakech', 'equipe': '', 'style': 'Infusion', 'description': "Le thé vert à la menthe sucré, boisson nationale et symbole de l'hospitalité marocaine.", 'degre_alcool': '', 'image_url': '', 'generated_by': 'manual'},
    # ── NIGERIA ──────────────────────────────────────────────────────────────
    {'nom': 'Star', 'brasserie': 'Nigerian Breweries', 'pays': 'nigeria', 'region': 'Lagos', 'equipe': '', 'style': 'Lager', 'description': "La première lager brassée au Nigéria, blonde et légère.", 'degre_alcool': '5.1', 'image_url': '', 'generated_by': 'manual'},
    # ── PANAMA ───────────────────────────────────────────────────────────────
    {'nom': 'Balboa', 'brasserie': 'Cerveceria Nacional de Panama', 'pays': 'panama', 'region': 'Panama', 'equipe': '', 'style': 'Lager', 'description': "Une bière blonde panaméenne classique, légère et désaltérante.", 'degre_alcool': '4.8', 'image_url': '', 'generated_by': 'manual'},
    # ── PARAGUAY ─────────────────────────────────────────────────────────────
    {'nom': 'Pilsen', 'brasserie': 'Cervepar', 'pays': 'paraguay', 'region': 'Asunción', 'equipe': '', 'style': 'Lager', 'description': "La bière la plus consommée du Paraguay, une blonde légère.", 'degre_alcool': '5.0', 'image_url': '', 'generated_by': 'manual'},
    # ── PERU ─────────────────────────────────────────────────────────────────
    {'nom': 'Cusqueña', 'brasserie': 'Backus', 'pays': 'peru', 'region': 'Cusco', 'equipe': '', 'style': 'Lager', 'description': "Une lager péruvienne premium brassée à partir de malt cultivé en altitude.", 'degre_alcool': '5.0', 'image_url': '', 'generated_by': 'manual'},
    # ── POLAND ───────────────────────────────────────────────────────────────
    {'nom': 'Żywiec', 'brasserie': 'Grupa Zywiec', 'pays': 'poland', 'region': 'Zywiec', 'equipe': '', 'style': 'Lager', 'description': "Une lager polonaise classique au caractère malté, brassée depuis 1856.", 'degre_alcool': '5.6', 'image_url': '', 'generated_by': 'manual'},
    # ── QATAR ────────────────────────────────────────────────────────────────
    {'nom': 'Karak', 'brasserie': 'Boisson traditionnelle', 'pays': 'qatar', 'region': 'Doha', 'equipe': '', 'style': 'Thé au lait épicé', 'description': "Le thé noir au lait et aux épices, boisson quotidienne incontournable au Qatar.", 'degre_alcool': '', 'image_url': '', 'generated_by': 'manual'},
    # ── SAUDI ARABIA ─────────────────────────────────────────────────────────
    {'nom': 'Vimto', 'brasserie': 'Aujan Industries', 'pays': 'saudi arabia', 'region': 'Djeddah', 'equipe': '', 'style': 'Cordial aux fruits', 'description': "Un sirop aux fruits rouges et épices, boisson incontournable des tables saoudiennes pendant le Ramadan.", 'degre_alcool': '', 'image_url': '', 'generated_by': 'manual'},
    # ── SENEGAL ──────────────────────────────────────────────────────────────
    {'nom': 'Gazelle', 'brasserie': "Brasseries de l'Ouest Africain", 'pays': 'senegal', 'region': 'Dakar', 'equipe': '', 'style': 'Lager', 'description': "La bière blonde nationale du Sénégal, légère et très répandue.", 'degre_alcool': '5.2', 'image_url': '', 'generated_by': 'manual'},
    # ── SERBIA ───────────────────────────────────────────────────────────────
    {'nom': 'Jelen', 'brasserie': 'Apatinska pivara', 'pays': 'serbia', 'region': 'Apatin', 'equipe': '', 'style': 'Lager', 'description': "La bière la plus vendue de Serbie, une blonde légère et populaire.", 'degre_alcool': '5.0', 'image_url': '', 'generated_by': 'manual'},
    # ── SLOVAKIA ─────────────────────────────────────────────────────────────
    {'nom': 'Zlatý Bažant', 'brasserie': 'Heineken Slovensko', 'pays': 'slovakia', 'region': 'Hurbanovo', 'equipe': '', 'style': 'Lager', 'description': "Le faisan doré, une lager slovaque emblématique au caractère doux.", 'degre_alcool': '5.0', 'image_url': '', 'generated_by': 'manual'},
    # ── SLOVENIA ─────────────────────────────────────────────────────────────
    {'nom': 'Laško Zlatorog', 'brasserie': 'Pivovarna Lasko', 'pays': 'slovenia', 'region': 'Lasko', 'equipe': '', 'style': 'Lager', 'description': "La bière slovène la plus connue, une blonde maltée brassée à Lasko.", 'degre_alcool': '4.9', 'image_url': '', 'generated_by': 'manual'},
    # ── SOUTH AFRICA ─────────────────────────────────────────────────────────
    {'nom': 'Castle Lager', 'brasserie': 'South African Breweries', 'pays': 'south africa', 'region': 'Johannesburg', 'equipe': '', 'style': 'Lager', 'description': "La bière historique d'Afrique du Sud, blonde et équilibrée depuis 1895.", 'degre_alcool': '5.0', 'image_url': '', 'generated_by': 'manual'},
    # ── SOUTH KOREA ──────────────────────────────────────────────────────────
    {'nom': 'Cass', 'brasserie': 'Oriental Brewery', 'pays': 'south korea', 'region': 'Séoul', 'equipe': '', 'style': 'Lager', 'description': "La lager la plus vendue de Corée du Sud, légère et très rafraîchissante.", 'degre_alcool': '4.5', 'image_url': '', 'generated_by': 'manual'},
    # ── SWITZERLAND ──────────────────────────────────────────────────────────
    {'nom': 'Feldschlösschen', 'brasserie': 'Feldschlosschen Brauerei', 'pays': 'switzerland', 'region': 'Rheinfelden', 'equipe': '', 'style': 'Lager', 'description': "La bière la plus vendue de Suisse, une lager blonde brassée à Rheinfelden.", 'degre_alcool': '4.8', 'image_url': '', 'generated_by': 'manual'},
    # ── TUNISIA ──────────────────────────────────────────────────────────────
    {'nom': 'Celtia', 'brasserie': 'Societe de Fabrication des Boissons de Tunisie', 'pays': 'tunisia', 'region': 'Tunis', 'equipe': '', 'style': 'Lager', 'description': "La bière nationale tunisienne, une blonde légère et désaltérante.", 'degre_alcool': '5.0', 'image_url': '', 'generated_by': 'manual'},
    # ── UKRAINE ──────────────────────────────────────────────────────────────
    {'nom': 'Obolon', 'brasserie': 'Obolon', 'pays': 'ukraine', 'region': 'Kiev', 'equipe': '', 'style': 'Lager', 'description': "La grande bière blonde ukrainienne, brassée à Kiev depuis 1980.", 'degre_alcool': '5.0', 'image_url': '', 'generated_by': 'manual'},
    # ── URUGUAY ──────────────────────────────────────────────────────────────
    {'nom': 'Pilsen', 'brasserie': 'Fabricas Nacionales de Cerveza', 'pays': 'uruguay', 'region': 'Montevideo', 'equipe': '', 'style': 'Lager', 'description': "Une des bières les plus anciennes et populaires d'Uruguay.", 'degre_alcool': '4.8', 'image_url': '', 'generated_by': 'manual'},
    # ── UZBEKISTAN ───────────────────────────────────────────────────────────
    {'nom': 'Sarbast', 'brasserie': 'Sarbast', 'pays': 'uzbekistan', 'region': 'Tachkent', 'equipe': '', 'style': 'Lager', 'description': "La bière blonde la plus connue d'Ouzbékistan, légère et populaire.", 'degre_alcool': '4.8', 'image_url': '', 'generated_by': 'manual'},
    # ── VENEZUELA ────────────────────────────────────────────────────────────
    {'nom': 'Polar', 'brasserie': 'Cerveceria Polar', 'pays': 'venezuela', 'region': 'Caracas', 'equipe': '', 'style': 'Lager', 'description': "La bière emblématique du Venezuela, une blonde très légère servie bien glacée.", 'degre_alcool': '4.5', 'image_url': '', 'generated_by': 'manual'},
]


class Command(BaseCommand):
    help = 'Charge les bières générées par agent pour 50 pays manquants (v1)'

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
