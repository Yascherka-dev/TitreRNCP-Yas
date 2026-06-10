from rest_framework.test import APITestCase
from rest_framework import status
from apps.recipes.models import Recipe


class RecipeTests(APITestCase):

    def setUp(self):
        Recipe.objects.create(
            titre='Bœuf bourguignon',
            pays='france',
            description='Un grand classique de la cuisine française.',
            temps_preparation=30,
            temps_cuisson=120,
            nb_personnes=4,
            type_plat=Recipe.TYPE_SALE,
            difficulte='Moyen',
            tags=['boeuf', 'vin', 'mijote'],
        )
        Recipe.objects.create(
            titre='Crème brûlée',
            pays='france',
            description='Dessert à la vanille avec croûte caramélisée.',
            temps_preparation=20,
            temps_cuisson=40,
            type_plat=Recipe.TYPE_SUCRE,
            difficulte='Facile',
        )

    def test_list_recipes_is_public(self):
        response = self.client.get('/api/recipes/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIsInstance(response.data, list)
        self.assertGreaterEqual(len(response.data), 2)

    def test_recipe_contains_required_fields(self):
        response = self.client.get('/api/recipes/')
        recipe = response.data[0]
        for field in ['id', 'titre', 'pays', 'type_plat', 'difficulte', 'description']:
            self.assertIn(field, recipe)

    def test_recipes_include_both_types(self):
        response = self.client.get('/api/recipes/')
        types = {r['type_plat'] for r in response.data}
        self.assertIn(Recipe.TYPE_SALE, types)
        self.assertIn(Recipe.TYPE_SUCRE, types)
