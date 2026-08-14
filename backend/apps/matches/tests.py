from datetime import date

from django.test import SimpleTestCase
from rest_framework.test import APITestCase
from rest_framework import status
from django.utils import timezone
from apps.matches.models import Match
from apps.matches.sports_api import LEAGUES, current_season, normalise_country


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


class SeasonResolutionTests(SimpleTestCase):
    """
    Les saisons ne doivent pas être codées en dur : elles se périmaient
    silencieusement chaque année et la synchro ne ramenait plus rien.
    """

    def test_saison_a_cheval_bascule_le_1er_juillet(self):
        # Ligue 1, Top 14, NHL, NBA, CL : saison 2026-2027 à partir de juillet 2026
        self.assertEqual(current_season({'season_style': 'split'}, date(2026, 8, 14)), '2026-2027')
        self.assertEqual(current_season({'season_style': 'split'}, date(2026, 7, 1)), '2026-2027')
        # Fin juin 2026 : on est encore sur 2025-2026
        self.assertEqual(current_season({'season_style': 'split'}, date(2026, 6, 30)), '2025-2026')

    def test_saison_calendaire_nfl_bascule_en_mars(self):
        self.assertEqual(current_season({'season_style': 'calendar'}, date(2026, 8, 14)), '2026')
        self.assertEqual(current_season({'season_style': 'calendar'}, date(2027, 1, 10)), '2026')
        self.assertEqual(current_season({'season_style': 'calendar'}, date(2027, 3, 1)), '2027')

    def test_edition_a_venir_six_nations(self):
        # En août 2026, la prochaine édition est celle de février 2027
        self.assertEqual(current_season({'season_style': 'next_year'}, date(2026, 8, 14)), '2027')
        # En mars 2027, on est sur l'édition en cours
        self.assertEqual(current_season({'season_style': 'next_year'}, date(2027, 3, 1)), '2027')

    def test_saison_figee_conserve_sa_valeur(self):
        # Coupe du Monde : événement daté, il ne se rejoue pas chaque année
        cfg = {'season_style': 'fixed', 'season': '2026'}
        self.assertEqual(current_season(cfg, date(2030, 1, 1)), '2026')

    def test_toutes_les_ligues_configurees_resolvent_une_saison(self):
        for cfg in LEAGUES:
            with self.subTest(league=cfg['id']):
                saison = current_season(cfg, date(2026, 9, 15))
                self.assertTrue(saison, f"ligue {cfg['id']} ne résout aucune saison")


class CountryNormalisationTests(SimpleTestCase):
    """
    TheSportsDB et le catalogue de recettes n'orthographient pas les pays
    pareil. Sans alias, les matchs concernés sortaient sans recette, en
    silence : aucune erreur, juste une suggestion vide.
    """

    def test_alias_vers_le_nom_du_catalogue(self):
        self.assertEqual(normalise_country('The Netherlands'), 'netherlands')
        self.assertEqual(normalise_country('Czechia'), 'czech republic')

    def test_insensible_a_la_casse_et_aux_espaces(self):
        self.assertEqual(normalise_country('  THE NETHERLANDS  '), 'netherlands')

    def test_pays_sans_alias_inchange(self):
        self.assertEqual(normalise_country('France'), 'france')
        self.assertEqual(normalise_country('Bulgaria'), 'bulgaria')

    def test_valeur_vide(self):
        self.assertEqual(normalise_country(''), '')
        self.assertEqual(normalise_country(None), '')

    def test_irlande_du_nord_reste_distincte(self):
        # L'Ulster a sa propre cuisine : l'aliaser vers 'ireland' serait faux.
        self.assertEqual(normalise_country('Northern Ireland'), 'northern ireland')
