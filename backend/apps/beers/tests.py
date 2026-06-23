from rest_framework.test import APITestCase
from rest_framework import status
from apps.beers.models import Beer


class BeerTests(APITestCase):

    def setUp(self):
        Beer.objects.create(
            nom='Kronenbourg 1664', brasserie='Brasserie Kronenbourg',
            pays='france', region='Alsace', equipe='',
            style='Lager', description='La bière française emblématique.',
            degre_alcool='5.0', image_url='',
        )
        Beer.objects.create(
            nom='Paulaner Weissbier', brasserie='Paulaner Brauerei',
            pays='germany', region='Bavière', equipe='',
            style='Hefeweizen', description='Grande bière de blé bavaroise.',
            degre_alcool='5.5', image_url='',
        )
        Beer.objects.create(
            nom='FC Beer', brasserie='Club Brasserie',
            pays='france', region='Paris', equipe='paris saint-germain',
            style='Lager', description='Bière officielle du club.',
            degre_alcool='4.5', image_url='',
        )

    def test_beers_accessible_without_auth(self):
        response = self.client.get('/api/beers/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_beers_returns_list(self):
        response = self.client.get('/api/beers/')
        self.assertIsInstance(response.data, list)
        self.assertEqual(len(response.data), 3)

    def test_beer_fields_present(self):
        response = self.client.get('/api/beers/')
        beer = response.data[0]
        for field in ['nom', 'brasserie', 'pays', 'style', 'description', 'degre_alcool']:
            self.assertIn(field, beer)

    def test_filter_by_pays(self):
        response = self.client.get('/api/beers/?pays=france')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        for beer in response.data:
            self.assertEqual(beer['pays'], 'france')
