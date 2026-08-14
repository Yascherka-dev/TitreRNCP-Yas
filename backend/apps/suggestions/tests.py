from decimal import Decimal
from rest_framework.test import APITestCase
from rest_framework import status
from apps.recipes.models import Recipe
from apps.beers.models import Beer


class SuggestionTests(APITestCase):

    def setUp(self):
        Recipe.objects.create(titre='Baguette',     pays='france', description='Pain',      temps_preparation=10, type_plat=Recipe.TYPE_SALE)
        Recipe.objects.create(titre='Paella',       pays='spain',  description='Riz',        temps_preparation=40, type_plat=Recipe.TYPE_SALE)
        Recipe.objects.create(titre='Crème brûlée', pays='france', description='Dessert',    temps_preparation=20, type_plat=Recipe.TYPE_SUCRE)
        Recipe.objects.create(titre='Churros',      pays='spain',  description='Beignets',   temps_preparation=15, type_plat=Recipe.TYPE_SUCRE)
        Beer.objects.create(nom='Kronenbourg',   brasserie='Kronenbourg SAS', pays='france', style='Lager', description='Bière française',  degre_alcool=Decimal('5.0'))
        Beer.objects.create(nom='Estrella Damm', brasserie='Damm',            pays='spain',  style='Lager', description='Bière espagnole', degre_alcool=Decimal('5.4'))

    def test_suggestions_returns_all_fields(self):
        response = self.client.post('/api/suggestions/', {'paysA': 'france', 'paysB': 'spain'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        for field in ['recette_a', 'recette_b', 'peche_mignon_a', 'peche_mignon_b', 'biere_a', 'biere_b']:
            self.assertIn(field, response.data)

    def test_suggestions_matches_requested_countries(self):
        response = self.client.post('/api/suggestions/', {'paysA': 'france', 'paysB': 'spain'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        if response.data['recette_a']:
            self.assertEqual(response.data['recette_a']['pays'], 'france')
        if response.data['recette_b']:
            self.assertEqual(response.data['recette_b']['pays'], 'spain')

    def test_suggestions_beers_match_countries(self):
        response = self.client.post('/api/suggestions/', {'paysA': 'france', 'paysB': 'spain'})
        if response.data['biere_a']:
            self.assertEqual(response.data['biere_a']['pays'], 'france')
        if response.data['biere_b']:
            self.assertEqual(response.data['biere_b']['pays'], 'spain')

    def test_missing_pays_a_returns_400(self):
        response = self.client.post('/api/suggestions/', {'paysB': 'spain'})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_missing_pays_b_returns_400(self):
        response = self.client.post('/api/suggestions/', {'paysA': 'france'})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_empty_payload_returns_400(self):
        response = self.client.post('/api/suggestions/', {})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_suggestions_is_public(self):
        response = self.client.post('/api/suggestions/', {'paysA': 'france', 'paysB': 'spain'})
        self.assertNotEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_unknown_country_returns_null_recipe(self):
        response = self.client.post('/api/suggestions/', {'paysA': 'narnia', 'paysB': 'mordor'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIsNone(response.data['recette_a'])
        self.assertIsNone(response.data['recette_b'])


class SameCountryVarietyTests(APITestCase):
    """
    95 % des matchs à venir opposent deux équipes du même pays : ligues
    domestiques, NBA, NFL, NHL. Sans précaution, les deux camps recevaient
    le même plat, ce qui vide la proposition de son sens.
    """

    def setUp(self):
        for i in range(1, 4):
            Recipe.objects.create(titre=f'Salé {i}',  pays='usa', description='x',
                                  temps_preparation=10, type_plat=Recipe.TYPE_SALE)
            Recipe.objects.create(titre=f'Sucré {i}', pays='usa', description='x',
                                  temps_preparation=10, type_plat=Recipe.TYPE_SUCRE)

    def test_deux_plats_differents_pour_un_match_domestique(self):
        for _ in range(15):  # le tirage est aléatoire : on répète
            r = self.client.post('/api/suggestions/', {
                'paysA': 'usa', 'paysB': 'usa',
                'equipeA': 'Los Angeles Lakers', 'equipeB': 'Boston Celtics',
            })
            self.assertEqual(r.status_code, status.HTTP_200_OK)
            self.assertNotEqual(r.data['recette_a']['id'], r.data['recette_b']['id'])
            self.assertNotEqual(r.data['peche_mignon_a']['id'], r.data['peche_mignon_b']['id'])

    def test_un_seul_plat_disponible_reste_servi_des_deux_cotes(self):
        # Mieux vaut répéter que renvoyer une carte vide.
        Recipe.objects.filter(pays='usa').delete()
        Recipe.objects.create(titre='Unique', pays='usa', description='x',
                              temps_preparation=10, type_plat=Recipe.TYPE_SALE)
        r = self.client.post('/api/suggestions/', {'paysA': 'usa', 'paysB': 'usa'})
        self.assertEqual(r.data['recette_a']['titre'], 'Unique')
        self.assertEqual(r.data['recette_b']['titre'], 'Unique')
