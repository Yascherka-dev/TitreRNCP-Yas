from django.db import IntegrityError, transaction
from rest_framework import status
from rest_framework.test import APITestCase

from apps.comments.models import Comment
from apps.fabriques import creer_biere, creer_match, creer_recette, creer_utilisateur


class CommentTests(APITestCase):

    def setUp(self):
        self.user = creer_utilisateur('comment@test.com', nom='A', prenom='B')
        self.other = creer_utilisateur('other@test.com', nom='C', prenom='D')
        self.recette = creer_recette()
        self.autre_recette = creer_recette('Tajine')

    def test_list_comments_is_public(self):
        response = self.client.get('/api/comments/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_filter_comments_by_reference(self):
        Comment.objects.create(user=self.user, recette=self.recette, contenu='Super !')
        Comment.objects.create(user=self.user, recette=self.autre_recette, contenu='Bien !')
        response = self.client.get(
            f'/api/comments/?type=recette&reference_id={self.recette.pk}')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['reference_id'], str(self.recette.pk))

    def test_filter_sur_reference_inexistante_renvoie_une_liste_vide(self):
        Comment.objects.create(user=self.user, recette=self.recette, contenu='Super !')
        response = self.client.get('/api/comments/?type=recette&reference_id=999999')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 0)

    def test_add_comment_requires_auth(self):
        response = self.client.post('/api/comments/', {
            'type': 'recette', 'reference_id': str(self.recette.pk),
            'contenu': 'Super recette !'})
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_add_comment_authenticated(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.post('/api/comments/', {
            'type': 'recette', 'reference_id': str(self.recette.pk),
            'contenu': 'Très bonne recette !'})
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(
            Comment.objects.filter(user=self.user, recette=self.recette).exists())

    def test_plusieurs_commentaires_sur_la_meme_recette(self):
        # Contrairement aux favoris et aux notes, aucune contrainte d'unicité :
        # c'est pourquoi le MCD fait de COMMENTAIRE une entité, pas une
        # association. Voir docs/MERISE.md.
        self.client.force_authenticate(user=self.user)
        ref = str(self.recette.pk)
        premier = self.client.post('/api/comments/', {
            'type': 'recette', 'reference_id': ref, 'contenu': 'Première fois'})
        second = self.client.post('/api/comments/', {
            'type': 'recette', 'reference_id': ref, 'contenu': 'Refaite hier'})
        self.assertEqual(premier.status_code, status.HTTP_201_CREATED)
        self.assertEqual(second.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Comment.objects.filter(recette=self.recette).count(), 2)

    def test_delete_own_comment(self):
        comment = Comment.objects.create(
            user=self.user, recette=self.recette, contenu='Test')
        self.client.force_authenticate(user=self.user)
        response = self.client.delete(f'/api/comments/{comment.id}/')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Comment.objects.filter(id=comment.id).exists())

    def test_cannot_delete_other_users_comment(self):
        comment = Comment.objects.create(
            user=self.other, recette=self.autre_recette, contenu='Test')
        self.client.force_authenticate(user=self.user)
        response = self.client.delete(f'/api/comments/{comment.id}/')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertTrue(Comment.objects.filter(id=comment.id).exists())


class CommentIntegriteTests(APITestCase):

    def setUp(self):
        self.user = creer_utilisateur('ci@test.com', nom='A', prenom='B')
        self.match = creer_match('sdb_777')
        self.biere = creer_biere()

    def test_suppression_du_match_supprime_le_commentaire(self):
        commentaire = Comment.objects.create(
            user=self.user, match=self.match, contenu='Quel match')
        self.match.delete()
        self.assertFalse(Comment.objects.filter(pk=commentaire.pk).exists())

    def test_commentaire_sur_une_biere(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.post('/api/comments/', {
            'type': 'biere', 'reference_id': str(self.biere.pk),
            'contenu': 'Bien houblonnée'})
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['type'], 'biere')

    def test_aucune_cible_refusee(self):
        with self.assertRaises(IntegrityError):
            with transaction.atomic():
                Comment.objects.create(user=self.user, contenu='Sans cible')
