from django.db import IntegrityError, transaction
from rest_framework import status
from rest_framework.test import APITestCase

from apps.fabriques import creer_biere, creer_match, creer_recette, creer_utilisateur
from apps.ratings.models import Rating


class RatingTests(APITestCase):

    def setUp(self):
        self.user = creer_utilisateur('rating@test.com', nom='A', prenom='B')
        self.other = creer_utilisateur('other@test.com', nom='C', prenom='D')
        self.recette = creer_recette()
        self.autre_recette = creer_recette('Tajine')

    def test_list_ratings_is_public(self):
        response = self.client.get('/api/ratings/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_filter_ratings_by_reference(self):
        Rating.objects.create(user=self.user, recette=self.recette, valeur=4)
        Rating.objects.create(user=self.user, recette=self.autre_recette, valeur=3)
        response = self.client.get(
            f'/api/ratings/?type=recette&reference_id={self.recette.pk}')
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['valeur'], 4)

    def test_add_rating_requires_auth(self):
        response = self.client.post('/api/ratings/', {
            'type': 'recette', 'reference_id': str(self.recette.pk), 'valeur': 4})
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_add_rating_authenticated(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.post('/api/ratings/', {
            'type': 'recette', 'reference_id': str(self.recette.pk), 'valeur': 4})
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(
            Rating.objects.filter(user=self.user, recette=self.recette).count(), 1)

    def test_unique_rating_per_user_and_reference(self):
        self.client.force_authenticate(user=self.user)
        ref = str(self.recette.pk)
        self.client.post('/api/ratings/', {
            'type': 'recette', 'reference_id': ref, 'valeur': 3})
        response = self.client.post('/api/ratings/', {
            'type': 'recette', 'reference_id': ref, 'valeur': 5})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_valeur_hors_bornes_refusee(self):
        self.client.force_authenticate(user=self.user)
        for valeur in (0, 6):
            response = self.client.post('/api/ratings/', {
                'type': 'recette', 'reference_id': str(self.recette.pk),
                'valeur': valeur})
            self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_delete_own_rating(self):
        rating = Rating.objects.create(user=self.user, recette=self.recette, valeur=4)
        self.client.force_authenticate(user=self.user)
        response = self.client.delete(f'/api/ratings/{rating.id}/')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Rating.objects.filter(id=rating.id).exists())

    def test_cannot_delete_other_users_rating(self):
        rating = Rating.objects.create(
            user=self.other, recette=self.autre_recette, valeur=5)
        self.client.force_authenticate(user=self.user)
        response = self.client.delete(f'/api/ratings/{rating.id}/')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)


class RatingIntegriteTests(APITestCase):

    def setUp(self):
        self.user = creer_utilisateur('ri@test.com', nom='A', prenom='B')
        self.match = creer_match('sdb_555')
        self.biere = creer_biere()

    def test_suppression_du_match_supprime_la_note(self):
        note = Rating.objects.create(user=self.user, match=self.match, valeur=5)
        self.match.delete()
        self.assertFalse(Rating.objects.filter(pk=note.pk).exists())

    def test_valeur_hors_bornes_refusee_par_la_base(self):
        with self.assertRaises(IntegrityError):
            with transaction.atomic():
                Rating.objects.create(user=self.user, biere=self.biere, valeur=9)

    def test_relation_many_to_many_depuis_le_match(self):
        Rating.objects.create(user=self.user, match=self.match, valeur=4)
        self.assertIn(self.user, self.match.utilisateurs_notes.all())
        self.assertIn(self.match, self.user.matchs_notes.all())


class RatingAuteurTests(APITestCase):
    """
    Sans l'auteur dans la réponse, le front prenait la première note venue
    pour celle de l'utilisateur courant.
    """

    def setUp(self):
        self.user = creer_utilisateur('note@test.com', nom='Cherkaoui', prenom='Yasmina')
        self.autre = creer_utilisateur('autre@test.com', nom='Martin', prenom='Léa')
        self.recette = creer_recette()

    def test_la_reponse_expose_l_auteur_de_la_note(self):
        Rating.objects.create(user=self.autre, recette=self.recette, valeur=2)
        Rating.objects.create(user=self.user, recette=self.recette, valeur=5)
        response = self.client.get(
            f'/api/ratings/?type=recette&reference_id={self.recette.pk}')
        par_user = {r['user']: r['valeur'] for r in response.data}
        self.assertEqual(par_user[self.user.pk], 5)
        self.assertEqual(par_user[self.autre.pk], 2)

    def test_l_auteur_n_est_pas_modifiable_par_le_client(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.post('/api/ratings/', {
            'type': 'recette', 'reference_id': str(self.recette.pk),
            'valeur': 4, 'user': self.autre.pk})
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['user'], self.user.pk)
