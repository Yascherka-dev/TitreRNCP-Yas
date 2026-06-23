from django.core.management.base import BaseCommand
from apps.recipes.models import Recipe

RECIPES = [
    # ── VENEZUELA ───────────────────────────────────────────────────────────────
    {'titre': 'Pabellón Criollo', 'pays': 'venezuela', 'type_plat': 'salé',
     'description': 'Le plat national vénézuélien : riz blanc, haricots noirs mijotés, bœuf effiloché et banane plantain frite.',
     'temps_preparation': 20, 'temps_cuisson': 40, 'nb_personnes': 4, 'difficulte': 'Facile',
     'ingredients': ['400 g de bœuf à braiser', '300 g de haricots noirs', '300 g de riz', '2 bananes plantains', '1 oignon', '3 gousses d\'ail', 'Cumin', 'Huile'],
     'etapes': ['Cuire les haricots noirs 30 min avec ail et cumin.', 'Braiser le bœuf, effilocher.', 'Cuire le riz à l\'eau salée.', 'Trancher et frire les plantains.', 'Servir les 4 éléments côte à côte.'],
     'tags': ['National', 'Caracas', 'Plantain'], 'image_url': ''},
    {'titre': 'Quesillo', 'pays': 'venezuela', 'type_plat': 'sucré',
     'description': 'Flan vénézuélien plus dense que son cousin cubain, parfumé à la vanille et au caramel brun.',
     'temps_preparation': 15, 'temps_cuisson': 50, 'nb_personnes': 8, 'difficulte': 'Facile',
     'ingredients': ['1 boîte de lait concentré sucré', '1 boîte de lait évaporé', '4 œufs', '1 c. vanille', '150 g de sucre (caramel)'],
     'etapes': ['Faire le caramel sec, couler dans un moule.', 'Mixer lait concentré, lait évaporé, œufs et vanille.', 'Verser sur le caramel.', 'Cuire au bain-marie 45 min à 180°C.', 'Réfrigérer 4h avant de démouler.'],
     'tags': ['Flan', 'Caramel', 'Dessert'], 'image_url': ''},

    # ── PANAMA ──────────────────────────────────────────────────────────────────
    {'titre': 'Sancocho de Gallina', 'pays': 'panama', 'type_plat': 'salé',
     'description': 'Soupe nationale du Panama : poule fermière, culantro, ñame et yuca mijotés longuement.',
     'temps_preparation': 15, 'temps_cuisson': 60, 'nb_personnes': 6, 'difficulte': 'Facile',
     'ingredients': ['1 poule fermière découpée', '300 g de ñame (ou igname)', '300 g de yuca', '1 épi de maïs', 'Culantro', '1 oignon', 'Ail', 'Sel'],
     'etapes': ['Faire revenir oignon et ail.', 'Ajouter la poule, couvrir d\'eau, porter à ébullition.', 'Ajouter ñame, yuca et maïs après 30 min.', 'Mijoter 30 min supplémentaires.', 'Servir avec riz blanc et culantro frais.'],
     'tags': ['National', 'Soupe', 'Réconfort'], 'image_url': ''},
    {'titre': 'Arroz con Leche Panaméen', 'pays': 'panama', 'type_plat': 'sucré',
     'description': 'Riz au lait épicé à la cannelle et aux clous de girofle, servi froid avec raisins secs.',
     'temps_preparation': 5, 'temps_cuisson': 35, 'nb_personnes': 6, 'difficulte': 'Facile',
     'ingredients': ['300 g de riz', '1 L de lait', '150 g de sucre', '1 bâton de cannelle', '3 clous de girofle', 'Zeste de citron', 'Raisins secs'],
     'etapes': ['Cuire riz dans l\'eau 15 min.', 'Ajouter lait, sucre, cannelle, clous.', 'Mijoter à feu doux 20 min en remuant.', 'Retirer épices, ajouter raisins et zeste.', 'Réfrigérer avant de servir.'],
     'tags': ['Riz au lait', 'Épices', 'Dessert'], 'image_url': ''},

    # ── COSTA RICA ──────────────────────────────────────────────────────────────
    {'titre': 'Gallo Pinto', 'pays': 'costa rica', 'type_plat': 'salé',
     'description': 'Le petit-déjeuner national : riz et haricots noirs sautés au Salsa Lizano, servis avec crème et œufs.',
     'temps_preparation': 10, 'temps_cuisson': 15, 'nb_personnes': 4, 'difficulte': 'Facile',
     'ingredients': ['300 g de riz cuit', '300 g de haricots noirs cuits', '2 c. Salsa Lizano', '1 oignon', '1 poivron', 'Coriandre', 'Huile'],
     'etapes': ['Faire revenir oignon et poivron.', 'Ajouter haricots et riz cuits.', 'Arroser de Salsa Lizano.', 'Sauter à feu vif 5 min.', 'Garnir de coriandre fraîche.'],
     'tags': ['National', 'Petit-déjeuner', 'San José'], 'image_url': ''},
    {'titre': 'Tres Leches', 'pays': 'costa rica', 'type_plat': 'sucré',
     'description': 'Génoise légère imbibée de trois laits (entier, concentré sucré, crème) et couverte de chantilly.',
     'temps_preparation': 30, 'temps_cuisson': 30, 'nb_personnes': 12, 'difficulte': 'Moyen',
     'ingredients': ['4 œufs', '200 g de sucre', '200 g de farine', '250 ml de lait entier', '200 ml de lait concentré sucré', '200 ml de crème liquide', '300 ml crème fouettée'],
     'etapes': ['Battre œufs et sucre, incorporer farine.', 'Cuire 25 min à 180°C.', 'Mélanger les trois laits, trouer le gâteau et verser.', 'Laisser imbiber 2h au frigo.', 'Couvrir de chantilly avant de servir.'],
     'tags': ['Célèbre', 'Moelleux', 'Fête'], 'image_url': ''},

    # ── HONDURAS ────────────────────────────────────────────────────────────────
    {'titre': 'Baleadas', 'pays': 'honduras', 'type_plat': 'salé',
     'description': 'Tortillas de farine épaisses garnies de haricots frits, crème, fromage et œuf brouillé.',
     'temps_preparation': 20, 'temps_cuisson': 20, 'nb_personnes': 4, 'difficulte': 'Facile',
     'ingredients': ['400 g de farine', '200 ml d\'eau tiède', '2 c. huile', 'Pincée sel', '400 g de haricots rouges frits', '4 œufs', '100 g de fromage râpé', '100 ml de crème'],
     'etapes': ['Pétrir farine, eau, huile et sel. Reposer 20 min.', 'Former des galettes épaisses. Cuire sur comal.', 'Tartiner de haricots frits.', 'Ajouter œuf brouillé, crème et fromage.', 'Servir chaud, plié en deux.'],
     'tags': ['Street food', 'Tegucigalpa', 'Tortilla'], 'image_url': ''},
    {'titre': 'Rosquillas Hondureñas', 'pays': 'honduras', 'type_plat': 'sucré',
     'description': 'Biscuits en anneau à base de farine de maïs, fromage sec et anis, dorés au four.',
     'temps_preparation': 20, 'temps_cuisson': 25, 'nb_personnes': 20, 'difficulte': 'Facile',
     'ingredients': ['500 g de masa de maïs', '150 g de fromage sec râpé', '2 œufs', '100 g de sucre', '1 c. anis', '50 g de beurre'],
     'etapes': ['Mélanger masa, fromage, sucre, beurre, œufs et anis.', 'Former des anneaux.', 'Déposer sur plaque beurrée.', 'Cuire 20-25 min à 180°C jusqu\'à dorure.', 'Laisser refroidir sur grille.'],
     'tags': ['Biscuit', 'Maïs', 'Traditionnel'], 'image_url': ''},

    # ── JAMAICA ─────────────────────────────────────────────────────────────────
    {'titre': 'Jerk Chicken', 'pays': 'jamaica', 'type_plat': 'salé',
     'description': 'Poulet mariné dans la sauce jerk jamaïcaine (piment Scotch Bonnet, allspice, thym) et grillé au charbon.',
     'temps_preparation': 30, 'temps_cuisson': 45, 'nb_personnes': 4, 'difficulte': 'Moyen',
     'ingredients': ['1 poulet découpé', '3 piments Scotch Bonnet', '2 c. allspice', '4 branches de thym', '4 gousses d\'ail', '2 c. gingembre', '2 c. sauce soja', '1 citron vert', 'Sucre brun'],
     'etapes': ['Mixer épices, piments, ail, gingembre, soja et citron.', 'Mariner le poulet 12h minimum.', 'Griller à feu moyen-vif 40 min en retournant.', 'Servir avec festival (pain frit) et riz aux pois.', 'La peau doit être bien carbonisée.'],
     'tags': ['Barbecue', 'Kingston', 'Épicé', 'Grill'], 'image_url': 'https://upload.wikimedia.org/wikipedia/commons/thumb/3/36/Jerk_chicken_with_festival.jpg/800px-Jerk_chicken_with_festival.jpg'},
    {'titre': 'Rum Cake', 'pays': 'jamaica', 'type_plat': 'sucré',
     'description': 'Gâteau dense aux fruits secs macérés dans le rhum jamaïcain pendant des semaines — incontournable à Noël.',
     'temps_preparation': 30, 'temps_cuisson': 90, 'nb_personnes': 12, 'difficulte': 'Moyen',
     'ingredients': ['500 g de fruits secs mélangés', '200 ml de rhum brun', '200 g de beurre', '200 g de sucre brun', '4 œufs', '300 g de farine', '1 c. mélange quatre-épices', '1 c. vanille'],
     'etapes': ['Faire tremper fruits secs dans le rhum 24h minimum.', 'Crémer beurre et sucre. Ajouter œufs.', 'Incorporer farine et épices, puis fruits macérés.', 'Cuire 1h30 à 150°C dans un moule beurré.', 'Arroser de rhum à la sortie du four.'],
     'tags': ['Noël', 'Rhum', 'Kingston', 'Moelleux'], 'image_url': ''},

    # ── SERBIA ──────────────────────────────────────────────────────────────────
    {'titre': 'Pljeskavica', 'pays': 'serbia', 'type_plat': 'salé',
     'description': 'Burger balkan XXL : galette de bœuf et porc épicée, servie dans un lepinja avec kajmak, oignon et ajvar.',
     'temps_preparation': 20, 'temps_cuisson': 15, 'nb_personnes': 4, 'difficulte': 'Facile',
     'ingredients': ['400 g de bœuf haché', '200 g de porc haché', '1 oignon finement haché', '1 c. paprika', '1 c. sel', 'Lepinja (pain)', 'Kajmak', 'Ajvar'],
     'etapes': ['Mélanger viandes, oignon et épices. Former des galettes plates.', 'Griller 6 min de chaque côté.', 'Ouvrir le lepinja légèrement grillé.', 'Garnir de kajmak, oignon cru et ajvar.', 'Servir immédiatement.'],
     'tags': ['Balkans', 'Belgrade', 'Grill', 'Street food'], 'image_url': ''},
    {'titre': 'Vanilice', 'pays': 'serbia', 'type_plat': 'sucré',
     'description': 'Sablés en forme de lune fourrés de confiture de prune et enrobés de sucre glace vanillé.',
     'temps_preparation': 30, 'temps_cuisson': 15, 'nb_personnes': 30, 'difficulte': 'Facile',
     'ingredients': ['300 g de farine', '200 g de beurre', '100 g de sucre glace', '2 jaunes d\'œuf', '1 c. vanille', 'Confiture de prune', 'Sucre glace pour enrober'],
     'etapes': ['Sabler beurre, farine, sucre, jaunes et vanille.', 'Former des petites boules, aplatir légèrement.', 'Cuire 12 min à 180°C.', 'Assembler deux sablés avec confiture de prune.', 'Rouler dans le sucre glace.'],
     'tags': ['Noël', 'Sablés', 'Belgrade'], 'image_url': ''},

    # ── POLAND ──────────────────────────────────────────────────────────────────
    {'titre': 'Bigos', 'pays': 'poland', 'type_plat': 'salé',
     'description': 'Le ragoût du chasseur polonais : choucroute, chou frais, viandes fumées et champignons mijotés des heures.',
     'temps_preparation': 30, 'temps_cuisson': 120, 'nb_personnes': 8, 'difficulte': 'Moyen',
     'ingredients': ['500 g de choucroute', '300 g de chou blanc', '300 g de porc fumé', '200 g de kielbasa', '50 g de champignons séchés', '150 ml de vin rouge', '2 oignons', 'Laurier', 'Poivre'],
     'etapes': ['Réhydrater les champignons. Faire revenir oignons et viandes.', 'Ajouter chou, choucroute, champignons et vin.', 'Mijoter 2h à feu doux.', 'Assaisonner. Le bigos est meilleur réchauffé le lendemain.', 'Servir avec pain de seigle.'],
     'tags': ['Chasseur', 'Varsovie', 'Hiver', 'Fumé'], 'image_url': ''},
    {'titre': 'Sernik', 'pays': 'poland', 'type_plat': 'sucré',
     'description': 'Cheesecake polonais au twaróg (fromage blanc frais) sur base de sablé, dense et légèrement acidulé.',
     'temps_preparation': 30, 'temps_cuisson': 60, 'nb_personnes': 10, 'difficulte': 'Moyen',
     'ingredients': ['1 kg de twaróg (ou fromage blanc)', '5 œufs', '200 g de sucre', '1 c. vanille', '50 g de fécule', '200 g de farine (base)', '100 g de beurre', '50 g de sucre (base)'],
     'etapes': ['Préparer la base sablée, foncer le moule, cuire 10 min.', 'Mixer fromage, sucre, œufs, vanille et fécule.', 'Verser sur la base.', 'Cuire 50 min à 170°C.', 'Laisser refroidir dans le four éteint (évite les craquelures).'],
     'tags': ['Varsovie', 'Cheesecake', 'Fête'], 'image_url': ''},

    # ── UKRAINE ─────────────────────────────────────────────────────────────────
    {'titre': 'Bortsch Ukrainien', 'pays': 'ukraine', 'type_plat': 'salé',
     'description': 'La soupe nationale ukrainienne : betteraves, chou, bœuf et légumes dans un bouillon rouge rubis.',
     'temps_preparation': 30, 'temps_cuisson': 90, 'nb_personnes': 6, 'difficulte': 'Moyen',
     'ingredients': ['3 betteraves', '500 g de bœuf', '200 g de chou', '3 pommes de terre', '2 carottes', '2 tomates', '1 oignon', 'Ail', 'Crème fraîche', 'Aneth'],
     'etapes': ['Faire le bouillon de bœuf 1h.', 'Râper betteraves, faire suer avec oignon et tomates.', 'Ajouter carottes, pommes de terre et chou au bouillon.', 'Incorporer les betteraves cuites 15 min avant la fin.', 'Servir avec crème et aneth.'],
     'tags': ['Kiev', 'Betterave', 'National'], 'image_url': 'https://upload.wikimedia.org/wikipedia/commons/thumb/4/4a/Borscht.jpg/800px-Borscht.jpg'},
    {'titre': 'Varenyky', 'pays': 'ukraine', 'type_plat': 'sucré',
     'description': 'Raviolis ukrainiens fourrés de cerises griottes, servis avec crème et sucre.',
     'temps_preparation': 60, 'temps_cuisson': 10, 'nb_personnes': 4, 'difficulte': 'Moyen',
     'ingredients': ['400 g de farine', '200 ml d\'eau tiède', '1 œuf', 'Pincée sel', '500 g de cerises griottes dénoyautées', '100 g de sucre', 'Crème fraîche'],
     'etapes': ['Pétrir farine, eau, œuf et sel. Reposer 30 min.', 'Mélanger cerises et sucre.', 'Étaler la pâte fine. Découper des ronds.', 'Garnir, plier et sceller. Cuire 8 min à l\'eau bouillante.', 'Servir avec crème fraîche et sucre supplémentaire.'],
     'tags': ['Ravioli', 'Cerises', 'Kiev'], 'image_url': ''},

    # ── HUNGARY ─────────────────────────────────────────────────────────────────
    {'titre': 'Gulyás', 'pays': 'hungary', 'type_plat': 'salé',
     'description': 'Le vrai goulash hongrois : soupe de bœuf au paprika fumé, pommes de terre et csipetke (petites pâtes).',
     'temps_preparation': 20, 'temps_cuisson': 90, 'nb_personnes': 6, 'difficulte': 'Facile',
     'ingredients': ['800 g de bœuf en cubes', '3 c. paprika doux', '1 c. paprika fumé', '2 oignons', '3 pommes de terre', '2 carottes', '1 poivron', 'Cumin', 'Ail'],
     'etapes': ['Faire revenir oignons dans le saindoux.', 'Ajouter bœuf et paprika hors du feu.', 'Couvrir d\'eau, mijoter 1h.', 'Ajouter pommes de terre et carottes, 20 min de plus.', 'Servir avec pain blanc.'],
     'tags': ['Budapest', 'Paprika', 'National'], 'image_url': 'https://upload.wikimedia.org/wikipedia/commons/thumb/9/9a/Guly%C3%A1sleves.jpg/800px-Guly%C3%A1sleves.jpg'},
    {'titre': 'Kürtőskalács', 'pays': 'hungary', 'type_plat': 'sucré',
     'description': 'Gâteau de cheminée transylvanien : pâte levée enroulée sur une broche, caramélisée au sucre.',
     'temps_preparation': 90, 'temps_cuisson': 20, 'nb_personnes': 6, 'difficulte': 'Difficile',
     'ingredients': ['500 g de farine', '7 g de levure', '200 ml de lait', '100 g de beurre', '3 jaunes', '50 g de sucre', '1 c. vanille', '100 g de sucre (enrobage)', 'Cannelle'],
     'etapes': ['Préparer une pâte levée, laisser doubler.', 'Étirer en ruban et enrouler en spirale sur une broche.', 'Rouler dans le sucre.', 'Griller en tournant près du feu 15-20 min.', 'Le sucre doit caraméliser. Glisser hors de la broche et servir chaud.'],
     'tags': ['Budapest', 'Cheminée', 'Caramel', 'Street food'], 'image_url': ''},

    # ── SLOVENIA ────────────────────────────────────────────────────────────────
    {'titre': 'Jota', 'pays': 'slovenia', 'type_plat': 'salé',
     'description': 'Soupe épaisse slovène : haricots, choucroute, pommes de terre et côtes fumées.',
     'temps_preparation': 15, 'temps_cuisson': 90, 'nb_personnes': 6, 'difficulte': 'Facile',
     'ingredients': ['400 g de haricots blancs secs', '500 g de choucroute', '300 g de pommes de terre', '200 g de lard fumé', '3 gousses d\'ail', 'Laurier', 'Cumin'],
     'etapes': ['Faire tremper les haricots une nuit.', 'Cuire haricots avec lard et ail 1h.', 'Ajouter choucroute, pommes de terre et cumin.', 'Mijoter 30 min.', 'Écraser légèrement pour épaissir. Servir chaud.'],
     'tags': ['Ljubljana', 'Hiver', 'Rustique'], 'image_url': ''},
    {'titre': 'Potica', 'pays': 'slovenia', 'type_plat': 'sucré',
     'description': 'Roulé festif slovène garni de noix moulues, miel et cannelle — emblème des fêtes nationales.',
     'temps_preparation': 120, 'temps_cuisson': 45, 'nb_personnes': 12, 'difficulte': 'Difficile',
     'ingredients': ['500 g de farine', '7 g levure', '200 ml lait', '100 g beurre', '3 jaunes', '400 g noix moulues', '150 g miel', '50 g sucre', '1 c. cannelle', 'Rhum'],
     'etapes': ['Préparer une pâte levée riche, laisser doubler.', 'Mélanger noix, miel, sucre, cannelle et rhum.', 'Étaler la pâte finement, garnir de noix.', 'Rouler serré en boudin, placer en moule à couronne.', 'Laisser lever 30 min puis cuire 40 min à 180°C.'],
     'tags': ['Ljubljana', 'Noix', 'Fêtes', 'Noël'], 'image_url': ''},

    # ── GEORGIA ─────────────────────────────────────────────────────────────────
    {'titre': 'Khinkali', 'pays': 'georgia', 'type_plat': 'salé',
     'description': 'Gros raviolis géorgiens à la viande épicée et bouillon — on tient la queue et on mange en aspirant le jus.',
     'temps_preparation': 60, 'temps_cuisson': 15, 'nb_personnes': 4, 'difficulte': 'Moyen',
     'ingredients': ['400 g de farine', '200 ml d\'eau', 'Pincée sel', '300 g de bœuf haché', '200 g de porc haché', '1 oignon', 'Coriandre', 'Cumin', 'Piment'],
     'etapes': ['Pétrir farine, eau et sel. Reposer 30 min.', 'Mélanger viandes, oignon haché, coriandre et épices avec eau.', 'Étaler la pâte, découper des ronds de 15 cm.', 'Garnir et plisser hermétiquement pour former la queue.', 'Cuire dans l\'eau bouillante salée 12 min.'],
     'tags': ['Tbilissi', 'Ravioli', 'Caucase'], 'image_url': ''},
    {'titre': 'Churchkhela', 'pays': 'georgia', 'type_plat': 'sucré',
     'description': 'Bougie géorgienne comestible : noix enfilées sur un fil, trempées dans du jus de raisin épaissi.',
     'temps_preparation': 60, 'temps_cuisson': 30, 'nb_personnes': 8, 'difficulte': 'Moyen',
     'ingredients': ['500 ml de jus de raisin rouge', '100 g de farine de blé', '200 g de noix ou noisettes', 'Fil de cuisine'],
     'etapes': ['Enfiler noix sur le fil, laisser 20 cm en bas.', 'Porter le jus de raisin à ébullition.', 'Délayer la farine dans un peu de jus froid, incorporer.', 'Cuire en fouettant jusqu\'à consistance sirupeuse épaisse.', 'Tremper les fils de noix 3 fois, laisser sécher 3 jours.'],
     'tags': ['Tbilissi', 'Raisin', 'Noix', 'Marché'], 'image_url': ''},

    # ── WALES ───────────────────────────────────────────────────────────────────
    {'titre': 'Cawl', 'pays': 'wales', 'type_plat': 'salé',
     'description': 'Soupe galloise ancestrale : épaule d\'agneau, poireaux, pommes de terre et navets mijotés des heures.',
     'temps_preparation': 20, 'temps_cuisson': 120, 'nb_personnes': 6, 'difficulte': 'Facile',
     'ingredients': ['1 kg d\'agneau (épaule)', '4 poireaux', '4 pommes de terre', '3 carottes', '2 navets', '1 oignon', 'Thym', 'Laurier', 'Persil'],
     'etapes': ['Cuire l\'agneau dans l\'eau froide, écumer.', 'Ajouter tous les légumes en cubes.', 'Mijoter 2h à feu doux.', 'Retirer l\'agneau, effilocher, remettre.', 'Servir parsemé de persil avec pain gallois.'],
     'tags': ['Cardiff', 'Agneau', 'Traditionnel', 'Hiver'], 'image_url': ''},
    {'titre': 'Welsh Cakes', 'pays': 'wales', 'type_plat': 'sucré',
     'description': 'Petits gâteaux gallois à la plancha : pâte sablée aux raisins secs, saupoudrés de sucre.',
     'temps_preparation': 15, 'temps_cuisson': 15, 'nb_personnes': 16, 'difficulte': 'Facile',
     'ingredients': ['225 g de farine', '100 g de beurre', '75 g de sucre', '1 œuf', '75 g de raisins secs', '1 c. de quatre-épices', 'Pincée sel', 'Sucre pour finir'],
     'etapes': ['Sabler farine et beurre.', 'Ajouter sucre, raisins, épices et œuf battu.', 'Former une boule, abaisser à 1 cm.', 'Découper des ronds de 7 cm.', 'Cuire sur plancha légèrement beurrée 3 min de chaque côté. Saupoudrer de sucre.'],
     'tags': ['Cardiff', 'Goûter', 'Raisins', 'Plancha'], 'image_url': ''},

    # ── QATAR ───────────────────────────────────────────────────────────────────
    {'titre': 'Machboos', 'pays': 'qatar', 'type_plat': 'salé',
     'description': 'Le plat national du Golfe : riz long épicé cuit avec agneau ou poulet, raisins secs et oignon frit.',
     'temps_preparation': 20, 'temps_cuisson': 60, 'nb_personnes': 6, 'difficulte': 'Moyen',
     'ingredients': ['600 g de riz basmati', '1 kg d\'agneau', '2 oignons', '3 tomates', 'Loomi (citron séché)', 'Baharat', 'Cardamome', 'Safran', 'Raisins secs', 'Amandes'],
     'etapes': ['Faire revenir oignon et agneau avec épices.', 'Ajouter tomates, loomi et eau. Mijoter 40 min.', 'Retirer la viande. Cuire le riz dans ce bouillon.', 'Disposer riz puis viande, garnir de raisins et amandes.', 'Servir avec salsa dakous (tomate-ail-coriandre).'],
     'tags': ['Doha', 'Golfe', 'National', 'Safran'], 'image_url': ''},
    {'titre': 'Luqaimat', 'pays': 'qatar', 'type_plat': 'sucré',
     'description': 'Beignets dorés du Golfe trempés dans du miel ou du sirop de dattes et saupoudrés de sésame.',
     'temps_preparation': 60, 'temps_cuisson': 20, 'nb_personnes': 6, 'difficulte': 'Facile',
     'ingredients': ['300 g de farine', '7 g levure', '1 c. sucre', '1 c. cardamome', '300 ml d\'eau tiède', 'Huile de friture', 'Miel ou dibs (sirop de dattes)', 'Sésame'],
     'etapes': ['Mélanger farine, levure, sucre, cardamome et eau tiède.', 'Laisser lever 1h.', 'Chauffer l\'huile à 180°C.', 'Frire des cuillerées de pâte 3-4 min jusqu\'à dorure.', 'Tremper dans le miel, saupoudrer de sésame.'],
     'tags': ['Doha', 'Beignets', 'Miel', 'Ramadan'], 'image_url': ''},

    # ── UZBEKISTAN ──────────────────────────────────────────────────────────────
    {'titre': 'Plov', 'pays': 'uzbekistan', 'type_plat': 'salé',
     'description': 'Le pilaf ouzbek royal : riz avec agneau, carottes jaunes et épices, cuit dans un grand kazan en fonte.',
     'temps_preparation': 30, 'temps_cuisson': 90, 'nb_personnes': 8, 'difficulte': 'Moyen',
     'ingredients': ['600 g de riz', '600 g d\'agneau', '4 carottes jaunes', '2 oignons', '1 tête d\'ail entière', '100 ml huile', 'Cumin', 'Barberries (épine-vinette)'],
     'etapes': ['Faire chauffer l\'huile à feu vif dans le kazan.', 'Faire revenir oignons puis agneau en cubes.', 'Ajouter carottes en julienne et épices.', 'Verser l\'eau, poser le riz et la tête d\'ail.', 'Cuire à couvert 30 min. Mélanger avant de servir.'],
     'tags': ['Tachkent', 'Kazan', 'Pilaf', 'National'], 'image_url': ''},
    {'titre': 'Chak-Chak', 'pays': 'uzbekistan', 'type_plat': 'sucré',
     'description': 'Gâteau de beignets fins nappés de miel chaud puis pressés en montagne — dessert des fêtes d\'Asie centrale.',
     'temps_preparation': 30, 'temps_cuisson': 20, 'nb_personnes': 10, 'difficulte': 'Moyen',
     'ingredients': ['400 g de farine', '3 œufs', '2 c. vodka ou cognac', 'Huile de friture', '300 g de miel', '50 g de sucre'],
     'etapes': ['Pétrir farine, œufs et alcool en pâte ferme.', 'Étaler et couper en bâtonnets fins.', 'Frire en petites quantités jusqu\'à dorure.', 'Chauffer miel et sucre jusqu\'à dissolution.', 'Mélanger miel et beignets, façonner en dôme sur assiette. Laisser durcir.'],
     'tags': ['Tachkent', 'Miel', 'Fête', 'Asie centrale'], 'image_url': ''},

    # ── JORDAN ──────────────────────────────────────────────────────────────────
    {'titre': 'Mansaf', 'pays': 'jordan', 'type_plat': 'salé',
     'description': 'Le plat national jordanien : agneau cuit dans le jameed (yaourt de brebis séché), servi sur riz et galette.',
     'temps_preparation': 30, 'temps_cuisson': 90, 'nb_personnes': 8, 'difficulte': 'Difficile',
     'ingredients': ['1,5 kg d\'agneau (épaule)', '500 ml de yaourt jameed (ou labn épais)', '400 g de riz', 'Pain taboun', 'Amandes grillées', 'Pignons', 'Curcuma', 'Cardamome'],
     'etapes': ['Cuire l\'agneau dans l\'eau épicée 1h.', 'Délayer le jameed dans le bouillon, chauffer sans bouillir.', 'Cuire le riz au curcuma dans le bouillon.', 'Étaler pain, riz, agneau dans un grand plat.', 'Napper généreusement de sauce jameed. Garnir d\'amandes et pignons.'],
     'tags': ['Amman', 'National', 'Bédouin', 'Fête'], 'image_url': ''},
    {'titre': 'Knafeh', 'pays': 'jordan', 'type_plat': 'sucré',
     'description': 'Pâtisserie du Levant : fromage akkawi fondu sous une croûte de cheveux d\'ange dorés, nappée de sirop de rose.',
     'temps_preparation': 20, 'temps_cuisson': 30, 'nb_personnes': 12, 'difficulte': 'Moyen',
     'ingredients': ['500 g de cheveux d\'ange (kataïfi)', '250 g de beurre clarifié', '500 g de fromage akkawi', '300 g de sucre', '150 ml d\'eau', '1 c. eau de rose', 'Pistaches'],
     'etapes': ['Préparer le sirop : sucre, eau et eau de rose, cuire 10 min.', 'Mélanger kataïfi et beurre, presser la moitié dans le moule.', 'Étaler le fromage rincé et émietté.', 'Couvrir du reste de kataïfi, presser.', 'Cuire 25 min à 200°C. Napper de sirop chaud, garnir de pistaches.'],
     'tags': ['Amman', 'Fromage', 'Sirop de rose', 'Levant'], 'image_url': ''},

    # ── NEW ZEALAND ─────────────────────────────────────────────────────────────
    {'titre': 'Hāngī', 'pays': 'new zealand', 'type_plat': 'salé',
     'description': 'Cuisson maorie traditionnelle sous terre : agneau, poulet, kumara (patate douce) et légumes cuits à la vapeur de pierres chauffées.',
     'temps_preparation': 60, 'temps_cuisson': 180, 'nb_personnes': 10, 'difficulte': 'Difficile',
     'ingredients': ['1 kg d\'agneau', '1 kg de poulet', '500 g de kumara', '500 g de pommes de terre', '300 g de carottes', 'Chou', 'Sel'],
     'etapes': ['Chauffer des pierres dans un feu (version four : 180°C).', 'Envelopper viandes et légumes séparément dans du papier alu.', 'Disposer en couches dans le four.', 'Cuire 2-3h à couvert.', 'Servir avec pain rewena (pain maori).'],
     'tags': ['Auckland', 'Maori', 'Terre', 'Cérémonie'], 'image_url': ''},
    {'titre': 'Pavlova', 'pays': 'new zealand', 'type_plat': 'sucré',
     'description': 'Meringue géante croustillante dehors, moelleuse dedans, garnie de kiwis, fruits de la passion et crème fouettée.',
     'temps_preparation': 20, 'temps_cuisson': 90, 'nb_personnes': 8, 'difficulte': 'Moyen',
     'ingredients': ['4 blancs d\'œuf', '250 g de sucre fin', '1 c. vinaigre blanc', '1 c. Maïzena', '300 ml crème entière', '4 kiwis', '2 fruits de la passion', 'Fraises'],
     'etapes': ['Battre blancs en neige, ajouter sucre progressivement.', 'Incorporer vinaigre et Maïzena.', 'Étaler en disque épais sur papier cuisson.', 'Cuire 90 min à 120°C, laisser refroidir four éteint.', 'Garnir de crème fouettée et fruits frais.'],
     'tags': ['Auckland', 'Meringue', 'Kiwi', 'Été'], 'image_url': ''},

    # ── INDONESIA ───────────────────────────────────────────────────────────────
    {'titre': 'Nasi Goreng', 'pays': 'indonesia', 'type_plat': 'salé',
     'description': 'Le riz sauté indonésien, plat national : riz cuit de la veille, kecap manis (sauce soja sucrée), œuf au plat, saté.',
     'temps_preparation': 15, 'temps_cuisson': 15, 'nb_personnes': 4, 'difficulte': 'Facile',
     'ingredients': ['600 g de riz cuit (veille)', '3 c. kecap manis', '2 c. sauce soja', '4 gousses d\'ail', '4 échalotes', '2 piments', '2 œufs', '100 g de crevettes', 'Concombre', 'Chips de crevettes'],
     'etapes': ['Frire ail, échalotes et piments jusqu\'à dorure.', 'Ajouter crevettes, sauter 2 min.', 'Incorporer le riz froid, bien séparer les grains.', 'Arroser de kecap manis et sauce soja. Sauter fort.', 'Servir avec œuf au plat, concombre et chips.'],
     'tags': ['Jakarta', 'National', 'Kecap', 'Street food'], 'image_url': 'https://upload.wikimedia.org/wikipedia/commons/thumb/3/38/Nasi_goreng_special.jpg/800px-Nasi_goreng_special.jpg'},
    {'titre': 'Klepon', 'pays': 'indonesia', 'type_plat': 'sucré',
     'description': 'Boules de riz gluant vert (pandan) fourrées de sucre de palme, roulées dans la noix de coco râpée.',
     'temps_preparation': 30, 'temps_cuisson': 10, 'nb_personnes': 20, 'difficulte': 'Facile',
     'ingredients': ['300 g de farine de riz gluant', '150 ml de lait de coco', '2 c. pâte de pandan (ou jus)', 'Pincée sel', '100 g de sucre de palme (gula jawa)', '100 g de noix de coco râpée'],
     'etapes': ['Mélanger farine de riz, lait de coco, pandan et sel.', 'Former des boules, creuser le centre, glisser un morceau de sucre de palme.', 'Refermer hermétiquement.', 'Cuire dans l\'eau bouillante jusqu\'à ce qu\'elles remontent.', 'Rouler immédiatement dans la noix de coco râpée.'],
     'tags': ['Jakarta', 'Pandan', 'Vert', 'Marché'], 'image_url': ''},

    # ── TUNISIA ─────────────────────────────────────────────────────────────────
    {'titre': 'Brik à l\'Œuf', 'pays': 'tunisia', 'type_plat': 'salé',
     'description': 'Feuille de brik croustillante fourrée d\'un œuf coulant, thon, câpres et harissa — à manger d\'un coup pour ne pas perdre le jaune.',
     'temps_preparation': 10, 'temps_cuisson': 5, 'nb_personnes': 4, 'difficulte': 'Facile',
     'ingredients': ['4 feuilles de brik', '4 œufs', '150 g de thon en boîte', '2 c. câpres', '1 c. harissa', 'Persil haché', 'Huile de friture'],
     'etapes': ['Mélanger thon, câpres, harissa et persil.', 'Poser une feuille de brik, garnir de farce au centre.', 'Créer un creux, casser l\'œuf dedans.', 'Plier en triangle, sceller avec un peu d\'eau.', 'Frire 2 min dans l\'huile chaude. Servir immédiatement.'],
     'tags': ['Tunis', 'Œuf', 'Harissa', 'Croustillant'], 'image_url': ''},
    {'titre': 'Makroud', 'pays': 'tunisia', 'type_plat': 'sucré',
     'description': 'Gâteaux de semoule fourrés aux dattes et au citron, frits puis trempés dans le miel d\'orange.',
     'temps_preparation': 45, 'temps_cuisson': 20, 'nb_personnes': 20, 'difficulte': 'Moyen',
     'ingredients': ['500 g de semoule fine', '150 g de beurre', '200 ml d\'eau de fleur d\'oranger', '400 g de pâte de datte', 'Zeste de citron', '1 c. cannelle', 'Huile friture', '300 g de miel'],
     'etapes': ['Mélanger semoule et beurre fondu. Ajouter eau de fleur d\'oranger.', 'Pétrir en pâte souple. Reposer 30 min.', 'Assaisonner la pâte de dattes avec citron et cannelle.', 'Former des boudins de semoule, fourrer de dattes, couper en losanges.', 'Frire jusqu\'à dorure. Tremper chaud dans le miel.'],
     'tags': ['Kairouan', 'Dattes', 'Miel', 'Fête'], 'image_url': ''},

    # ── EL SALVADOR ─────────────────────────────────────────────────────────────
    {'titre': 'Pupusas', 'pays': 'el salvador', 'type_plat': 'salé',
     'description': 'Galettes épaisses de masa de maïs fourrées de fromage, haricots et chicharrón — plat national du Salvador.',
     'temps_preparation': 30, 'temps_cuisson': 20, 'nb_personnes': 4, 'difficulte': 'Facile',
     'ingredients': ['500 g de masa harina', '350 ml d\'eau tiède', '200 g de fromage fondant', '200 g de haricots rouges frits', '100 g de chicharrón (porc frit)', 'Curtido (salade de chou fermentée)'],
     'etapes': ['Mélanger masa et eau pour une pâte souple.', 'Former des boules, creuser le centre.', 'Farcir avec mélange fromage, haricots, chicharrón.', 'Refermer et aplatir délicatement.', 'Cuire sur comal 4 min de chaque côté. Servir avec curtido.'],
     'tags': ['San Salvador', 'National', 'Street food', 'Maïs'], 'image_url': ''},
    {'titre': 'Quesadilla Salvadoreña', 'pays': 'el salvador', 'type_plat': 'sucré',
     'description': 'Gâteau salvadorien à base de farine de riz, fromage et crème — rien à voir avec la tortilla mexicaine.',
     'temps_preparation': 20, 'temps_cuisson': 30, 'nb_personnes': 8, 'difficulte': 'Facile',
     'ingredients': ['250 g de farine de riz', '250 g de fromage sec râpé', '200 ml de crème fraîche', '3 œufs', '100 g de sucre', '50 g de beurre', '1 c. levure', 'Sésame'],
     'etapes': ['Battre œufs et sucre.', 'Ajouter fromage, crème et beurre fondu.', 'Incorporer farine de riz et levure.', 'Verser dans un moule rectangulaire.', 'Saupoudrer de sésame. Cuire 25-30 min à 180°C.'],
     'tags': ['San Salvador', 'Fromage', 'Riz', 'Petit-déjeuner'], 'image_url': ''},

    # ── ALBANIA ─────────────────────────────────────────────────────────────────
    {'titre': 'Tavë Kosi', 'pays': 'albania', 'type_plat': 'salé',
     'description': 'Casserole nationale albanaise : agneau et riz cuits sous une couverture de yaourt et œufs dorée au four.',
     'temps_preparation': 20, 'temps_cuisson': 60, 'nb_personnes': 6, 'difficulte': 'Facile',
     'ingredients': ['1 kg d\'agneau en cubes', '500 ml de yaourt grec', '3 œufs', '50 g de riz', '50 g de beurre', 'Sel', 'Poivre', 'Origan'],
     'etapes': ['Faire revenir l\'agneau dans le beurre.', 'Ajouter le riz, mélanger.', 'Verser dans un plat allant au four.', 'Battre yaourt et œufs, saler, verser sur l\'agneau.', 'Cuire 45 min à 180°C jusqu\'à coloration.'],
     'tags': ['Elbasan', 'National', 'Yaourt', 'Balkans'], 'image_url': ''},
    {'titre': 'Baklava Albanaise', 'pays': 'albania', 'type_plat': 'sucré',
     'description': 'Baklava balkanique : feuilles de filo beurrées, noix moulues et épices, imbibées de sirop de citron et miel.',
     'temps_preparation': 45, 'temps_cuisson': 40, 'nb_personnes': 20, 'difficulte': 'Moyen',
     'ingredients': ['500 g de feuilles de filo', '200 g de beurre clarifié', '400 g de noix moulues', '100 g de sucre', '1 c. cannelle', '1 c. cardamome', '300 g de miel', '150 ml d\'eau', 'Jus de citron'],
     'etapes': ['Beurrer le moule, alterner feuilles de filo et noix sucrées.', 'Finir avec 6 couches de filo beurré.', 'Couper en losanges avant de cuire.', 'Cuire 35-40 min à 170°C jusqu\'à dorure.', 'Napper de sirop miel-citron chaud à la sortie.'],
     'tags': ['Tirana', 'Noix', 'Balkans', 'Fête'], 'image_url': ''},
]


class Command(BaseCommand):
    help = 'Charge les recettes des pays WC 2026 manquants (Americas, Europe, Asie, Océanie)'

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
