from datetime import date, timedelta
from io import StringIO

import requests

from django.core.management import call_command
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


class EchecReseauTests(SimpleTestCase):
    """
    TheSportsDB peut tomber, changer de format ou expirer. La synchronisation
    doit alors continuer sur les autres ligues — mais l'échec doit laisser une
    trace : sans elle, une synchronisation vide passe pour une absence de
    matchs, et personne ne cherche la panne.
    """

    def test_une_ligue_en_echec_n_emporte_pas_les_autres(self):
        from unittest.mock import patch
        from apps.matches import sports_api

        appels = {'n': 0}

        def _v2_capricieux(chemin):
            appels['n'] += 1
            if appels['n'] == 1:
                raise requests.RequestException('502 Bad Gateway')
            return {'schedule': []}

        with patch.object(sports_api, '_v2', side_effect=_v2_capricieux):
            with self.assertLogs('apps.matches.sports_api', level='WARNING') as journal:
                resultats = sports_api.fetch_fixtures()

        # Toutes les ligues ont été tentées malgré le premier échec.
        self.assertEqual(appels['n'], len(sports_api.LEAGUES))
        self.assertEqual(resultats, [])
        # Et l'échec est nommé, avec la ligue concernée.
        self.assertTrue(any('Calendrier indisponible' in m for m in journal.output))

    def test_l_echec_des_scores_en_direct_est_journalise(self):
        from unittest.mock import patch
        from apps.matches import sports_api

        with patch.object(sports_api, '_v2', side_effect=requests.RequestException('timeout')), \
             patch.object(sports_api, '_v1', return_value={'events': []}):
            with self.assertLogs('apps.matches.sports_api', level='WARNING') as journal:
                resultats = sports_api.fetch_livescores()

        self.assertEqual(resultats, [])
        self.assertTrue(any('Scores en direct indisponibles' in m for m in journal.output))

    def test_l_echec_d_une_journee_est_journalise(self):
        from unittest.mock import patch
        from apps.matches import sports_api

        with patch.object(sports_api, '_v1', side_effect=requests.RequestException('404')):
            with self.assertLogs('apps.matches.sports_api', level='WARNING') as journal:
                resultats = sports_api.fetch_fixtures(date='2026-08-28')

        self.assertEqual(resultats, [])
        self.assertTrue(any('Récupération des matchs' in m for m in journal.output))

    def test_un_score_illisible_ne_fait_pas_tomber_la_synchro(self):
        from apps.matches.sports_api import _parse_score

        self.assertEqual(_parse_score('3'), 3)
        self.assertIsNone(_parse_score(None))
        self.assertIsNone(_parse_score('—'))


class SynchronisationTests(APITestCase):
    """
    La commande sync_matches n'écrit que les matchs de la fenêtre affichée
    (J-30 / J+60) et purge le reste. Depuis le passage aux clés étrangères,
    les favoris, notes et commentaires des matchs purgés partent en cascade.
    """

    def _fixture(self, external_id, jours):
        """Un match brut tel que sports_api le renvoie, décalé de N jours."""
        return {
            'external_id': external_id,
            'sport': 'football',
            'competition': 'French Ligue 1',
            'equipe_a': 'Lille',
            'equipe_b': 'Paris Saint-Germain',
            'pays_a': 'france',
            'pays_b': 'france',
            'date_heure': timezone.now() + timedelta(days=jours),
            'statut': 'NS',
        }

    def test_seuls_les_matchs_de_la_fenetre_sont_enregistres(self):
        from unittest.mock import patch

        fixtures = [
            self._fixture('sdb_dans', 5),      # dans la fenêtre
            self._fixture('sdb_trop_loin', 200),  # au-delà de J+60
            self._fixture('sdb_trop_vieux', -200),  # avant J-30
        ]
        with patch('apps.matches.management.commands.sync_matches.fetch_fixtures',
                   return_value=fixtures):
            call_command('sync_matches', '--no-purge', stdout=StringIO())

        enregistres = set(Match.objects.values_list('external_id', flat=True))
        self.assertEqual(enregistres, {'sdb_dans'})

    def test_la_purge_emporte_les_favoris_du_match_supprime(self):
        from unittest.mock import patch
        from apps.fabriques import creer_utilisateur
        from apps.favorites.models import Favorite

        hors_fenetre = Match.objects.create(
            external_id='sdb_perime', sport='football', competition='Ligue 1',
            equipe_a='A', equipe_b='B', pays_a='france', pays_b='france',
            date_heure=timezone.now() - timedelta(days=300), statut='FT')
        favori = Favorite.objects.create(
            user=creer_utilisateur('purge@test.com'), match=hors_fenetre)

        with patch('apps.matches.management.commands.sync_matches.fetch_fixtures',
                   return_value=[]):
            call_command('sync_matches', stdout=StringIO())

        self.assertFalse(Match.objects.filter(pk=hors_fenetre.pk).exists())
        # Plus besoin de nettoyage manuel : la clé étrangère l'a emporté.
        self.assertFalse(Favorite.objects.filter(pk=favori.pk).exists())

    def test_une_date_ciblee_desactive_la_purge(self):
        from unittest.mock import patch

        garde = Match.objects.create(
            external_id='sdb_ancien', sport='football', competition='Ligue 1',
            equipe_a='A', equipe_b='B', pays_a='france', pays_b='france',
            date_heure=timezone.now() - timedelta(days=300), statut='FT')

        with patch('apps.matches.management.commands.sync_matches.fetch_fixtures',
                   return_value=[]):
            call_command('sync_matches', '--date', '2026-08-28', stdout=StringIO())

        self.assertTrue(Match.objects.filter(pk=garde.pk).exists())
