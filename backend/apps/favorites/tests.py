from rest_framework.test import APITestCase
from rest_framework import status
from apps.users.models import User
from apps.favorites.models import Favorite


class FavoriteTests(APITestCase):

    def setUp(self):
        self.user  = User.objects.create_user(email='fav@test.com',   password='pass1234', nom='A', prenom='B')
        self.other = User.objects.create_user(email='other@test.com', password='pass1234', nom='C', prenom='D')

    def test_list_requires_authentication(self):
        response = self.client.get('/api/favorites/')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_list_returns_only_own_favorites(self):
        Favorite.objects.create(user=self.user,  type='recette', reference_id='1')
        Favorite.objects.create(user=self.other, type='recette', reference_id='2')
        self.client.force_authenticate(user=self.user)
        response = self.client.get('/api/favorites/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['reference_id'], '1')

    def test_add_favorite(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.post('/api/favorites/', {'type': 'recette', 'reference_id': '42'})
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(Favorite.objects.filter(user=self.user, reference_id='42').exists())

    def test_add_favorite_requires_auth(self):
        response = self.client.post('/api/favorites/', {'type': 'recette', 'reference_id': '1'})
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_duplicate_favorite_rejected(self):
        self.client.force_authenticate(user=self.user)
        self.client.post('/api/favorites/', {'type': 'recette', 'reference_id': '99'})
        response = self.client.post('/api/favorites/', {'type': 'recette', 'reference_id': '99'})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_delete_own_favorite(self):
        fav = Favorite.objects.create(user=self.user, type='recette', reference_id='77')
        self.client.force_authenticate(user=self.user)
        response = self.client.delete(f'/api/favorites/{fav.id}/')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Favorite.objects.filter(id=fav.id).exists())

    def test_cannot_delete_other_users_favorite(self):
        other_fav = Favorite.objects.create(user=self.other, type='recette', reference_id='55')
        self.client.force_authenticate(user=self.user)
        response = self.client.delete(f'/api/favorites/{other_fav.id}/')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertTrue(Favorite.objects.filter(id=other_fav.id).exists())
