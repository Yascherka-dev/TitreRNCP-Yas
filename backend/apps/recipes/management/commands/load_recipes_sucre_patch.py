"""
Patch sucré : recettes sucrées pour les pays qui n'en avaient pas.
Priorité : England (et autres pays européens présents à la WC 2026).
"""
from django.core.management.base import BaseCommand
from apps.recipes.models import Recipe

RECIPES = [
    # ── ENGLAND ──────────────────────────────────────────────────────────────
    {
        'titre': 'Sticky Toffee Pudding',
        'pays': 'england',
        'type_plat': 'sucré',
        'description': 'Le dessert britannique par excellence : gâteau moelleux aux dattes nappé d\'une sauce toffee au beurre chaude.',
        'temps_preparation': 20, 'temps_cuisson': 35, 'nb_personnes': 6, 'difficulte': 'Moyen',
        'ingredients': ['200 g de dattes dénoyautées', '200 ml d\'eau bouillante', '1 c. de bicarbonate',
                        '180 g de farine', '150 g de sucre', '2 œufs', '80 g de beurre mou',
                        '200 ml de crème liquide', '150 g de cassonade', '50 g de beurre (sauce)', '1 c. de vanille'],
        'etapes': ['Verser l\'eau bouillante sur les dattes avec le bicarbonate. Laisser 10 min puis mixer.',
                   'Battre beurre et sucre. Ajouter œufs, farine et purée de dattes.',
                   'Cuire dans un moule beurré 30–35 min à 180°C.',
                   'Préparer la sauce toffee : beurre, cassonade, crème et vanille. Faire fondre et mijoter 3 min.',
                   'Piquer le gâteau chaud, napper généreusement de sauce toffee. Servir chaud.'],
        'tags': ['Pub', 'Dessert', 'Toffee', 'Réconfort'],
        'image_url': 'https://upload.wikimedia.org/wikipedia/commons/thumb/b/b1/Sticky_toffee_pudding.jpg/800px-Sticky_toffee_pudding.jpg',
    },
    {
        'titre': 'Eton Mess',
        'pays': 'england',
        'type_plat': 'sucré',
        'description': 'Dessert estival anglais né à Eton : fraises fraîches, meringue craquante et crème fouettée, mélangés en vrac.',
        'temps_preparation': 15, 'temps_cuisson': 0, 'nb_personnes': 4, 'difficulte': 'Facile',
        'ingredients': ['500 g de fraises', '300 ml de crème entière', '4 meringues du commerce (ou maison)',
                        '2 c. de sucre glace', '1 c. d\'extrait de vanille'],
        'etapes': ['Laver et couper les fraises en morceaux. Écraser grossièrement la moitié avec une fourchette.',
                   'Fouetter la crème avec le sucre glace et la vanille jusqu\'à consistance ferme.',
                   'Briser grossièrement les meringues en morceaux irréguliers.',
                   'Mélanger fraises entières, fraises écrasées, meringue et crème dans un grand bol.',
                   'Servir immédiatement dans des verres transparents.'],
        'tags': ['Été', 'Fraise', 'Meringue', 'Eton'],
        'image_url': 'https://upload.wikimedia.org/wikipedia/commons/thumb/8/81/Eton_Mess.jpg/800px-Eton_Mess.jpg',
    },
    # ── GERMANY ──────────────────────────────────────────────────────────────
    {
        'titre': 'Schwarzwälder Kirschtorte',
        'pays': 'germany',
        'type_plat': 'sucré',
        'description': 'La forêt-noire allemande originale : génoise au cacao, chantilly, cerises griottines et kirsch.',
        'temps_preparation': 45, 'temps_cuisson': 30, 'nb_personnes': 10, 'difficulte': 'Difficile',
        'ingredients': ['4 œufs', '120 g de sucre', '80 g de farine', '40 g de cacao',
                        '500 ml de crème entière', '400 g de cerises griottines', '50 ml de kirsch',
                        '100 g de chocolat noir (copeaux)'],
        'etapes': ['Battre œufs et sucre au bain-marie jusqu\'à ruban. Incorporer farine et cacao tamisés.',
                   'Cuire en moule beurré 25–30 min à 180°C. Laisser refroidir.',
                   'Couper en 3 disques. Imbiber chaque disque de kirsch.',
                   'Monter la chantilly ferme.',
                   'Alterner disques de génoise, chantilly et cerises. Couvrir de chantilly et décorer de copeaux de chocolat.'],
        'tags': ['Forêt-Noire', 'Chocolat', 'Kirsch', 'Gâteau'],
        'image_url': 'https://upload.wikimedia.org/wikipedia/commons/thumb/b/b3/Schwarzw%C3%A4lder_Kirschtorte_2009.jpg/800px-Schwarzw%C3%A4lder_Kirschtorte_2009.jpg',
    },
    # ── SPAIN ────────────────────────────────────────────────────────────────
    {
        'titre': 'Churros con Chocolate',
        'pays': 'spain',
        'type_plat': 'sucré',
        'description': 'Beignets espagnols croustillants trempés dans un chocolat chaud épais — le petit-déjeuner de champion.',
        'temps_preparation': 15, 'temps_cuisson': 15, 'nb_personnes': 4, 'difficulte': 'Facile',
        'ingredients': ['250 g de farine', '250 ml d\'eau bouillante', '1 pincée de sel',
                        'Huile de friture', 'Sucre + cannelle pour enrober',
                        '200 g de chocolat noir', '400 ml de lait', '2 c. de Maïzena', '50 g de sucre'],
        'etapes': ['Mélanger farine, sel et eau bouillante pour former une pâte lisse.',
                   'Mettre en poche à douille cannelée. Chauffer l\'huile à 180°C.',
                   'Frire des boudins de 15 cm en les coupant aux ciseaux. Frire 3 min de chaque côté.',
                   'Égoutter et rouler dans sucre + cannelle.',
                   'Préparer le chocolat : faire fondre chocolat avec lait, Maïzena et sucre en fouettant. Servir chaud.'],
        'tags': ['Madrid', 'Petit-déjeuner', 'Chocolat', 'Street food'],
        'image_url': 'https://upload.wikimedia.org/wikipedia/commons/thumb/3/38/Churros_Churreria.jpg/800px-Churros_Churreria.jpg',
    },
    # ── ITALY ────────────────────────────────────────────────────────────────
    {
        'titre': 'Tiramisu',
        'pays': 'italy',
        'type_plat': 'sucré',
        'description': 'Le dessert italien absolu : biscuits imbibés d\'expresso, crème mascarpone-œufs et cacao amer.',
        'temps_preparation': 30, 'temps_cuisson': 0, 'nb_personnes': 8, 'difficulte': 'Facile',
        'ingredients': ['400 g de mascarpone', '4 œufs', '100 g de sucre', '24 boudoirs (savoiardi)',
                        '300 ml d\'expresso refroidi', '30 ml de marsala ou rhum', 'Cacao amer'],
        'etapes': ['Séparer les blancs des jaunes. Battre jaunes et sucre jusqu\'à blanchissement.',
                   'Incorporer le mascarpone au mélange jaunes-sucre.',
                   'Monter les blancs en neige ferme. Plier délicatement dans la crème mascarpone.',
                   'Tremper rapidement les boudoirs dans l\'expresso + marsala. Tapisser un plat.',
                   'Alterner couche de biscuits et crème. Finir par la crème. Réfrigérer 6h. Saupoudrer de cacao.'],
        'tags': ['Venise', 'Café', 'Mascarpone', 'Classique'],
        'image_url': 'https://upload.wikimedia.org/wikipedia/commons/thumb/9/9c/Tiramisu_1.jpg/800px-Tiramisu_1.jpg',
    },
    # ── PORTUGAL ─────────────────────────────────────────────────────────────
    {
        'titre': 'Pastéis de Nata',
        'pays': 'portugal',
        'type_plat': 'sucré',
        'description': 'Les célèbres tartelettes à la crème portugaises : flan crémeux vanillé dans une coque feuilletée croustillante.',
        'temps_preparation': 20, 'temps_cuisson': 15, 'nb_personnes': 12, 'difficulte': 'Moyen',
        'ingredients': ['1 rouleau de pâte feuilletée', '500 ml de lait entier', '6 jaunes d\'œuf',
                        '150 g de sucre', '30 g de Maïzena', '1 bâton de cannelle', 'Zeste de citron',
                        'Cannelle + sucre glace pour servir'],
        'etapes': ['Préparer le flan : chauffer lait avec cannelle et zeste. Filtrer.',
                   'Battre jaunes, sucre et Maïzena. Verser le lait chaud en fouettant. Cuire jusqu\'à épaississement.',
                   'Découper la pâte feuilletée en ronds. Foncer des moules à tartelette.',
                   'Remplir de crème aux 3/4. Cuire 12–15 min à 250°C (four très chaud).',
                   'La surface doit être légèrement brûlée. Saupoudrer de cannelle + sucre glace.'],
        'tags': ['Lisbonne', 'Belém', 'Flan', 'Café'],
        'image_url': 'https://upload.wikimedia.org/wikipedia/commons/thumb/3/3a/Pastel_de_nata.jpg/800px-Pastel_de_nata.jpg',
    },
    # ── NETHERLANDS ──────────────────────────────────────────────────────────
    {
        'titre': 'Stroopwafels',
        'pays': 'netherlands',
        'type_plat': 'sucré',
        'description': 'Gaufres hollandaises fourrées de caramel liquide : s\'apprécient posées sur une tasse chaude pour ramollir le caramel.',
        'temps_preparation': 30, 'temps_cuisson': 20, 'nb_personnes': 16, 'difficulte': 'Moyen',
        'ingredients': ['250 g de farine', '125 g de beurre fondu', '75 g de sucre', '7 g de levure',
                        '1 œuf', '100 ml de lait tiède',
                        '200 g de cassonade', '100 g de beurre (caramel)', '1 c. de sirop de maïs', '1 c. de cannelle'],
        'etapes': ['Mélanger farine, levure, sucre, beurre, œuf et lait. Pétrir. Laisser lever 1h.',
                   'Diviser en 16 boules. Cuire dans un gaufrier très chaud (fine et ronde).',
                   'Préparer le caramel : cassonade, beurre, sirop et cannelle. Cuire 5 min.',
                   'Couper chaque gaufre en deux à l\'horizontal encore chaud.',
                   'Tartiner de caramel et refermer immédiatement.'],
        'tags': ['Amsterdam', 'Café', 'Caramel', 'Goûter'],
        'image_url': 'https://upload.wikimedia.org/wikipedia/commons/thumb/6/64/Stroopwafels_01.jpg/800px-Stroopwafels_01.jpg',
    },
    # ── BELGIUM ──────────────────────────────────────────────────────────────
    {
        'titre': 'Gaufres de Liège',
        'pays': 'belgium',
        'type_plat': 'sucré',
        'description': 'Gaufres belges caramélisées, denses et moelleuses — avec des perles de sucre fondues à la cuisson.',
        'temps_preparation': 20, 'temps_cuisson': 20, 'nb_personnes': 8, 'difficulte': 'Moyen',
        'ingredients': ['500 g de farine', '200 g de beurre mou', '10 g de levure sèche',
                        '200 ml de lait tiède', '2 œufs', '1 sachet de sucre vanillé',
                        '200 g de sucre perlé (grains)'],
        'etapes': ['Dissoudre la levure dans le lait tiède. Mélanger avec farine, beurre, œufs et sucre vanillé.',
                   'Pétrir 10 min. Laisser lever 1h.',
                   'Incorporer délicatement le sucre perlé sans pétrir.',
                   'Diviser en 8 pâtons. Cuire dans le gaufrier 3–4 min.',
                   'Servir chaud tel quel ou avec chantilly et fruits.'],
        'tags': ['Liège', 'Street food', 'Sucre perlé', 'Moelleux'],
        'image_url': 'https://upload.wikimedia.org/wikipedia/commons/thumb/8/8e/Gaufres_de_li%C3%A8ge.jpg/800px-Gaufres_de_li%C3%A8ge.jpg',
    },
]


class Command(BaseCommand):
    help = 'Patch sucré — ajoute les recettes dessert manquantes (England, Germany, Spain, Italy, Portugal, Netherlands, Belgium)'

    def handle(self, *args, **options):
        created, updated = 0, 0
        for data in RECIPES:
            lookup = {
                'titre':     data['titre'],
                'pays':      data['pays'],
                'type_plat': data['type_plat'],
            }
            defaults = {k: v for k, v in data.items() if k not in lookup}
            obj, was_created = Recipe.objects.update_or_create(**lookup, defaults=defaults)
            if was_created:
                created += 1
            else:
                updated += 1
        self.stdout.write(self.style.SUCCESS(
            f'Done — {created} created, {updated} updated ({created + updated} total)'
        ))
