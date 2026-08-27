from rest_framework.test import APITestCase
from rest_framework import status
from apps.users.models import User
from apps.favorites.models import Favorite


class FavoriteTests(APITestCase):

    def setUp(self):
        self.user  = User.objects.create_user(email='fav@test.com',   password='pass1234', nom='A', prenom='B')
        self.other = User.objects.create_user(email='other@test.com', password='pass1234', nom='C', prenom='D')

        # Les références polymorphes sont désormais validées à l'écriture
        # (apps/references.py) : les recettes visées par ces tests doivent
        # exister. 999999 reste volontairement absent, il sert aux cas d'échec.
        from apps.recipes.models import Recipe
        for pk in [1, 2, 42, 55, 77, 99]:
            Recipe.objects.create(pk=pk, titre=f'Recette {pk}', pays='france',
                                  description='x', temps_preparation=10)

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


class ReferenceIntegrityTests(APITestCase):
    """
    Favorite, Comment et Rating désignent leur cible par un couple
    (type, reference_id) plutôt que par une clé étrangère. La base ne peut donc
    pas garantir que la cible existe : 12 références sur 18 pointaient vers le
    vide après un changement d'API sportive et un rechargement des recettes.

    L'intégrité est assurée ici, à l'écriture.
    """

    def setUp(self):
        from apps.recipes.models import Recipe
        from apps.matches.models import Match
        from django.utils import timezone

        self.user = User.objects.create_user(
            email='ref@test.com', password='pass1234', nom='A', prenom='B')
        self.recipe = Recipe.objects.create(
            titre='Cassoulet', pays='france', description='x', temps_preparation=10)
        self.match = Match.objects.create(
            external_id='sdb_123', sport='football', competition='Ligue 1',
            equipe_a='A', equipe_b='B', pays_a='france', pays_b='france',
            date_heure=timezone.now(), statut='NS')
        self.client.force_authenticate(user=self.user)

    def test_reference_existante_acceptee(self):
        r = self.client.post('/api/favorites/', {
            'type': 'recette', 'reference_id': str(self.recipe.id)})
        self.assertEqual(r.status_code, status.HTTP_201_CREATED)

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

        ko = self.client.post('/api/favorites/', {
            'type': 'match', 'reference_id': str(self.match.pk)})
        self.assertEqual(ko.status_code, status.HTTP_400_BAD_REQUEST)

    def test_type_inconnu_refuse(self):
        r = self.client.post('/api/favorites/', {
            'type': 'recete', 'reference_id': '1'})
        self.assertEqual(r.status_code, status.HTTP_400_BAD_REQUEST)

    def test_reference_non_numerique_refusee_pour_une_recette(self):
        r = self.client.post('/api/favorites/', {
            'type': 'recette', 'reference_id': 'football_542667'})
        self.assertEqual(r.status_code, status.HTTP_400_BAD_REQUEST)


class PurgeDeadReferencesTests(APITestCase):
    """
    La validation à l'écriture ne protège que du présent : un favori valide au
    moment du clic devient orphelin quand sync_matches purge le match sorti de
    la fenêtre J-30/J+60. Le nettoyage doit donc suivre la purge.
    """

    def setUp(self):
        from apps.matches.models import Match
        from apps.recipes.models import Recipe
        from django.utils import timezone

        self.user = User.objects.create_user(
            email='purge@test.com', password='pass1234', nom='A', prenom='B')
        self.recipe = Recipe.objects.create(
            titre='Cassoulet', pays='france', description='x', temps_preparation=10)
        self.match = Match.objects.create(
            external_id='sdb_999', sport='football', competition='Ligue 1',
            equipe_a='A', equipe_b='B', pays_a='france', pays_b='france',
            date_heure=timezone.now(), statut='NS')

    def test_supprime_les_orphelins_et_epargne_les_valides(self):
        from apps.references import purge_dead_references

        vivant = Favorite.objects.create(
            user=self.user, type='recette', reference_id=str(self.recipe.id))
        sur_match = Favorite.objects.create(
            user=self.user, type='match', reference_id='sdb_999')

        # Le match sort de la fenêtre : sync_matches le supprime.
        self.match.delete()

        supprimes = purge_dead_references()

        self.assertEqual(supprimes['favoris'], 1)
        self.assertTrue(Favorite.objects.filter(pk=vivant.pk).exists())
        self.assertFalse(Favorite.objects.filter(pk=sur_match.pk).exists())

    def test_ne_supprime_rien_quand_tout_est_valide(self):
        from apps.references import purge_dead_references

        Favorite.objects.create(
            user=self.user, type='recette', reference_id=str(self.recipe.id))
        self.assertEqual(sum(purge_dead_references().values()), 0)

    def test_mode_simulation_ne_supprime_pas(self):
        from apps.references import purge_dead_references

        orphelin = Favorite.objects.create(
            user=self.user, type='match', reference_id='sdb_inexistant')

        supprimes = purge_dead_references(dry_run=True)

        self.assertEqual(supprimes['favoris'], 1)
        self.assertTrue(Favorite.objects.filter(pk=orphelin.pk).exists())
