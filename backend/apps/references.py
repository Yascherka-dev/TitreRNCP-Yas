"""
Intégrité des références polymorphes.

Favorite, Comment et Rating désignent leur cible par un couple
(type, reference_id) plutôt que par une clé étrangère. Ce choix évite de
multiplier les tables — un favori peut viser une recette, une bière ou un
match — mais il prive la base de toute garantie : PostgreSQL ne sait pas que
`reference_id` désigne quelque chose, donc rien n'empêche d'enregistrer une
référence vers un objet inexistant, ni de laisser des orphelins derrière soi
quand la cible disparaît.

Ce module rétablit la garantie au seul endroit où c'est possible :
à l'écriture, avant enregistrement.

Attention aux identifiants : l'API expose `Match.id` comme étant
`external_id` (« sdb_2528727 »), alors que recettes et bières sont désignées
par leur clé primaire numérique. Le front renvoie ce qu'il a reçu.
"""

from apps.beers.models import Beer
from apps.matches.models import Match
from apps.recipes.models import Recipe

#: Types acceptés dans le champ `type`, et façon de retrouver la cible.
REFERENCE_TYPES = ('recette', 'biere', 'match')


def reference_exists(type_: str, reference_id: str) -> bool:
    """La cible désignée par (type, reference_id) existe-t-elle ?"""
    ref = (reference_id or '').strip()
    if not ref:
        return False

    if type_ == 'match':
        # Désigné par external_id, pas par la clé primaire.
        return Match.objects.filter(external_id=ref).exists()

    model = {'recette': Recipe, 'biere': Beer}.get(type_)
    if model is None:
        return False

    # Clé primaire numérique : une référence non numérique ne peut pas exister.
    if not ref.isdigit():
        return False

    return model.objects.filter(pk=int(ref)).exists()


def purge_dead_references(dry_run: bool = False) -> dict[str, int]:
    """
    Supprime les lignes dont la cible a disparu, et renvoie le compte par table.

    La validation à l'écriture ne protège que du présent : un favori valide au
    moment du clic devient orphelin quand `sync_matches` purge le match sorti
    de la fenêtre J-30/J+60. Le nettoyage doit donc suivre chaque purge.

    Import local des modèles : ce module est importé par les serializers, qui
    le sont eux-mêmes au chargement des applications.
    """
    from apps.comments.models import Comment
    from apps.favorites.models import Favorite
    from apps.ratings.models import Rating

    resultat: dict[str, int] = {}

    for model, libelle in ((Favorite, 'favoris'), (Comment, 'commentaires'), (Rating, 'notes')):
        orphelins = [
            obj.pk for obj in model.objects.all()
            if not reference_exists(obj.type, obj.reference_id)
        ]
        if orphelins and not dry_run:
            model.objects.filter(pk__in=orphelins).delete()
        resultat[libelle] = len(orphelins)

    return resultat


def validate_reference(attrs: dict) -> dict:
    """
    Validateur partagé par les serializers Favorite, Comment et Rating.
    Lève une ValidationError si le type est inconnu ou la cible absente.
    """
    from rest_framework import serializers

    type_ = attrs.get('type')
    ref   = attrs.get('reference_id')

    if type_ not in REFERENCE_TYPES:
        raise serializers.ValidationError({
            'type': f"Type inconnu. Valeurs acceptées : {', '.join(REFERENCE_TYPES)}."
        })

    if not reference_exists(type_, ref):
        raise serializers.ValidationError({
            'reference_id': f"Aucun objet de type « {type_} » ne porte la référence « {ref} »."
        })

    return attrs
