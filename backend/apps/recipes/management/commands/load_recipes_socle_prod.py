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
    # 159 matchs à venir opposent deux équipes américaines : il faut assez de
    # variété pour que les deux camps ne reçoivent pas le même plat.
    {'titre': "Pulled Pork Sandwich", 'pays': "usa", 'type_plat': "salé",
     'description': "Épaule de porc effilochée après une longue cuisson douce, liée à une sauce barbecue au vinaigre et servie dans un pain brioché avec du chou croquant.",
     'temps_preparation': 20, 'temps_cuisson': 180, 'nb_personnes': 6, 'difficulte': "Facile",
     'ingredients': ["1,5 kg d'épaule de porc", "2 c. paprika fumé", "1 c. cassonade", "200 ml de sauce barbecue", "60 ml de vinaigre de cidre", "6 pains briochés", "1/4 de chou blanc", "2 c. mayonnaise"],
     'etapes': ["Frotter le porc au paprika, à la cassonade, au sel et au poivre.", "Cuire à couvert 3 h à 150°C, la viande doit céder sous la fourchette.", "Effilocher à deux fourchettes, mêler à la sauce barbecue et au vinaigre.", "Émincer le chou finement, le lier à la mayonnaise.", "Griller les pains, garnir de porc puis de chou.", "Servir aussitôt, la viande encore chaude."],
     'tags': ["Barbecue", "Sud", "Porc", "Convivial"], 'image_url': ""},
    {'titre': "Buffalo Wings", 'pays': "usa", 'type_plat': "salé",
     'description': "Ailes de poulet rôties jusqu'au croustillant puis enrobées d'une sauce au piment et au beurre, servies avec une sauce au bleu et des bâtonnets de céleri.",
     'temps_preparation': 15, 'temps_cuisson': 45, 'nb_personnes': 4, 'difficulte': "Facile",
     'ingredients': ["1,2 kg d'ailes de poulet", "2 c. levure chimique", "120 ml de sauce piquante type cayenne", "80 g de beurre", "1 c. vinaigre blanc", "100 g de bleu", "150 ml de crème aigre", "4 branches de céleri"],
     'etapes': ["Sécher les ailes, les mêler à la levure chimique, au sel et au poivre.", "Disposer sur une grille et cuire 45 min à 200°C en retournant à mi-cuisson.", "Fondre le beurre avec la sauce piquante et le vinaigre.", "Enrober les ailes brûlantes de sauce dans un grand saladier.", "Écraser le bleu dans la crème aigre.", "Servir avec la sauce et les bâtonnets de céleri."],
     'tags': ["Buffalo", "Poulet", "Piquant", "À partager"], 'image_url': ""},
    {'titre': "Mac and Cheese au four", 'pays': "usa", 'type_plat': "salé",
     'description': "Macaronis nappés d'une béchamel au cheddar affiné, gratinés sous une chapelure beurrée jusqu'à former une croûte.",
     'temps_preparation': 15, 'temps_cuisson': 30, 'nb_personnes': 6, 'difficulte': "Facile",
     'ingredients': ["500 g de macaronis", "60 g de beurre", "60 g de farine", "800 ml de lait", "400 g de cheddar affiné râpé", "1 c. moutarde en poudre", "1 pincée de noix de muscade", "80 g de chapelure", "30 g de beurre (croûte)"],
     'etapes': ["Cuire les macaronis 2 min de moins que le temps indiqué.", "Faire un roux blond, mouiller au lait chaud en fouettant.", "Cuire 5 min, ajouter le cheddar, la moutarde et la muscade hors du feu.", "Mêler aux pâtes, verser dans un plat beurré.", "Couvrir de chapelure mêlée au beurre fondu.", "Gratiner 25 min à 190°C jusqu'à croûte dorée."],
     'tags': ["Cheddar", "Gratin", "Réconfort"], 'image_url': ""},
    {'titre': "New England Clam Chowder", 'pays': "usa", 'type_plat': "salé",
     'description': "Soupe crémeuse de palourdes et de pommes de terre, relevée au lard fumé et au thym. La spécialité de la côte Est.",
     'temps_preparation': 20, 'temps_cuisson': 35, 'nb_personnes': 4, 'difficulte': "Moyen",
     'ingredients': ["1 kg de palourdes", "150 g de poitrine fumée", "600 g de pommes de terre", "1 oignon", "2 branches de céleri", "40 g de farine", "500 ml de crème liquide", "Thym", "Poivre blanc", "Crackers salés"],
     'etapes': ["Ouvrir les palourdes à couvert dans un fond d'eau, filtrer et garder le jus.", "Décoquiller, réserver la chair.", "Rissoler le lard, ajouter oignon et céleri en petits dés.", "Singer à la farine, mouiller au jus de cuisson filtré.", "Ajouter les pommes de terre en cubes, cuire 20 min.", "Verser la crème, remettre les palourdes, chauffer sans bouillir.", "Servir avec des crackers émiettés."],
     'tags': ["Nouvelle-Angleterre", "Palourdes", "Soupe", "Hiver"], 'image_url': ""},
    {'titre': "Peach Cobbler", 'pays': "usa", 'type_plat': "sucré",
     'description': "Pêches cuites sous une pâte sablée qui s'ouvre en croûte irrégulière, parfumée à la cannelle. Servi tiède avec une glace vanille.",
     'temps_preparation': 15, 'temps_cuisson': 40, 'nb_personnes': 6, 'difficulte': "Facile",
     'ingredients': ["1 kg de pêches", "100 g de sucre roux", "1 c. cannelle", "Jus d'un demi-citron", "180 g de farine", "100 g de beurre froid", "80 g de sucre", "1 c. levure chimique", "120 ml de lait"],
     'etapes': ["Peler et trancher les pêches, les mêler au sucre roux, à la cannelle et au citron.", "Répartir dans un plat beurré.", "Sabler farine, beurre froid, sucre et levure du bout des doigts.", "Détendre au lait pour obtenir une pâte épaisse.", "Déposer par cuillerées irrégulières sur les fruits.", "Cuire 40 min à 190°C. Laisser tiédir 10 min avant de servir."],
     'tags': ["Géorgie", "Pêche", "Cannelle", "Tiède"], 'image_url': ""},
    {'titre': "New York Cheesecake", 'pays': "usa", 'type_plat': "sucré",
     'description': "Cheesecake dense au fromage frais sur fond de biscuits beurrés, cuit au bain-marie pour éviter les craquelures.",
     'temps_preparation': 30, 'temps_cuisson': 60, 'nb_personnes': 10, 'difficulte': "Moyen",
     'ingredients': ["200 g de biscuits secs", "90 g de beurre fondu", "900 g de fromage frais", "200 g de sucre", "4 œufs", "200 ml de crème épaisse", "1 c. vanille", "Zeste d'un citron", "2 c. maïzena"],
     'etapes': ["Mixer les biscuits, lier au beurre, tasser au fond d'un moule à charnière.", "Battre le fromage et le sucre sans incorporer d'air.", "Ajouter les œufs un à un, puis crème, vanille, zeste et maïzena.", "Verser sur le fond, poser le moule dans un bain-marie.", "Cuire 60 min à 160°C : le centre doit encore trembler.", "Laisser refroidir four éteint porte entrouverte, puis 6 h au frais."],
     'tags': ["New York", "Fromage frais", "Bain-marie"], 'image_url': ""},
    {'titre': "Brownies fondants aux noix de pécan", 'pays': "usa", 'type_plat': "sucré",
     'description': "Brownies au chocolat noir, cœur fondant et croûte fine, parsemés de noix de pécan torréfiées.",
     'temps_preparation': 15, 'temps_cuisson': 25, 'nb_personnes': 12, 'difficulte': "Facile",
     'ingredients': ["200 g de chocolat noir", "180 g de beurre", "220 g de sucre", "3 œufs", "100 g de farine", "1 pincée de sel", "120 g de noix de pécan", "1 c. vanille"],
     'etapes': ["Torréfier les noix de pécan 8 min à 170°C, concasser.", "Fondre chocolat et beurre au bain-marie.", "Fouetter œufs et sucre jusqu'à blanchiment, ajouter la vanille.", "Incorporer le chocolat fondu, puis farine et sel sans trop travailler.", "Ajouter les noix, verser dans un moule chemisé.", "Cuire 22-25 min à 180°C : la lame doit ressortir humide."],
     'tags': ["Chocolat", "Pécan", "Fondant"], 'image_url': ""},
    {'titre': "Key Lime Pie", 'pays': "usa", 'type_plat': "sucré",
     'description': "Tarte de Floride au citron vert : crème acidulée au lait concentré sur un fond de biscuits, couronnée de chantilly.",
     'temps_preparation': 25, 'temps_cuisson': 20, 'nb_personnes': 8, 'difficulte': "Facile",
     'ingredients': ["220 g de biscuits secs", "100 g de beurre fondu", "400 g de lait concentré sucré", "4 jaunes d'œufs", "150 ml de jus de citron vert", "Zeste de 3 citrons verts", "250 ml de crème liquide", "30 g de sucre glace"],
     'etapes': ["Mixer les biscuits, lier au beurre, tasser dans un moule à tarte.", "Cuire le fond 10 min à 175°C, laisser refroidir.", "Fouetter les jaunes avec le zeste jusqu'à épaississement.", "Incorporer le lait concentré puis le jus de citron vert.", "Verser sur le fond, cuire 15 min à 175°C.", "Refroidir 4 h, couvrir de crème fouettée au sucre glace."],
     'tags': ["Floride", "Citron vert", "Acidulé"], 'image_url': ""},
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
