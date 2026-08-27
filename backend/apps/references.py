"""
Résolution des cibles de Favorite, Comment et Rating.

Ces trois tables désignent une cible parmi trois : un match, une recette ou une
bière. Le choix historique était un couple (type, reference_id) — deux colonnes
de texte, sans clé étrangère. Il évitait de multiplier les tables, mais privait
la base de toute garantie : PostgreSQL ne savait pas que `reference_id`
désignait quelque chose, donc rien n'empêchait d'enregistrer une référence vers
un objet inexistant, ni de laisser des orphelins quand la cible disparaissait.

Depuis, chaque cible possède sa propre clé étrangère, nullable, et une
contrainte garantit qu'exactement une est renseignée. L'intégrité est redevenue
l'affaire de la base : références invalides refusées, suppressions en cascade.

Ce module ne garde que la traduction entre les deux langages :

    API   ──  type='match', reference_id='sdb_2528727'
    base  ──  match=<Match: …>

L'API publique n'a pas changé — le front continue d'envoyer et de lire un
couple (type, reference_id).

Attention aux identifiants : l'API expose `Match.id` comme étant `external_id`
(« sdb_2528727 »), alors que recettes et bières sont désignées par leur clé
primaire numérique. Le front renvoie ce qu'il a reçu.
"""

from django.db import models

#: Types acceptés dans le champ `type`, et nom du champ de liaison associé.
CHAMP_PAR_TYPE: dict[str, str] = {
    'match':   'match',
    'recette': 'recette',
    'biere':   'biere',
}

#: Types acceptés dans le champ `type` de l'API.
REFERENCE_TYPES = tuple(CHAMP_PAR_TYPE)


def champ_de(type_: str) -> str | None:
    """Nom du champ de liaison correspondant à un type de l'API."""
    return CHAMP_PAR_TYPE.get(type_)


def resolve_reference(type_: str, reference_id: str) -> models.Model | None:
    """
    L'objet désigné par (type, reference_id), ou None s'il n'existe pas.

    Import local des modèles : ce module est importé par les modèles eux-mêmes,
    qui le sont au chargement des applications.
    """
    from apps.beers.models import Beer
    from apps.matches.models import Match
    from apps.recipes.models import Recipe

    ref = (reference_id or '').strip()
    if not ref:
        return None

    if type_ == 'match':
        # Désigné par external_id, pas par la clé primaire.
        return Match.objects.filter(external_id=ref).first()

    model = {'recette': Recipe, 'biere': Beer}.get(type_)
    if model is None:
        return None

    # Clé primaire numérique : une référence non numérique ne peut pas exister.
    if not ref.isdigit():
        return None

    return model.objects.filter(pk=int(ref)).first()


def reference_exists(type_: str, reference_id: str) -> bool:
    """La cible désignée par (type, reference_id) existe-t-elle ?"""
    return resolve_reference(type_, reference_id) is not None
