from django.db import IntegrityError, transaction
from rest_framework import status
from rest_framework.test import APITestCase

from apps.fabriques import creer_biere, creer_match, creer_recette, creer_utilisateur
from apps.favorites.models import Favorite


class FavoriteTests(APITestCase):

    def setUp(self):
        self.user = creer_utilisateur('fav@test.com', nom='A', prenom='B')
        self.other = creer_utilisateur('other@test.com', nom='C', prenom='D')
        self.recette = creer_recette()
        self.autre_recette = creer_recette('Tajine')

    def test_list_requires_authentication(self):
        response = self.client.get('/api/favorites/')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_list_returns_only_own_favorites(self):
        Favorite.objects.create(user=self.user, recette=self.recette)
        Favorite.objects.create(user=self.other, recette=self.autre_recette)
        self.client.force_authenticate(user=self.user)
        response = self.client.get('/api/favorites/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['reference_id'], str(self.recette.pk))

    def test_add_favorite(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.post('/api/favorites/', {
            'type': 'recette', 'reference_id': str(self.recette.pk)})
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(
            Favorite.objects.filter(user=self.user, recette=self.recette).exists())

    def test_add_favorite_requires_auth(self):
        response = self.client.post('/api/favorites/', {
            'type': 'recette', 'reference_id': str(self.recette.pk)})
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_duplicate_favorite_rejected(self):
        self.client.force_authenticate(user=self.user)
        ref = str(self.recette.pk)
        self.client.post('/api/favorites/', {'type': 'recette', 'reference_id': ref})
        response = self.client.post('/api/favorites/', {'type': 'recette', 'reference_id': ref})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_delete_own_favorite(self):
        fav = Favorite.objects.create(user=self.user, recette=self.recette)
        self.client.force_authenticate(user=self.user)
        response = self.client.delete(f'/api/favorites/{fav.id}/')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Favorite.objects.filter(id=fav.id).exists())

    def test_cannot_delete_other_users_favorite(self):
        other_fav = Favorite.objects.create(user=self.other, recette=self.recette)
        self.client.force_authenticate(user=self.user)
        response = self.client.delete(f'/api/favorites/{other_fav.id}/')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertTrue(Favorite.objects.filter(id=other_fav.id).exists())


class ReferenceApiTests(APITestCase):
    """
    L'API expose toujours un couple (type, reference_id) : la bascule vers de
    vraies clés étrangères ne devait rien changer pour le front.
    """

    def setUp(self):
        self.user = creer_utilisateur('ref@test.com', nom='A', prenom='B')
        self.recipe = creer_recette()
        self.match = creer_match()
        self.biere = creer_biere()
        self.client.force_authenticate(user=self.user)

    def test_reference_existante_acceptee(self):
        r = self.client.post('/api/favorites/', {
            'type': 'recette', 'reference_id': str(self.recipe.id)})
        self.assertEqual(r.status_code, status.HTTP_201_CREATED)
        self.assertEqual(r.data['type'], 'recette')
        self.assertEqual(r.data['reference_id'], str(self.recipe.id))

    def test_reference_inexistante_refusee(self):
        r = self.client.post('/api/favorites/', {
            'type': 'recette', 'reference_id': '999999'})
        self.assertEqual(r.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('reference_id', r.data)

    def test_match_designe_par_son_external_id(self):
        # L'API expose Match.id = external_id : c'est lui que le front renvoie.
        ok = self.client.post('/api/favorites/', {
            'type': 'match', 'reference_id': 'sdb_123'})
        self.assertEqual(ok.status_code, status.HTTP_201_CREATED)
        self.assertEqual(ok.data['reference_id'], 'sdb_123')

        ko = self.client.post('/api/favorites/', {
            'type': 'match', 'reference_id': str(self.match.pk)})
        self.assertEqual(ko.status_code, status.HTTP_400_BAD_REQUEST)

    def test_biere_acceptee(self):
        r = self.client.post('/api/favorites/', {
            'type': 'biere', 'reference_id': str(self.biere.pk)})
        self.assertEqual(r.status_code, status.HTTP_201_CREATED)
        self.assertEqual(r.data['type'], 'biere')

    def test_type_inconnu_refuse(self):
        r = self.client.post('/api/favorites/', {
            'type': 'recete', 'reference_id': '1'})
        self.assertEqual(r.status_code, status.HTTP_400_BAD_REQUEST)

    def test_type_equipe_refuse(self):
        # 'equipe' figurait dans les choix du modèle sans qu'aucune entité
        # Équipe n'existe en base : la fonctionnalité ne pouvait pas marcher.
        r = self.client.post('/api/favorites/', {
            'type': 'equipe', 'reference_id': 'PSG'})
        self.assertEqual(r.status_code, status.HTTP_400_BAD_REQUEST)

    def test_reference_non_numerique_refusee_pour_une_recette(self):
        r = self.client.post('/api/favorites/', {
            'type': 'recette', 'reference_id': 'football_542667'})
        self.assertEqual(r.status_code, status.HTTP_400_BAD_REQUEST)


class IntegriteEnBaseTests(APITestCase):
    """
    Ce que les clés étrangères garantissent, et que le couple (type,
    reference_id) laissait passer : plus d'orphelins, plus de cible absente.
    """

    def setUp(self):
        self.user = creer_utilisateur('integrite@test.com', nom='A', prenom='B')
        self.recette = creer_recette()
        self.match = creer_match('sdb_999')

    def test_suppression_du_match_supprime_le_favori_en_cascade(self):
        favori = Favorite.objects.create(user=self.user, match=self.match)
        survivant = Favorite.objects.create(user=self.user, recette=self.recette)

        # Le match sort de la fenêtre : sync_matches le supprime.
        self.match.delete()

        self.assertFalse(Favorite.objects.filter(pk=favori.pk).exists())
        self.assertTrue(Favorite.objects.filter(pk=survivant.pk).exists())

    def test_suppression_de_l_utilisateur_supprime_ses_favoris(self):
        favori = Favorite.objects.create(user=self.user, recette=self.recette)
        self.user.delete()
        self.assertFalse(Favorite.objects.filter(pk=favori.pk).exists())

    def test_deux_cibles_a_la_fois_refusees(self):
        with self.assertRaises(IntegrityError):
            with transaction.atomic():
                Favorite.objects.create(
                    user=self.user, recette=self.recette, match=self.match)

    def test_aucune_cible_refusee(self):
        with self.assertRaises(IntegrityError):
            with transaction.atomic():
                Favorite.objects.create(user=self.user)

    def test_relation_many_to_many_depuis_la_recette(self):
        Favorite.objects.create(user=self.user, recette=self.recette)
        self.assertIn(self.user, self.recette.utilisateurs_favoris.all())
        self.assertIn(self.recette, self.user.recettes_favorites.all())
