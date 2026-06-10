from rest_framework.test import APITestCase
from rest_framework import status
from django.utils import timezone
from apps.matches.models import Match


class MatchTests(APITestCase):

    def setUp(self):
        Match.objects.create(
            external_id='test-001',
            sport='football',
            competition='Ligue 1',
            league_id=4334,
            equipe_a='PSG',
            equipe_b='Marseille',
            pays_a='france',
            pays_b='france',
            date_heure=timezone.now(),
            statut='NS',
        )
        Match.objects.create(
            external_id='test-002',
            sport='basketball',
            competition='NBA',
            league_id=4387,
            equipe_a='Lakers',
            equipe_b='Bulls',
            pays_a='usa',
            pays_b='usa',
            date_heure=timezone.now(),
            statut='FT',
            score_a=108,
            score_b=95,
        )

    def test_list_matches_is_public(self):
        response = self.client.get('/api/matches/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIsInstance(response.data, list)

    def test_list_matches_returns_correct_fields(self):
        response = self.client.get('/api/matches/')
        self.assertGreaterEqual(len(response.data), 1)
        match = response.data[0]
        for field in ['id', 'equipe_a', 'equipe_b', 'statut', 'date_heure']:
            self.assertIn(field, match)

    def test_filter_by_sport(self):
        response = self.client.get('/api/matches/?sport=basketball')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        for match in response.data:
            self.assertEqual(match['sport'], 'basketball')
