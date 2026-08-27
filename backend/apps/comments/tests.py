from rest_framework.test import APITestCase
from rest_framework import status
from apps.users.models import User
from apps.comments.models import Comment


class CommentTests(APITestCase):

    def setUp(self):
        self.user  = User.objects.create_user(email='comment@test.com', password='pass1234', nom='A', prenom='B')
        self.other = User.objects.create_user(email='other@test.com',   password='pass1234', nom='C', prenom='D')

        # Les références polymorphes sont désormais validées à l'écriture
        # (apps/references.py) : les recettes visées par ces tests doivent
        # exister. 999999 reste volontairement absent, il sert aux cas d'échec.
        from apps.recipes.models import Recipe
        for pk in [1, 2, 5, 6]:
            Recipe.objects.create(pk=pk, titre=f'Recette {pk}', pays='france',
                                  description='x', temps_preparation=10)

    def test_list_comments_is_public(self):
        response = self.client.get('/api/comments/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_filter_comments_by_reference(self):
        Comment.objects.create(user=self.user, type='recette', reference_id='5', contenu='Super !')
        Comment.objects.create(user=self.user, type='recette', reference_id='6', contenu='Bien !')
        response = self.client.get('/api/comments/?type=recette&reference_id=5')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['reference_id'], '5')

    def test_add_comment_requires_auth(self):
        response = self.client.post('/api/comments/', {'type': 'recette', 'reference_id': '1', 'contenu': 'Super recette !'})
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_add_comment_authenticated(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.post('/api/comments/', {
            'type': 'recette', 'reference_id': '1', 'contenu': 'Très bonne recette !'
        })
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(Comment.objects.filter(user=self.user, reference_id='1').exists())

    def test_delete_own_comment(self):
        comment = Comment.objects.create(user=self.user, type='recette', reference_id='1', contenu='Test')
        self.client.force_authenticate(user=self.user)
        response = self.client.delete(f'/api/comments/{comment.id}/')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Comment.objects.filter(id=comment.id).exists())

    def test_cannot_delete_other_users_comment(self):
        comment = Comment.objects.create(user=self.other, type='recette', reference_id='2', contenu='Test')
        self.client.force_authenticate(user=self.user)
        response = self.client.delete(f'/api/comments/{comment.id}/')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertTrue(Comment.objects.filter(id=comment.id).exists())
