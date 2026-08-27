"""
Fabriques d'objets pour les tests.

Regroupées ici plutôt que dupliquées dans chaque `tests.py` — ou pire, importées
d'une application à l'autre. Le nom du module ne commence pas par `test` : le
lanceur de tests Django ne le collecte pas.
"""

from django.utils import timezone

from apps.beers.models import Beer
from apps.matches.models import Match
from apps.recipes.models import Recipe
from apps.users.models import User


def creer_utilisateur(email='test@test.com', **extra) -> User:
    return User.objects.create_user(
        email=email, password='pass1234',
        nom=extra.pop('nom', 'Nom'), prenom=extra.pop('prenom', 'Prenom'), **extra)


def creer_recette(titre='Cassoulet', **extra) -> Recipe:
    return Recipe.objects.create(
        titre=titre,
        pays=extra.pop('pays', 'france'),
        description=extra.pop('description', 'x'),
        temps_preparation=extra.pop('temps_preparation', 10),
        **extra)


def creer_match(external_id='sdb_123', **extra) -> Match:
    return Match.objects.create(
        external_id=external_id,
        sport=extra.pop('sport', 'football'),
        competition=extra.pop('competition', 'Ligue 1'),
        equipe_a=extra.pop('equipe_a', 'A'),
        equipe_b=extra.pop('equipe_b', 'B'),
        pays_a=extra.pop('pays_a', 'france'),
        pays_b=extra.pop('pays_b', 'france'),
        date_heure=extra.pop('date_heure', None) or timezone.now(),
        statut=extra.pop('statut', 'NS'),
        **extra)


def creer_biere(nom='Triple', **extra) -> Beer:
    return Beer.objects.create(
        nom=nom,
        brasserie=extra.pop('brasserie', 'X'),
        pays=extra.pop('pays', 'belgium'),
        style=extra.pop('style', 'Triple'),
        description=extra.pop('description', 'x'),
        **extra)
