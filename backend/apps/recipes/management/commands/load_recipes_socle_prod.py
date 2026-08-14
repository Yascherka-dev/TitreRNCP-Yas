"""
Socle minimal de recettes pour la production.

Une partie du catalogue local n'a jamais été versionnée : ces recettes-là
n'existent que dans la base de développement. En production, les pays
concernés sortaient donc sans recette — 3 sports sur 5 étaient muets.

Ce fichier ne reprend pas tout le catalogue local : uniquement un plat salé
et un dessert par pays absent de la production. _pick_recipe retombe sur le
pays quand aucune recette d'équipe ni de région ne correspond, ce qui suffit
à ne jamais afficher de carte vide.

Les recettes propres aux clubs restent en base de développement.
"""

from django.core.management.base import BaseCommand
from apps.recipes.models import Recipe

RECIPES = [
    # ── AZERBAIJAN ────────────────────────────────────────────────────────────
    {'titre': "Pakhlava de Bakou", 'pays': "azerbaijan", 'type_plat': "sucré",
     'description': "Feuilletés croustillants imbibés de miel et généreusement garnis de pistaches concassées. Le dessert emblématique du Caucase : la pâte croque, le miel chaud imprègne chaque couche.",
     'temps_preparation': 15, 'temps_cuisson': 20, 'nb_personnes': 6, 'difficulte': "Facile",
     'ingredients': ["6 feuilles de pâte filo", "150g de pistaches concassées", "80g de beurre fondu", "150g de miel", "2 cuillères à soupe d'eau", "1 pincée de cannelle"],
     'etapes': ["Badigeonne chaque feuille filo de beurre fondu et empile-les en coupant des losanges.", "Parsème généreusement de pistaches entre les couches.", "Enfourne 20 min à 180°C jusqu'à doré croustillant.", "Pendant ce temps, réchauffe le miel avec l'eau et la cannelle.", "Trempe les losanges chauds dans le miel sucré — laisse bien imbiber et laisse refroidir."],
     'tags': ["traditionnel", "miel", "pistache", "feuilleté", "Moyen-Orient", "rapide"], 'image_url': ""},

    # ── CYPRUS ────────────────────────────────────────────────────────────────
    {'titre': "Loukoumades aux miel et cannelle", 'pays': "cyprus", 'type_plat': "sucré",
     'description': "Petites boules de pâte frites, croustillantes dehors et moelleuses dedans, nappées de miel chaud et saupoudrées de cannelle. Le classique méditerranéen, servi brûlant.",
     'temps_preparation': 15, 'temps_cuisson': 10, 'nb_personnes': 4, 'difficulte': "Facile",
     'ingredients': ["250g farine", "200ml eau tiède", "1 cuillère à café levure chimique", "150ml miel", "1 cuillère à café cannelle", "Huile de friture"],
     'etapes': ["Mélange farine, levure et eau tiède jusqu'à obtenir une pâte lisse et homogène", "Chauffe l'huile à 170°C, puis prélève des petites boules avec deux cuillères et plonge-les", "Fais frire 2-3 minutes jusqu'à dorure uniforme, puis égoutte sur papier absorbant", "Trempe chaque loukoumade dans le miel chaud, saupoudre généreusement de cannelle", "Sers immédiatement, encore chaudes et dégoulinantes de miel."],
     'tags': ["Dessert traditionnel", "Méditerranéen", "Friandise locale", "Rapide", "Convivialité"], 'image_url': ""},

    # ── CZECH REPUBLIC ────────────────────────────────────────────────────────
    {'titre': "Trdelník - Le rouleau sucré de Prague", 'pays': "czech republic", 'type_plat': "sucré",
     'description': "Un classique des rues de Prague : du pain enrobé de sucre et de cannelle, grillé à la perfection jusqu'à être croustillant dehors, moelleux dedans. C'est comme croquer dans une vraie victoire, les copains !",
     'temps_preparation': 15, 'temps_cuisson': 10, 'nb_personnes': 4, 'difficulte': "Facile",
     'ingredients': ["1 rouleau de pâte briochée du commerce", "50g de beurre fondu", "50g de sucre en poudre", "2 cuillères à café de cannelle", "30g de noix concassées", "Miel pour servir"],
     'etapes': ["Déroulez la pâte et coupez-la en lanières de 2cm de large", "Badigeonnez généreusement de beurre fondu", "Mélangez sucre, cannelle et noix, puis roulez les lanières dedans", "Enroulez chaque lanière autour d'une brochette en bois", "Grrillez 8-10 min à la poêle ou au four à 200°C jusqu'à doré croustillant"],
     'tags': ["Prague", "pâtisserie locale", "match day", "sucré croustillant", "tradition tchèque", "rapide"], 'image_url': ""},

    # ── DENMARK ───────────────────────────────────────────────────────────────
    {'titre': "Æbleskiver - Les Boules Sucrées de Copenhague", 'pays': "denmark", 'type_plat': "sucré",
     'description': "Des petites boules gonflées, dorées et moelleuses, fourrées de confiture de pomme — c'est le hymne sucré des hivers danois ! Poudre de sucre glace, compote chaude à l'intérieur, c'est du pur réconfort avant le match.",
     'temps_preparation': 15, 'temps_cuisson': 12, 'nb_personnes': 4, 'difficulte': "Facile",
     'ingredients': ["200g de farine", "2 œufs", "250ml de lait", "1 sachet de levure chimique", "Confiture de pomme ou marmelade", "Sucre glace pour saupoudrer"],
     'etapes': ["Mélange farine, levure et une pincée de sel, puis incorpore les œufs et le lait pour une pâte lisse.", "Préchauffe le moule à æbleskiver (ou utilise une poêle spéciale) bien beurré.", "Verse la pâte aux trois quarts dans chaque creux, puis une cuillerée de confiture au centre.", "Cuis 4-6 minutes par côté jusqu'à dorage parfait, en les tournant régulièrement à la brochette.", "Dépote encore chaud et saupoudre généreusement de sucre glace — c'est prêt !"],
     'tags': ["Denmark", "Copenhague", "dessert danois", "gourmandise locale", "tradition", "réconfortant", "rapide"], 'image_url': ""},

    # ── GREECE ────────────────────────────────────────────────────────────────
    {'titre': "Loukoumades - Beignets au miel et noix", 'pays': "greece", 'type_plat': "sucré",
     'description': "Des petites boules dorées et croustillantes, moelleuses dedans, généreusement arrosées de miel chaud et saupoudrées de noix concassées. C'est la gourmandise grecque par excellence — le must avant le match, quand les supporters descendent vers le stade avec ces petites merveilles en main !",
     'temps_preparation': 15, 'temps_cuisson': 10, 'nb_personnes': 4, 'difficulte': "Facile",
     'ingredients': ["250g farine", "250ml eau tiède", "7g levure boulangère", "Miel liquide (5-6 c. à soupe)", "Noix concassées", "Huile pour friture"],
     'etapes': ["Mélange farine, eau tiède et levure — laisse reposer 1h", "Préchauffe l'huile à 180°C", "Prélève des petites portions à la cuillère, laisse cuire 2-3 min jusqu'à doré", "Égoute sur papier absorbant", "Arrose généreusement de miel chaud et saupoudre de noix"],
     'tags': ["Grèce", "Pirée", "dessert traditionnel", "beignets", "miel", "snack match", "gourmandise"], 'image_url': ""},

    # ── IRELAND ───────────────────────────────────────────────────────────────
    {'titre': "Colcannon du Supporter Dublinois", 'pays': "ireland", 'type_plat': "salé",
     'description': "Pommes de terre écrasées avec du chou, du beurre et du lait — le plat réconfortant des pubs irlandais! Parfait pour se réchauffer avant le match avec ses copains. Simple, authentique, bourré de saveurs rustiques!",
     'temps_preparation': 10, 'temps_cuisson': 20, 'nb_personnes': 4, 'difficulte': "Facile",
     'ingredients': ["800g de pommes de terre", "300g de chou vert", "150ml de lait chaud", "100g de beurre", "4 oignons verts", "Sel et poivre"],
     'etapes': ["Cuire les pommes de terre pelées dans l'eau salée pendant 15 minutes", "Faire revenir le chou ciselé au beurre avec les oignons verts pendant 5 minutes", "Écraser les pommes de terre avec le lait chaud et le beurre", "Mélanger délicatement le chou cuit aux pommes de terre", "Assaisonner généreusement et servir fumant dans les assiettes!"],
     'tags': ["Cuisine irlandaise", "Plat réconfortant", "Match rugby", "Dublin", "Recette rapide", "Tradition pub"], 'image_url': ""},
    {'titre': "Baileys Brownies - Le péché mignon du supporter irlandais", 'pays': "ireland", 'type_plat': "sucré",
     'description': "Des brownies moelleux imbibés de Baileys, c'est le vrai truc qui fait vibrer les supporters dublinois ! Riche, gourmand, avec cette touche de crème irlandaise qui rend fou — parfait pour rugbymen qui aiment les vraies saveurs.",
     'temps_preparation': 10, 'temps_cuisson': 20, 'nb_personnes': 6, 'difficulte': "Facile",
     'ingredients': ["100g chocolat noir", "100g beurre", "150g sucre", "2 œufs", "80ml Baileys Irish Cream", "80g farine"],
     'etapes': ["Fonds le chocolat et le beurre ensemble au bain-marie, puis mélange avec le sucre et les œufs.", "Verse le Baileys dans la préparation, puis ajoute délicatement la farine.", "Verse dans un moule beurré et enfourne 20 min à 180°C — le centre doit rester gourmand !", "Laisse refroidir avant de découper en carrés généreux."],
     'tags': ["Baileys", "chocolat", "Irlande", "rugby", "rapide", "gourmand"], 'image_url': ""},

    # ── KAZAKHSTAN ────────────────────────────────────────────────────────────
    {'titre': "Chak-Chak aux amandes — le miel doré du Kazakhstan", 'pays': "kazakhstan", 'type_plat': "sucré",
     'description': "Des petites perles de pâte frite enrobées de miel chaud et d'amandes concassées — croustillant dehors, fondant dedans. C'est la gourmandise traditionnelle kazakhe qui fera trembler les filets du FK Kairat ! Simple, rapide, et tellement gourmand qu'on ne peut pas s'arrêter.",
     'temps_preparation': 15, 'temps_cuisson': 12, 'nb_personnes': 4, 'difficulte': "Facile",
     'ingredients': ["200g de farine", "1 œuf", "100g de miel", "100g d'amandes effilées", "Huile de friture", "1 pincée de sel"],
     'etapes': ["Mélange farine, œuf et sel, forme une boule. Laisse reposer 5 min.", "Divise en petites boulettes, aplatis-les légèrement.", "Fais-les frire 2-3 min jusqu'à doré croustillant.", "Chauffe le miel, trempe les perles dedans, roule dans les amandes.", "Laisse refroidir sur papier absorbant, puis sers sans attendre."],
     'tags': ["Kazakhstan", "Almaty", "Traditionnel", "Miel", "Amandes", "Match day", "Gourmandise", "Rapide"], 'image_url': ""},

    # ── NORWAY ────────────────────────────────────────────────────────────────
    {'titre': "Serinakaker - Les Petits Gâteaux du Nord", 'pays': "norway", 'type_plat': "sucré",
     'description': "Des petits gâteaux moelleux aux amandes et à la cardamome, typiques de la Norvège du Nord — croustillants dehors, fondants dedans, avec cette touche d'épice nordique qui réchauffe comme un but en dernière minute !",
     'temps_preparation': 15, 'temps_cuisson': 12, 'nb_personnes': 12, 'difficulte': "Facile",
     'ingredients': ["100g de beurre mou", "100g de sucre", "1 œuf", "100g de poudre d'amandes", "1 cuillère à café de cardamome moulue", "30g de farine"],
     'etapes': ["Mélange le beurre et le sucre jusqu'à blanchir — c'est la base gagnante !", "Ajoute l'œuf, puis la poudre d'amandes, la cardamome et la farine", "Dépose des petites cuillères de pâte sur une plaque", "Enfourne à 200°C pendant 10-12 minutes — dorage parfait !"],
     'tags': ["Norvège", "gâteaux", "amandes", "cardamome", "rapide", "match day", "gourmandise nordique"], 'image_url': ""},

    # ── SCOTLAND ──────────────────────────────────────────────────────────────
    {'titre': "Shortbread d'Édimbourg aux Écossais", 'pays': "scotland", 'type_plat': "sucré",
     'description': "Le shortbread écossais : du beurre, du sucre, de la farine — trois ingrédients glorieux qui deviennent croustillants, fondants, irrésistibles. C'est le péché mignon des Calédoniens, le gâteau qui accompagne chaque victoire ! Parfait avant le coup d'envoi.",
     'temps_preparation': 10, 'temps_cuisson': 15, 'nb_personnes': 4, 'difficulte': "Facile",
     'ingredients': ["200g de beurre doux ramolli", "100g de sucre glace", "300g de farine", "1 pincée de sel", "Sucre cristallisé pour finir"],
     'etapes': ["Mélange le beurre et le sucre glace jusqu'à obtenir une crème légère et mousseuse", "Incorpore la farine et le sel délicatement, pétrisse à la main jusqu'à former une boule homogène", "Étale entre deux feuilles de papier cuisson, découpe en carrés ou rectangles", "Enfourne 15 min à 180°C jusqu'à doré pâle, saupoudre de sucre cristallisé en sortant", "Laisse refroidir 5 min — ça va craquer sous la dent, c'est divin !"],
     'tags': ["shortbread", "Édimbourg", "rugby", "croustillant", "recette classique écossaise", "apéritif sucré"], 'image_url': ""},

    # ── TURKEY ────────────────────────────────────────────────────────────────
    {'titre': "Baklava", 'pays': "turkey", 'type_plat': "sucré",
     'description': "Ah, le baklava ! Des feuilles fines comme du papier de soie, croustillantes à souhait, fourrées de pistaches et noix concassées — c'est du pur bonheur entre les dents. On arrose tout ça généreusement de sirop au miel et eau de rose, et voilà un dessert qui t'envoie directement en Orient avec chaque bouchée !",
     'temps_preparation': 45, 'temps_cuisson': 35, 'nb_personnes': 12, 'difficulte': "Moyen",
     'ingredients': ["500 g de pâte filo", "200 g de pistaches non salées", "150 g de noix", "200 g de beurre clarifié", "300 g de sucre", "200 ml d'eau", "Eau de rose"],
     'etapes': ["Hacher grossièrement pistaches et noix.", "Superposer 8 feuilles de filo en badigeonnant de beurre à chaque couche.", "Étaler les fruits secs, continuer avec 8 autres couches de filo.", "Découper en losanges et cuire 30–35 min à 170°C.", "Napper de sirop chaud (sucre + eau + eau de rose) dès la sortie du four."],
     'tags': ["Dessert", "Istanbul", "Pistache", "Festif"], 'image_url': "https://upload.wikimedia.org/wikipedia/commons/thumb/9/9e/Baklava_-_Turkish_special%2C_fresh_out_of_the_oven_%283392593238%29.jpg/800px-Baklava_-_Turkish_special%2C_fresh_out_of_the_oven_%283392593238%29.jpg"},

    # ── USA ───────────────────────────────────────────────────────────────────
    {'titre': "Pulled Pork Sliders à l'Atlanta", 'pays': "usa", 'type_plat': "salé",
     'description': "Des mini sandwichs de porc effiloché, mariné et cuit à feu doux, avec une sauce BBQ maison qui colle aux doigts. Parfait pour grignoter entre deux paniers – rapide, gourmand, et tu peux les préparer avant le coup d'envoi !",
     'temps_preparation': 10, 'temps_cuisson': 25, 'nb_personnes': 4, 'difficulte': "Facile",
     'ingredients': ["600g de porc (épaule ou poitrine)", "4 cuillères à soupe de sauce BBQ", "2 cuillères à soupe de vinaigre blanc", "1 cuillère à café de paprika fumé", "8 petits pains ronds", "Oignons rouges frais (pour garnir)", "Sel et poivre"],
     'etapes': ["Assaisonne le porc avec paprika, sel et poivre. Fais-le revenir 5 min à la poêle bien chaude.", "Ajoute sauce BBQ et vinaigre, puis couvre et laisse mijoter 20 min à feu moyen-doux.", "Effiloche la viande avec deux fourchettes, le porc doit se défaire tout seul.", "Grille les petits pains 1-2 min, garnit-les de porc effiloché et quelques lamelles d'oignon.", "Sers chaud et rapide – les Hawks ne vont pas t'attendre !"],
     'tags': ["barbecue", "match-day", "street-food", "rapide", "convivial", "Atlanta"], 'image_url': ""},
    {'titre': "Peach Cobbler d'Atlanta", 'pays': "usa", 'type_plat': "sucré",
     'description': "Le dessert culte de Géorgie ! Des pêches fondantes caramélisées sous une couche dorée et croustillante — c'est comme une victoire aux Hawks, irrésistible et mémorable. Parfait chaud avec une boule de vanille pour célébrer le match !",
     'temps_preparation': 15, 'temps_cuisson': 25, 'nb_personnes': 4, 'difficulte': "Facile",
     'ingredients': ["800g de pêches en conserve (ou fraîches épluchées)", "100g de farine", "80g de sucre roux", "60g de beurre mou", "1 c.à.c. de cannelle", "1 pincée de sel"],
     'etapes': ["Versez les pêches avec leur jus dans un plat allant au four, saupoudrez de cannelle.", "Mélangez farine, sucre roux, sel et beurre mou avec les doigts — ça doit ressembler à du sable humide.", "Étalez ce mélange généreusement sur les pêches.", "Enfournez à 200°C pendant 25 min jusqu'à brun doré.", "Sortez et laissez tiédir 5 min avant de servir."],
     'tags': ["Géorgie", "Pêches", "Dessert rapide", "Match de basket", "Tradition américaine", "Facile et gourmand"], 'image_url': ""},
]


class Command(BaseCommand):
    help = "Socle minimal : un salé et un dessert pour chaque pays absent de la production"

    def handle(self, *args, **options):
        created, updated = 0, 0
        for data in RECIPES:
            lookup = {'titre': data['titre'], 'pays': data['pays'], 'type_plat': data['type_plat']}
            defaults = {k: v for k, v in data.items() if k not in lookup}
            _, was_created = Recipe.objects.update_or_create(**lookup, defaults=defaults)
            if was_created:
                created += 1
            else:
                updated += 1
        self.stdout.write(self.style.SUCCESS(
            f'Done — {created} created, {updated} updated ({created + updated} total)'
        ))
