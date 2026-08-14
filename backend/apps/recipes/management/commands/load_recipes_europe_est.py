"""
Recettes des pays européens qui apparaissent dans les matchs suivis mais
n'avaient aucune entrée au catalogue — plus les deux desserts manquants
pour l'Autriche et la Suisse.

Sans ces recettes, SuggestionView renvoyait une carte vide pour 42 matchs,
sans lever d'erreur.
"""

from django.core.management.base import BaseCommand
from apps.recipes.models import Recipe

RECIPES = [
    # ── ISRAËL ──────────────────────────────────────────────────────────────────
    {'titre': 'Shakshuka', 'pays': 'israel', 'type_plat': 'salé',
     'description': 'Œufs pochés dans une sauce tomate au poivron et au cumin, servie brûlante à la poêle avec du pain pour saucer.',
     'temps_preparation': 15, 'temps_cuisson': 30, 'nb_personnes': 4, 'difficulte': 'Facile',
     'ingredients': ['6 œufs', '800 g de tomates concassées', '2 poivrons rouges', '1 oignon', '3 gousses d\'ail', '1 c. cumin moulu', '1 c. paprika fumé', 'Harissa', 'Coriandre fraîche', 'Huile d\'olive'],
     'etapes': ['Faire suer oignon et poivrons en lamelles 10 min.', 'Ajouter ail, cumin et paprika, laisser chanter 1 min.', 'Verser les tomates, mijoter 15 min jusqu\'à épaississement.', 'Creuser six puits, y casser les œufs.', 'Couvrir et cuire 6-8 min : le blanc pris, le jaune coulant.', 'Parsemer de coriandre, servir à la poêle avec du pain.'],
     'tags': ['Petit-déjeuner', 'Tel Aviv', 'Poêle unique'], 'image_url': ''},
    {'titre': 'Malabi', 'pays': 'israel', 'type_plat': 'sucré',
     'description': 'Crème de lait à la fleur d\'oranger, nappée de sirop de rose et de pistaches concassées. Servie très froide.',
     'temps_preparation': 15, 'temps_cuisson': 10, 'nb_personnes': 6, 'difficulte': 'Facile',
     'ingredients': ['1 L de lait', '80 g de maïzena', '100 g de sucre', '2 c. eau de fleur d\'oranger', 'Sirop de rose', '80 g de pistaches', 'Noix de coco râpée'],
     'etapes': ['Délayer la maïzena dans un verre de lait froid.', 'Chauffer le reste du lait avec le sucre.', 'Verser la maïzena en remuant, cuire jusqu\'à napper la cuillère.', 'Hors du feu, parfumer à la fleur d\'oranger.', 'Répartir en verrines, réfrigérer 3 h.', 'Napper de sirop de rose, pistaches et coco.'],
     'tags': ['Fleur d\'oranger', 'Verrine', 'Sans four'], 'image_url': ''},

    # ── BULGARIE ────────────────────────────────────────────────────────────────
    {'titre': 'Banitsa', 'pays': 'bulgaria', 'type_plat': 'salé',
     'description': 'Feuilleté roulé en spirale, garni de sirene — la feta bulgare — battue aux œufs et au yaourt.',
     'temps_preparation': 25, 'temps_cuisson': 40, 'nb_personnes': 6, 'difficulte': 'Moyen',
     'ingredients': ['500 g de feuilles de filo', '400 g de sirene (ou feta)', '4 œufs', '200 g de yaourt bulgare', '100 g de beurre fondu', '1 c. bicarbonate', 'Huile'],
     'etapes': ['Émietter le fromage, mélanger aux œufs et au yaourt battus.', 'Ajouter le bicarbonate, saler légèrement.', 'Badigeonner chaque feuille de filo de beurre, garnir, rouler en boudin.', 'Disposer les boudins en spirale dans un moule rond.', 'Badigeonner du reste de beurre.', 'Cuire 40 min à 180°C jusqu\'à dorure profonde.'],
     'tags': ['Sofia', 'Filo', 'Fromage', 'Traditionnel'], 'image_url': ''},
    {'titre': 'Garash', 'pays': 'bulgaria', 'type_plat': 'sucré',
     'description': 'Gâteau bulgare sans farine : disques de noix moulues et blancs en neige, montés à la ganache au chocolat noir.',
     'temps_preparation': 40, 'temps_cuisson': 30, 'nb_personnes': 10, 'difficulte': 'Moyen',
     'ingredients': ['300 g de noix moulues', '8 blancs d\'œufs', '200 g de sucre', '300 g de chocolat noir', '400 ml de crème liquide', '100 g de beurre', 'Cacao amer'],
     'etapes': ['Monter les blancs, serrer au sucre.', 'Incorporer les noix moulues à la maryse.', 'Étaler en quatre disques, cuire 12 min à 170°C chacun.', 'Chauffer la crème, verser sur le chocolat, ajouter le beurre.', 'Laisser tiédir la ganache jusqu\'à consistance tartinable.', 'Monter les disques en alternant, masquer et saupoudrer de cacao.'],
     'tags': ['Sans farine', 'Noix', 'Chocolat', 'Fête'], 'image_url': ''},

    # ── SUÈDE ───────────────────────────────────────────────────────────────────
    {'titre': 'Köttbullar', 'pays': 'sweden', 'type_plat': 'salé',
     'description': 'Boulettes de viande suédoises en sauce crémeuse, servies avec purée, airelles et concombre mariné.',
     'temps_preparation': 25, 'temps_cuisson': 25, 'nb_personnes': 4, 'difficulte': 'Facile',
     'ingredients': ['400 g de bœuf haché', '200 g de porc haché', '1 oignon', '80 g de chapelure', '150 ml de lait', '1 œuf', 'Piment de la Jamaïque', '30 g de beurre', '30 g de farine', '400 ml de bouillon de bœuf', '150 ml de crème', 'Confiture d\'airelles'],
     'etapes': ['Tremper la chapelure dans le lait 10 min.', 'Mêler viandes, oignon râpé, œuf, chapelure et piment.', 'Rouler des boulettes de la taille d\'une noix.', 'Dorer au beurre en plusieurs fournées, réserver.', 'Faire un roux dans la poêle, mouiller au bouillon puis à la crème.', 'Remettre les boulettes, mijoter 10 min. Servir avec les airelles.'],
     'tags': ['Stockholm', 'Réconfort', 'Airelles'], 'image_url': ''},
    {'titre': 'Kanelbullar', 'pays': 'sweden', 'type_plat': 'sucré',
     'description': 'Brioches roulées à la cannelle et à la cardamome, dorées et perlées de sucre. L\'institution du fika suédois.',
     'temps_preparation': 40, 'temps_cuisson': 12, 'nb_personnes': 16, 'difficulte': 'Moyen',
     'ingredients': ['500 g de farine', '250 ml de lait tiède', '25 g de levure fraîche', '80 g de sucre', '80 g de beurre', '1 c. cardamome moulue', '100 g de beurre mou (garniture)', '80 g de cassonade', '2 c. cannelle', 'Sucre perlé'],
     'etapes': ['Délayer la levure dans le lait tiède.', 'Pétrir farine, sucre, cardamome, beurre et lait 10 min.', 'Laisser lever 1 h à couvert.', 'Abaisser en rectangle, tartiner du beurre à la cannelle.', 'Rouler, trancher, façonner en nœuds sur plaque.', 'Laisser pousser 45 min, dorer à l\'œuf, sucre perlé.', 'Cuire 10-12 min à 220°C.'],
     'tags': ['Fika', 'Cardamome', 'Brioche'], 'image_url': ''},

    # ── ARMÉNIE ─────────────────────────────────────────────────────────────────
    {'titre': 'Khorovats', 'pays': 'armenia', 'type_plat': 'salé',
     'description': 'Le barbecue arménien : porc mariné à l\'oignon et au paprika, grillé en brochettes avec des légumes braisés à la flamme.',
     'temps_preparation': 30, 'temps_cuisson': 25, 'nb_personnes': 6, 'difficulte': 'Facile',
     'ingredients': ['1,2 kg d\'échine de porc', '3 oignons', '2 poivrons', '2 aubergines', '4 tomates', '2 c. paprika', 'Poivre noir concassé', '150 ml d\'eau gazeuse', 'Persil plat', 'Lavash'],
     'etapes': ['Tailler la viande en gros cubes de 4 cm.', 'Mariner 4 h avec oignons en rondelles, paprika, poivre et eau gazeuse.', 'Enfiler sur brochettes larges, sans serrer.', 'Griller sur braises 20 min en tournant régulièrement.', 'Braiser aubergines, poivrons et tomates entiers à côté.', 'Peler les légumes, hacher grossièrement, servir avec le lavash.'],
     'tags': ['Erevan', 'Braises', 'Convivial'], 'image_url': ''},
    {'titre': 'Gata', 'pays': 'armenia', 'type_plat': 'sucré',
     'description': 'Galette feuilletée arménienne fourrée de khoriz, un mélange sablé de beurre, farine et sucre. Décorée à la fourchette.',
     'temps_preparation': 35, 'temps_cuisson': 30, 'nb_personnes': 8, 'difficulte': 'Moyen',
     'ingredients': ['400 g de farine', '200 g de beurre', '150 g de yaourt', '1 œuf', '1 c. levure', '200 g de farine (khoriz)', '150 g de beurre mou (khoriz)', '150 g de sucre glace', '1 jaune d\'œuf'],
     'etapes': ['Pétrir farine, beurre, yaourt, œuf et levure. Reposer 1 h au frais.', 'Sabler du bout des doigts farine, beurre mou et sucre glace : c\'est le khoriz.', 'Abaisser la pâte, répartir le khoriz, rouler puis aplatir.', 'Dorer au jaune d\'œuf.', 'Rayer la surface à la fourchette en losanges.', 'Cuire 30 min à 180°C. Trancher tiède.'],
     'tags': ['Feuilleté', 'Fête', 'Traditionnel'], 'image_url': ''},

    # ── LITUANIE ────────────────────────────────────────────────────────────────
    {'titre': 'Cepelinai', 'pays': 'lithuania', 'type_plat': 'salé',
     'description': 'Quenelles de pomme de terre en forme de zeppelin, fourrées à la viande, nappées de lardons et de crème.',
     'temps_preparation': 50, 'temps_cuisson': 30, 'nb_personnes': 4, 'difficulte': 'Difficile',
     'ingredients': ['2 kg de pommes de terre', '400 g de porc haché', '1 oignon', '200 g de lardons fumés', '200 ml de crème épaisse', '2 c. fécule', 'Marjolaine', 'Aneth'],
     'etapes': ['Râper finement les trois quarts des pommes de terre, presser pour extraire l\'eau.', 'Laisser décanter l\'eau, récupérer la fécule au fond et la remettre dans la râpure.', 'Cuire et écraser le quart restant, mêler aux crues.', 'Assaisonner la viande à l\'oignon et à la marjolaine.', 'Former des quenelles autour de la farce, bien sceller.', 'Pocher 25-30 min à frémissement dans l\'eau salée.', 'Napper de lardons rissolés et de crème, parsemer d\'aneth.'],
     'tags': ['Vilnius', 'Pomme de terre', 'Copieux'], 'image_url': ''},
    {'titre': 'Tinginys', 'pays': 'lithuania', 'type_plat': 'sucré',
     'description': 'Le « paresseux » lituanien : biscuits concassés pris dans un chocolat au lait concentré. Aucune cuisson.',
     'temps_preparation': 20, 'temps_cuisson': 0, 'nb_personnes': 12, 'difficulte': 'Facile',
     'ingredients': ['400 g de biscuits secs', '200 g de beurre', '400 g de lait concentré sucré', '80 g de cacao amer', '100 g de noix concassées', '1 pincée de sel'],
     'etapes': ['Concasser les biscuits en morceaux irréguliers.', 'Fondre le beurre à feu doux, incorporer le cacao tamisé.', 'Verser le lait concentré, lisser hors du feu.', 'Mélanger biscuits et noix à la préparation.', 'Rouler en boudin serré dans du film alimentaire.', 'Réfrigérer 4 h, trancher épais.'],
     'tags': ['Sans cuisson', 'Chocolat', 'Enfance'], 'image_url': ''},

    # ── ROUMANIE ────────────────────────────────────────────────────────────────
    {'titre': 'Sarmale', 'pays': 'romania', 'type_plat': 'salé',
     'description': 'Feuilles de chou aigre roulées autour d\'une farce de porc et de riz, mijotées des heures avec du lard fumé.',
     'temps_preparation': 45, 'temps_cuisson': 150, 'nb_personnes': 6, 'difficulte': 'Moyen',
     'ingredients': ['1 chou aigre entier', '600 g de porc haché', '150 g de riz', '2 oignons', '200 g de poitrine fumée', '400 g de tomates concassées', 'Aneth', 'Thym', 'Feuilles de laurier', 'Crème aigre'],
     'etapes': ['Séparer les feuilles de chou, ôter les côtes épaisses.', 'Suer les oignons, mêler au porc, au riz cru et à l\'aneth.', 'Garnir chaque feuille, rouler serré en repliant les côtés.', 'Tapisser la cocotte de chou haché et de lard.', 'Ranger les rouleaux en couches, intercaler tomates et laurier.', 'Couvrir d\'eau à hauteur, mijoter 2 h 30 à feu très doux.', 'Servir avec crème aigre et polenta.'],
     'tags': ['Fête', 'Chou', 'Mijoté', 'Noël'], 'image_url': ''},
    {'titre': 'Papanași', 'pays': 'romania', 'type_plat': 'sucré',
     'description': 'Beignets de fromage frais en forme d\'anneau, coiffés de leur boule, servis chauds sous la crème et la confiture de myrtilles.',
     'temps_preparation': 25, 'temps_cuisson': 15, 'nb_personnes': 4, 'difficulte': 'Moyen',
     'ingredients': ['500 g de fromage blanc égoutté', '2 œufs', '200 g de farine', '80 g de semoule fine', '1 c. levure', 'Zeste de citron', '60 g de sucre', 'Huile de friture', '300 g de crème aigre', 'Confiture de myrtilles'],
     'etapes': ['Mêler fromage, œufs, sucre et zeste.', 'Incorporer farine, semoule et levure jusqu\'à une pâte souple.', 'Façonner des anneaux et de petites boules.', 'Frire à 170°C 3-4 min par face jusqu\'à dorure.', 'Égoutter sur papier absorbant.', 'Poser la boule sur l\'anneau, napper de crème et de myrtilles.'],
     'tags': ['Beignet', 'Fromage frais', 'Myrtille'], 'image_url': ''},

    # ── ÎLES FÉROÉ ──────────────────────────────────────────────────────────────
    {'titre': 'Knettir', 'pays': 'faroe islands', 'type_plat': 'salé',
     'description': 'Boulettes de poisson féroïennes liées au suif et à l\'orge, pochées dans un bouillon de légumes racines.',
     'temps_preparation': 30, 'temps_cuisson': 30, 'nb_personnes': 4, 'difficulte': 'Moyen',
     'ingredients': ['600 g de filets de cabillaud', '100 g de suif de mouton (ou beurre froid)', '80 g de farine d\'orge', '1 oignon', '4 pommes de terre', '2 carottes', '1 navet', 'Poivre blanc', 'Sel'],
     'etapes': ['Hacher finement le poisson au couteau.', 'Mêler au suif froid râpé, à l\'oignon haché et à la farine d\'orge.', 'Assaisonner généreusement, former des boulettes fermes.', 'Porter à frémissement un bouillon avec les légumes taillés en gros dés.', 'Cuire les légumes 15 min.', 'Pocher les boulettes 15 min sans bouillir.', 'Servir dans le bouillon brûlant.'],
     'tags': ['Tórshavn', 'Poisson', 'Atlantique Nord'], 'image_url': ''},
    {'titre': 'Rabarbugreytur', 'pays': 'faroe islands', 'type_plat': 'sucré',
     'description': 'Compotée de rhubarbe des îles, à peine liée, servie glacée sous un voile de crème fraîche non sucrée.',
     'temps_preparation': 10, 'temps_cuisson': 20, 'nb_personnes': 6, 'difficulte': 'Facile',
     'ingredients': ['1 kg de rhubarbe', '200 g de sucre', '200 ml d\'eau', '2 c. fécule de pomme de terre', '1 gousse de vanille', '300 ml de crème fraîche'],
     'etapes': ['Tronçonner la rhubarbe en bâtonnets de 2 cm.', 'Cuire avec l\'eau, le sucre et la vanille 15 min à couvert.', 'Délayer la fécule dans un peu d\'eau froide.', 'Verser en filet hors du feu, remuer : la compote doit napper sans figer.', 'Refroidir puis réfrigérer 3 h.', 'Servir en coupes, crème froide versée en surface.'],
     'tags': ['Rhubarbe', 'Sans four', 'Été'], 'image_url': ''},

    # ── ISLANDE ─────────────────────────────────────────────────────────────────
    {'titre': 'Kjötsúpa', 'pays': 'iceland', 'type_plat': 'salé',
     'description': 'Soupe d\'agneau islandaise aux légumes racines et au riz, mijotée sans épices superflues. Le plat des jours de vent.',
     'temps_preparation': 20, 'temps_cuisson': 90, 'nb_personnes': 6, 'difficulte': 'Facile',
     'ingredients': ['1 kg de collier d\'agneau', '4 pommes de terre', '3 carottes', '1 rutabaga', '1 poireau', '1 oignon', '100 g de riz', 'Thym', 'Poivre', 'Sel'],
     'etapes': ['Couvrir l\'agneau d\'eau froide, porter à frémissement, écumer.', 'Mijoter 1 h à couvert avec l\'oignon et le thym.', 'Ajouter rutabaga et carottes en gros morceaux, cuire 20 min.', 'Ajouter pommes de terre, poireau et riz, cuire 20 min de plus.', 'Rectifier l\'assaisonnement, la soupe doit rester franche.', 'Servir brûlant, avec du pain de seigle beurré.'],
     'tags': ['Reykjavik', 'Agneau', 'Hiver', 'Une casserole'], 'image_url': ''},
    {'titre': 'Kleinur', 'pays': 'iceland', 'type_plat': 'sucré',
     'description': 'Beignets torsadés à la cardamome, frits jusqu\'à ce qu\'ils gonflent. Le goûter islandais par excellence.',
     'temps_preparation': 30, 'temps_cuisson': 15, 'nb_personnes': 20, 'difficulte': 'Moyen',
     'ingredients': ['500 g de farine', '120 g de sucre', '1 c. levure chimique', '1 c. cardamome moulue', '50 g de beurre fondu', '2 œufs', '150 ml de babeurre', 'Huile de friture'],
     'etapes': ['Mêler farine, sucre, levure et cardamome.', 'Ajouter beurre, œufs et babeurre, pétrir brièvement.', 'Reposer 30 min au frais.', 'Abaisser sur 5 mm, découper des losanges.', 'Fendre chaque losange au centre, passer une pointe dans la fente pour torsader.', 'Frire à 180°C 1-2 min par face.', 'Égoutter, servir tièdes.'],
     'tags': ['Cardamome', 'Beignet', 'Goûter'], 'image_url': ''},

    # ── GIBRALTAR ───────────────────────────────────────────────────────────────
    {'titre': 'Calentita', 'pays': 'gibraltar', 'type_plat': 'salé',
     'description': 'Le plat national de Gibraltar : galette de farine de pois chiche cuite au four, croustillante dessus, fondante dedans.',
     'temps_preparation': 10, 'temps_cuisson': 45, 'nb_personnes': 6, 'difficulte': 'Facile',
     'ingredients': ['250 g de farine de pois chiche', '750 ml d\'eau', '80 ml d\'huile d\'olive', '1 c. sel', 'Poivre noir moulu généreusement'],
     'etapes': ['Fouetter farine de pois chiche et eau sans grumeaux.', 'Laisser reposer 30 min, écumer la mousse en surface.', 'Ajouter l\'huile et le sel, mélanger.', 'Verser dans un plat huilé sur 2 cm d\'épaisseur.', 'Cuire 45 min à 200°C : le dessus doit brunir par plaques.', 'Poivrer largement, découper en carrés, manger à la main.'],
     'tags': ['National', 'Pois chiche', 'Sans gluten'], 'image_url': ''},
    {'titre': 'Japonesa', 'pays': 'gibraltar', 'type_plat': 'sucré',
     'description': 'Brioche frite de Gibraltar fourrée à la crème pâtissière et glacée d\'un fondant rose vif.',
     'temps_preparation': 40, 'temps_cuisson': 15, 'nb_personnes': 12, 'difficulte': 'Moyen',
     'ingredients': ['500 g de farine', '250 ml de lait tiède', '20 g de levure fraîche', '80 g de sucre', '80 g de beurre', '2 œufs', '500 ml de crème pâtissière', '250 g de sucre glace', 'Colorant rose', 'Huile de friture'],
     'etapes': ['Pétrir une pâte à brioche, laisser doubler 1 h 30.', 'Détailler des boules de 60 g, laisser pousser 45 min.', 'Frire à 170°C 2 min par face.', 'Refroidir, fendre et garnir de crème pâtissière à la poche.', 'Délayer le sucre glace en fondant, teinter en rose.', 'Napper le dessus, laisser prendre 20 min.'],
     'tags': ['Brioche', 'Crème', 'Emblématique'], 'image_url': ''},

    # ── IRLANDE DU NORD ─────────────────────────────────────────────────────────
    {'titre': 'Ulster Fry', 'pays': 'northern ireland', 'type_plat': 'salé',
     'description': 'Le grand petit-déjeuner nord-irlandais : ce qui le distingue du fry irlandais, c\'est le soda farl et le potato bread poêlés.',
     'temps_preparation': 20, 'temps_cuisson': 25, 'nb_personnes': 4, 'difficulte': 'Facile',
     'ingredients': ['8 saucisses de porc', '8 tranches de bacon', '4 œufs', '4 soda farls', '4 potato breads', '200 g de black pudding', '4 tomates', '250 g de champignons', 'Beurre'],
     'etapes': ['Rissoler les saucisses à feu moyen 12 min, réserver au chaud.', 'Cuire le bacon jusqu\'à ce qu\'il craque, puis le black pudding.', 'Poêler soda farls et potato breads dans la graisse rendue, 2 min par face.', 'Faire revenir champignons et tomates coupées en deux.', 'Cuire les œufs au plat en dernier.', 'Dresser tous les éléments côte à côte, sans les empiler.'],
     'tags': ['Belfast', 'Petit-déjeuner', 'Copieux'], 'image_url': ''},
    {'titre': 'Fifteens', 'pays': 'northern ireland', 'type_plat': 'sucré',
     'description': 'Roulé sans cuisson à quinze de chaque : quinze biscuits, quinze chamallows, quinze cerises confites, roulé dans la noix de coco.',
     'temps_preparation': 20, 'temps_cuisson': 0, 'nb_personnes': 10, 'difficulte': 'Facile',
     'ingredients': ['15 biscuits digestive', '15 chamallows', '15 cerises confites', '200 ml de lait concentré sucré', '100 g de noix de coco râpée'],
     'etapes': ['Écraser les biscuits en miettes grossières.', 'Couper chamallows et cerises en quatre.', 'Mêler le tout, lier au lait concentré.', 'Étaler la noix de coco sur du film alimentaire.', 'Former un boudin et le rouler dans la coco.', 'Serrer dans le film, réfrigérer 3 h, trancher en rondelles.'],
     'tags': ['Sans cuisson', 'Coco', 'Enfance'], 'image_url': ''},

    # ── FINLANDE ────────────────────────────────────────────────────────────────
    {'titre': 'Lohikeitto', 'pays': 'finland', 'type_plat': 'salé',
     'description': 'Soupe finlandaise au saumon et à la crème, généreuse en aneth, montée avec un peu de beurre en fin de cuisson.',
     'temps_preparation': 15, 'temps_cuisson': 25, 'nb_personnes': 4, 'difficulte': 'Facile',
     'ingredients': ['600 g de pavé de saumon sans peau', '600 g de pommes de terre', '1 poireau', '2 carottes', '1 L de fumet de poisson', '250 ml de crème liquide', '40 g de beurre', 'Aneth', 'Grains de piment de la Jamaïque'],
     'etapes': ['Tailler pommes de terre et carottes en cubes réguliers.', 'Cuire dans le fumet avec le piment 15 min.', 'Ajouter le poireau émincé, cuire 3 min.', 'Détailler le saumon en gros cubes, l\'ajouter hors ébullition.', 'Verser la crème, laisser frémir 5 min sans bouillir.', 'Monter au beurre, couvrir d\'aneth ciselé.'],
     'tags': ['Helsinki', 'Saumon', 'Aneth', 'Réconfort'], 'image_url': ''},
    {'titre': 'Korvapuusti', 'pays': 'finland', 'type_plat': 'sucré',
     'description': 'Brioches finlandaises à la cannelle, pincées en « gifles » qui font ressortir la spirale sur les côtés.',
     'temps_preparation': 40, 'temps_cuisson': 15, 'nb_personnes': 16, 'difficulte': 'Moyen',
     'ingredients': ['550 g de farine', '250 ml de lait tiède', '25 g de levure fraîche', '80 g de sucre', '1 c. cardamome moulue', '75 g de beurre', '1 œuf', '100 g de beurre mou (garniture)', '80 g de cassonade', '2 c. cannelle', 'Sucre perlé'],
     'etapes': ['Délayer la levure dans le lait tiède.', 'Pétrir avec farine, sucre, cardamome, œuf et beurre 10 min.', 'Lever 1 h à couvert.', 'Abaisser en rectangle, tartiner beurre, cassonade et cannelle.', 'Rouler, couper en triangles biseautés.', 'Pincer chaque triangle au centre pour ouvrir la spirale.', 'Pousser 30 min, dorer, sucre perlé, cuire 12 min à 225°C.'],
     'tags': ['Cannelle', 'Cardamome', 'Café'], 'image_url': ''},

    # ── BIÉLORUSSIE ─────────────────────────────────────────────────────────────
    {'titre': 'Draniki', 'pays': 'belarus', 'type_plat': 'salé',
     'description': 'Galettes de pomme de terre râpée, dorées à la poêle, servies brûlantes sous la smetana. Le plat national biélorusse.',
     'temps_preparation': 20, 'temps_cuisson': 20, 'nb_personnes': 4, 'difficulte': 'Facile',
     'ingredients': ['1 kg de pommes de terre à chair farineuse', '1 oignon', '1 œuf', '2 c. farine', 'Huile', 'Poivre', 'Sel', '250 g de smetana (crème aigre)'],
     'etapes': ['Râper finement pommes de terre et oignon.', 'Presser la râpure dans un linge pour extraire le maximum d\'eau.', 'Lier à l\'œuf et à la farine, assaisonner.', 'Chauffer une bonne épaisseur d\'huile.', 'Déposer des cuillerées aplaties, cuire 4 min par face jusqu\'à croustillance.', 'Égoutter et servir aussitôt avec la crème aigre.'],
     'tags': ['Minsk', 'Pomme de terre', 'National'], 'image_url': ''},
    {'titre': 'Kulaga', 'pays': 'belarus', 'type_plat': 'sucré',
     'description': 'Dessert paysan biélorusse : baies des bois épaissies à la farine de seigle et adoucies au miel.',
     'temps_preparation': 10, 'temps_cuisson': 25, 'nb_personnes': 6, 'difficulte': 'Facile',
     'ingredients': ['700 g de baies mêlées (myrtilles, framboises, groseilles)', '400 ml d\'eau', '80 g de farine de seigle', '120 g de miel', '1 pincée de sel'],
     'etapes': ['Porter les baies à ébullition avec l\'eau, cuire 10 min.', 'Écraser grossièrement au presse-purée.', 'Délayer la farine de seigle dans un peu d\'eau froide.', 'Verser en filet dans les baies en fouettant.', 'Cuire 10 min à feu doux jusqu\'à épaississement.', 'Sucrer au miel hors du feu, servir tiède ou froid.'],
     'tags': ['Baies', 'Miel', 'Rustique'], 'image_url': ''},

    # ── MONTÉNÉGRO ──────────────────────────────────────────────────────────────
    {'titre': 'Njeguški Stek', 'pays': 'montenegro', 'type_plat': 'salé',
     'description': 'Escalope de veau farcie au jambon fumé de Njeguši et au fromage local, panée puis rissolée au beurre.',
     'temps_preparation': 25, 'temps_cuisson': 20, 'nb_personnes': 4, 'difficulte': 'Moyen',
     'ingredients': ['4 escalopes de veau de 180 g', '150 g de pršut (jambon fumé)', '150 g de fromage de Njeguši (ou kachkaval)', '2 œufs', '100 g de farine', '150 g de chapelure', '60 g de beurre', 'Huile', 'Citron'],
     'etapes': ['Aplatir les escalopes entre deux films, sans les déchirer.', 'Garnir la moitié de chaque escalope de jambon et de fromage.', 'Replier, sceller les bords en pressant fermement.', 'Passer dans la farine, l\'œuf battu puis la chapelure.', 'Rissoler 5 min par face dans un mélange beurre-huile.', 'Terminer 5 min au four à 180°C. Servir avec un quartier de citron.'],
     'tags': ['Njeguši', 'Veau', 'Fumé'], 'image_url': ''},
    {'titre': 'Priganice', 'pays': 'montenegro', 'type_plat': 'sucré',
     'description': 'Petits beignets monténégrins levés, croustillants dehors et aériens dedans, servis au miel et au fromage frais.',
     'temps_preparation': 20, 'temps_cuisson': 15, 'nb_personnes': 6, 'difficulte': 'Facile',
     'ingredients': ['400 g de farine', '300 ml d\'eau tiède', '15 g de levure fraîche', '1 c. sucre', '1 c. sel', 'Huile de friture', 'Miel de montagne', '200 g de fromage frais', 'Sucre glace'],
     'etapes': ['Délayer levure et sucre dans l\'eau tiède, laisser mousser 10 min.', 'Mêler à la farine et au sel : la pâte doit rester très souple, presque coulante.', 'Laisser lever 1 h à couvert.', 'Prélever des cuillerées et les jeter dans l\'huile à 175°C.', 'Frire 3 min en retournant, jusqu\'à dorure uniforme.', 'Égoutter, servir brûlants avec miel et fromage frais.'],
     'tags': ['Beignet', 'Miel', 'Partage'], 'image_url': ''},

    # ── MOLDAVIE ────────────────────────────────────────────────────────────────
    {'titre': 'Mămăligă cu Brânză', 'pays': 'moldova', 'type_plat': 'salé',
     'description': 'Polenta moldave ferme, servie en tranches avec brânză de brebis, crème aigre et lardons croustillants.',
     'temps_preparation': 10, 'temps_cuisson': 35, 'nb_personnes': 4, 'difficulte': 'Facile',
     'ingredients': ['300 g de semoule de maïs', '1,2 L d\'eau', '1 c. sel', '200 g de brânză (ou feta de brebis)', '200 g de smântână (crème aigre)', '150 g de lardons fumés', '30 g de beurre'],
     'etapes': ['Porter l\'eau salée à ébullition.', 'Verser la semoule en pluie en fouettant sans arrêt.', 'Cuire 30 min à feu doux, en remuant à la cuillère de bois.', 'La mămăligă est prête quand elle se détache des parois.', 'Renverser sur une planche, laisser prendre 5 min, trancher au fil.', 'Servir avec fromage émietté, crème et lardons rissolés.'],
     'tags': ['Chișinău', 'Maïs', 'Fromage de brebis'], 'image_url': ''},
    {'titre': 'Plăcintă cu Mere', 'pays': 'moldova', 'type_plat': 'sucré',
     'description': 'Galette moldave à la pâte étirée très fine, garnie de pommes râpées à la cannelle, dorée à la poêle.',
     'temps_preparation': 40, 'temps_cuisson': 20, 'nb_personnes': 6, 'difficulte': 'Moyen',
     'ingredients': ['400 g de farine', '200 ml d\'eau tiède', '60 ml d\'huile', '1 c. sel', '5 pommes', '80 g de sucre', '1 c. cannelle', '50 g de chapelure', 'Beurre'],
     'etapes': ['Pétrir farine, eau, huile et sel jusqu\'à une pâte lisse. Reposer 30 min sous un bol chaud.', 'Râper les pommes, mêler sucre, cannelle et chapelure.', 'Étirer chaque pâton à la main jusqu\'à transparence.', 'Répartir la garniture, replier les bords en carré.', 'Cuire à la poêle beurrée 5 min par face à feu moyen.', 'Saupoudrer de sucre, servir tiède.'],
     'tags': ['Pomme', 'Pâte étirée', 'Goûter'], 'image_url': ''},

    # ── LUXEMBOURG ──────────────────────────────────────────────────────────────
    {'titre': 'Judd mat Gaardebounen', 'pays': 'luxembourg', 'type_plat': 'salé',
     'description': 'Le plat national luxembourgeois : collet de porc fumé dessalé puis mijoté, servi avec des fèves des marais à la crème.',
     'temps_preparation': 20, 'temps_cuisson': 120, 'nb_personnes': 6, 'difficulte': 'Moyen',
     'ingredients': ['1,5 kg de collet de porc fumé', '800 g de fèves des marais écossées', '200 g de lardons', '1 oignon', '2 carottes', '1 bouquet garni', '200 ml de crème', '30 g de farine', 'Sarriette', 'Pommes de terre'],
     'etapes': ['Dessaler la viande 12 h à l\'eau froide, changer l\'eau deux fois.', 'Couvrir d\'eau fraîche avec oignon, carottes et bouquet garni.', 'Mijoter 2 h à petits frémissements.', 'Cuire les fèves 15 min, les dérober si la peau est épaisse.', 'Rissoler les lardons, singer à la farine, mouiller au bouillon de cuisson.', 'Ajouter crème, fèves et sarriette, mijoter 10 min.', 'Trancher la viande, napper de fèves, servir avec pommes vapeur.'],
     'tags': ['National', 'Fumé', 'Fèves', 'Hiver'], 'image_url': ''},
    {'titre': 'Quetschentaart', 'pays': 'luxembourg', 'type_plat': 'sucré',
     'description': 'Tarte luxembourgeoise aux quetsches serrées debout sur une pâte levée, à peine sucrée pour laisser parler le fruit.',
     'temps_preparation': 35, 'temps_cuisson': 40, 'nb_personnes': 8, 'difficulte': 'Facile',
     'ingredients': ['300 g de farine', '120 ml de lait tiède', '15 g de levure fraîche', '60 g de sucre', '60 g de beurre', '1 œuf', '1,2 kg de quetsches', '40 g de chapelure', 'Cannelle', 'Sucre glace'],
     'etapes': ['Pétrir une pâte levée, laisser doubler 1 h.', 'Dénoyauter les quetsches, les ouvrir sans les séparer.', 'Abaisser la pâte dans un moule, parsemer de chapelure : elle boira le jus.', 'Ranger les quetsches serrées, debout, chair vers le haut.', 'Saupoudrer de sucre et de cannelle.', 'Cuire 40 min à 190°C. Sucre glace une fois tiède.'],
     'tags': ['Quetsche', 'Automne', 'Pâte levée'], 'image_url': ''},

    # ── AUTRICHE — dessert manquant ─────────────────────────────────────────────
    {'titre': 'Sachertorte', 'pays': 'austria', 'type_plat': 'sucré',
     'description': 'Le gâteau viennois : biscuit au chocolat noir, fine couche d\'abricot, glaçage miroir. Servi avec une crème fouettée non sucrée.',
     'temps_preparation': 45, 'temps_cuisson': 45, 'nb_personnes': 12, 'difficulte': 'Difficile',
     'ingredients': ['140 g de chocolat noir 55%', '140 g de beurre', '110 g de sucre glace', '6 œufs', '110 g de sucre', '140 g de farine', '200 g de confiture d\'abricot', '200 g de chocolat noir (glaçage)', '250 g de sucre', '150 ml d\'eau', 'Crème fouettée'],
     'etapes': ['Fondre le chocolat, crémer beurre et sucre glace, ajouter les jaunes un à un.', 'Monter les blancs en serrant au sucre.', 'Incorporer chocolat fondu, blancs et farine tamisée en alternance.', 'Cuire 45 min à 170°C, refroidir sur grille 12 h.', 'Trancher en deux, garnir et masquer de confiture chauffée.', 'Cuire sucre et eau à 108°C, verser sur le chocolat, lisser.', 'Napper en une seule fois, laisser prendre sans toucher.'],
     'tags': ['Vienne', 'Chocolat', 'Abricot', 'Emblématique'], 'image_url': ''},

    # ── SUISSE — dessert manquant ───────────────────────────────────────────────
    {'titre': 'Bündner Nusstorte', 'pays': 'switzerland', 'type_plat': 'sucré',
     'description': 'Tourte des Grisons : pâte sablée épaisse refermée sur des noix prises dans un caramel à la crème.',
     'temps_preparation': 40, 'temps_cuisson': 40, 'nb_personnes': 10, 'difficulte': 'Moyen',
     'ingredients': ['400 g de farine', '250 g de beurre', '150 g de sucre', '1 œuf', '1 pincée de sel', '300 g de cerneaux de noix', '250 g de sucre (caramel)', '200 ml de crème entière', '30 g de miel'],
     'etapes': ['Sabler farine, beurre et sucre, lier à l\'œuf. Reposer 1 h au frais.', 'Caraméliser le sucre à sec jusqu\'à ambre foncé.', 'Décuire à la crème chaude, hors du feu, avec précaution.', 'Ajouter miel et noix concassées, laisser refroidir complètement.', 'Foncer un moule, garnir de la masse aux noix.', 'Couvrir d\'un second disque, souder les bords, piquer le dessus.', 'Cuire 40 min à 180°C. Attendre 24 h avant de trancher.'],
     'tags': ['Grisons', 'Noix', 'Caramel', 'Se conserve'], 'image_url': ''},
]


class Command(BaseCommand):
    help = "Charge les recettes des pays européens absents du catalogue (+ desserts Autriche et Suisse)"

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
