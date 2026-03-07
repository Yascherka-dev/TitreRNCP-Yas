from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from rest_framework import status
import random


MOCK_RECIPES = {
    'fr': [
        {'titre': 'Boeuf Bourguignon', 'pays': 'fr', 'description': 'Mijoté de boeuf au vin rouge', 'temps_preparation': 120, 'ingredients': ['boeuf', 'vin rouge', 'carottes', 'oignons'], 'etapes': ['Faire revenir la viande', 'Ajouter les légumes', 'Mijoter 2h'], 'image_url': ''},
        {'titre': 'Ratatouille', 'pays': 'fr', 'description': 'Légumes provençaux mijotés', 'temps_preparation': 45, 'ingredients': ['courgettes', 'aubergines', 'tomates', 'poivrons'], 'etapes': ['Couper les légumes', 'Faire revenir', 'Mijoter'], 'image_url': ''},
    ],
    'de': [
        {'titre': 'Bratwurst & Choucroute', 'pays': 'de', 'description': 'Saucisses grillées avec choucroute', 'temps_preparation': 30, 'ingredients': ['bratwurst', 'choucroute', 'moutarde'], 'etapes': ['Griller les saucisses', 'Chauffer la choucroute', 'Servir'], 'image_url': ''},
    ],
    'es': [
        {'titre': 'Paella Valenciana', 'pays': 'es', 'description': 'Riz safranné aux fruits de mer', 'temps_preparation': 60, 'ingredients': ['riz', 'safran', 'poulet', 'crevettes'], 'etapes': ['Faire revenir', 'Ajouter le riz', 'Cuire 20min'], 'image_url': ''},
    ],
    'gb-eng': [
        {'titre': 'Fish & Chips', 'pays': 'gb-eng', 'description': 'Poisson frit et frites croustillantes', 'temps_preparation': 40, 'ingredients': ['cabillaud', 'pommes de terre', 'farine', 'bière'], 'etapes': ['Préparer la pâte', 'Frire le poisson', 'Frire les frites'], 'image_url': ''},
    ],
    'it': [
        {'titre': 'Risotto alla Milanese', 'pays': 'it', 'description': 'Risotto crémeux au safran', 'temps_preparation': 35, 'ingredients': ['riz arborio', 'safran', 'parmesan', 'beurre'], 'etapes': ['Faire revenir l\'oignon', 'Ajouter le riz', 'Incorporer le bouillon'], 'image_url': ''},
    ],
    'pt': [
        {'titre': 'Bacalhau à Brás', 'pays': 'pt', 'description': 'Morue effilochée aux oeufs et pommes de terre', 'temps_preparation': 40, 'ingredients': ['morue', 'oeufs', 'pommes de terre', 'olives'], 'etapes': ['Dessaler la morue', 'Frire les pommes de terre', 'Mélanger avec les oeufs'], 'image_url': ''},
    ],
    'ar': [
        {'titre': 'Asado Argentin', 'pays': 'ar', 'description': 'Barbecue traditionnel argentin', 'temps_preparation': 90, 'ingredients': ['côtes de boeuf', 'chimichurri', 'sel'], 'etapes': ['Préparer les braises', 'Griller la viande', 'Servir avec chimichurri'], 'image_url': ''},
    ],
}

DEFAULT_RECIPE = {'titre': 'Plat du monde', 'pays': 'world', 'description': 'Recette internationale', 'temps_preparation': 30, 'ingredients': ['ingrédients variés'], 'etapes': ['Cuisiner avec amour'], 'image_url': ''}


class SuggestionView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        pays_a = request.data.get('paysA')
        pays_b = request.data.get('paysB')

        if not pays_a or not pays_b:
            return Response({'error': 'paysA et paysB sont requis'}, status=status.HTTP_400_BAD_REQUEST)

        recettes_a = MOCK_RECIPES.get(pays_a, [DEFAULT_RECIPE])
        recettes_b = MOCK_RECIPES.get(pays_b, [DEFAULT_RECIPE])

        return Response({
            'recettes': [
                random.choice(recettes_a),
                random.choice(recettes_b),
            ]
        })
