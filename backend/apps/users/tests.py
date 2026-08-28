from rest_framework.test import APITestCase
from rest_framework import status
from apps.users.models import User


class AuthTests(APITestCase):

    def test_register_creates_user_and_returns_tokens(self):
        data = {'email': 'new@test.com', 'password': 'MarcoCuisine2026', 'nom': 'Dupont', 'prenom': 'Jean'}
        response = self.client.post('/api/auth/register/', data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIn('access', response.data)
        self.assertIn('refresh', response.data)
        self.assertTrue(User.objects.filter(email='new@test.com').exists())

    def test_register_fails_with_duplicate_email(self):
        User.objects.create_user(email='dup@test.com', password='pass1234', nom='A', prenom='B')
        data = {'email': 'dup@test.com', 'password': 'other123', 'nom': 'C', 'prenom': 'D'}
        response = self.client.post('/api/auth/register/', data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_register_requires_all_fields(self):
        response = self.client.post('/api/auth/register/', {'email': 'x@test.com'})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_login_returns_tokens(self):
        User.objects.create_user(email='login@test.com', password='secret123', nom='A', prenom='B')
        response = self.client.post('/api/auth/login/', {'email': 'login@test.com', 'password': 'secret123'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('access', response.data)
        self.assertIn('refresh', response.data)

    def test_login_fails_with_wrong_password(self):
        User.objects.create_user(email='user@test.com', password='correct', nom='A', prenom='B')
        response = self.client.post('/api/auth/login/', {'email': 'user@test.com', 'password': 'wrong'})
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_login_fails_with_unknown_email(self):
        response = self.client.post('/api/auth/login/', {'email': 'ghost@test.com', 'password': 'any'})
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_me_returns_profile_when_authenticated(self):
        user = User.objects.create_user(email='me@test.com', password='pass1234', nom='Curie', prenom='Marie')
        self.client.force_authenticate(user=user)
        response = self.client.get('/api/auth/me/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['email'], 'me@test.com')
        self.assertEqual(response.data['prenom'], 'Marie')

    def test_me_requires_authentication(self):
        response = self.client.get('/api/auth/me/')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


class InscriptionSecuriteTests(APITestCase):
    """
    AUTH_PASSWORD_VALIDATORS est configuré dans settings.py mais le serializer
    ne l'appelait jamais : « password » et « 12345678 » passaient.
    """

    BASE = {'email': 'nouveau@test.com', 'nom': 'Dupont', 'prenom': 'Thomas'}

    def _inscrire(self, password, **extra):
        return self.client.post('/api/auth/register/',
                                {**self.BASE, **extra, 'password': password}, format='json')

    def test_mot_de_passe_courant_refuse(self):
        r = self._inscrire('password')
        self.assertEqual(r.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('password', r.data)

    def test_mot_de_passe_tout_en_chiffres_refuse(self):
        r = self._inscrire('12345678')
        self.assertEqual(r.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('password', r.data)

    def test_mot_de_passe_trop_proche_de_l_email_refuse(self):
        r = self._inscrire('nouveau@test.com')
        self.assertEqual(r.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('password', r.data)

    def test_mot_de_passe_solide_accepte(self):
        r = self._inscrire('MarcoCuisine2026')
        self.assertEqual(r.status_code, status.HTTP_201_CREATED)

    def test_message_lisible_quand_l_email_est_deja_pris(self):
        self._inscrire('MarcoCuisine2026')
        r = self._inscrire('AutreMotDePasse99')
        self.assertEqual(r.status_code, status.HTTP_400_BAD_REQUEST)
        message = r.data['email'][0]
        self.assertIn('compte', message.lower())
        self.assertNotIn('objet user', message.lower())


class SuppressionDuCompteTests(APITestCase):
    """
    Les mentions légales annoncent que les données sont « supprimées avec le
    compte ». Le droit à l'effacement s'exerce donc depuis l'application.

    Le mot de passe est redemandé : une session laissée ouverte ne doit pas
    suffire à effacer un compte.
    """

    def setUp(self):
        self.user = User.objects.create_user(
            email='asupprimer@test.com', password='MarcoCuisine2026',
            nom='Cherkaoui', prenom='Yasmina')
        self.client.force_authenticate(user=self.user)

    def test_suppression_avec_le_bon_mot_de_passe(self):
        r = self.client.delete('/api/auth/me/', {'password': 'MarcoCuisine2026'}, format='json')
        self.assertEqual(r.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(User.objects.filter(pk=self.user.pk).exists())

    def test_mot_de_passe_incorrect_refuse(self):
        r = self.client.delete('/api/auth/me/', {'password': 'PasLeBon2026'}, format='json')
        self.assertEqual(r.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertTrue(User.objects.filter(pk=self.user.pk).exists())

    def test_mot_de_passe_manquant_refuse(self):
        r = self.client.delete('/api/auth/me/', {}, format='json')
        self.assertEqual(r.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertTrue(User.objects.filter(pk=self.user.pk).exists())

    def test_suppression_refusee_sans_authentification(self):
        self.client.force_authenticate(user=None)
        r = self.client.delete('/api/auth/me/', {'password': 'MarcoCuisine2026'}, format='json')
        self.assertEqual(r.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertTrue(User.objects.filter(pk=self.user.pk).exists())

    def test_les_contributions_partent_avec_le_compte(self):
        from apps.comments.models import Comment
        from apps.fabriques import creer_recette
        from apps.favorites.models import Favorite
        from apps.ratings.models import Rating

        recette = creer_recette()
        Favorite.objects.create(user=self.user, recette=recette)
        Comment.objects.create(user=self.user, recette=recette, contenu='Excellent')
        Rating.objects.create(user=self.user, recette=recette, valeur=5)

        r = self.client.delete('/api/auth/me/', {'password': 'MarcoCuisine2026'}, format='json')

        self.assertEqual(r.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Favorite.objects.count(), 0)
        self.assertEqual(Comment.objects.count(), 0)
        self.assertEqual(Rating.objects.count(), 0)
        # La recette, elle, ne appartient à personne : elle reste.
        self.assertTrue(recette.__class__.objects.filter(pk=recette.pk).exists())
