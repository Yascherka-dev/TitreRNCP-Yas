from rest_framework.test import APITestCase
from rest_framework import status
from apps.users.models import User
from apps.ratings.models import Rating


class RatingTests(APITestCase):

    def setUp(self):
        self.user  = User.objects.create_user(email='rating@test.com', password='pass1234', nom='A', prenom='B')
        self.other = User.objects.create_user(email='other@test.com',  password='pass1234', nom='C', prenom='D')

    def test_list_ratings_is_public(self):
        response = self.client.get('/api/ratings/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_filter_ratings_by_reference(self):
        Rating.objects.create(user=self.user, type='recette', reference_id='10', valeur=4)
        Rating.objects.create(user=self.user, type='recette', reference_id='11', valeur=3)
        response = self.client.get('/api/ratings/?type=recette&reference_id=10')
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['valeur'], 4)

    def test_add_rating_requires_auth(self):
        response = self.client.post('/api/ratings/', {'type': 'recette', 'reference_id': '1', 'valeur': 4})
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_add_rating_authenticated(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.post('/api/ratings/', {'type': 'recette', 'reference_id': '1', 'valeur': 4})
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Rating.objects.filter(user=self.user, reference_id='1').count(), 1)

    def test_unique_rating_per_user_and_reference(self):
        self.client.force_authenticate(user=self.user)
        self.client.post('/api/ratings/', {'type': 'recette', 'reference_id': '5', 'valeur': 3})
        response = self.client.post('/api/ratings/', {'type': 'recette', 'reference_id': '5', 'valeur': 5})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_delete_own_rating(self):
        rating = Rating.objects.create(user=self.user, type='recette', reference_id='10', valeur=4)
        self.client.force_authenticate(user=self.user)
        response = self.client.delete(f'/api/ratings/{rating.id}/')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Rating.objects.filter(id=rating.id).exists())

    def test_cannot_delete_other_users_rating(self):
        rating = Rating.objects.create(user=self.other, type='recette', reference_id='20', valeur=5)
        self.client.force_authenticate(user=self.user)
        response = self.client.delete(f'/api/ratings/{rating.id}/')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
