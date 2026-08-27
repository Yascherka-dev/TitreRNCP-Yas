"""
Socle commun à Favorite, Comment et Rating : la cible de la référence.

Ces trois modèles visent une cible parmi trois — un match, une recette ou une
bière. Plutôt que trois tables par modèle (neuf au total), chacun porte trois
clés étrangères nullables et une contrainte qui garantit qu'exactement une est
renseignée. La base retrouve ainsi ce qu'un couple (type, reference_id) lui
retirait : le refus des références invalides et la suppression en cascade.

C'est la traduction relationnelle de la contrainte d'exclusion totale (XT) du
MCD : trois branches, exactement une empruntée. Voir docs/MERISE.md.
"""

from django.core.exceptions import ValidationError
from django.db import models


class CibleReference(models.Model):
    """
    Trois liaisons exclusives, et la traduction vers le couple (type,
    reference_id) attendu par l'API.

    `related_name='%(class)ss'` donne `match.favorites`, `recette.comments`,
    `biere.ratings` — un nom par modèle concret, sans collision.
    """

    match = models.ForeignKey(
        'matches.Match', null=True, blank=True,
        on_delete=models.CASCADE, related_name='%(class)ss')
    recette = models.ForeignKey(
        'recipes.Recipe', null=True, blank=True,
        on_delete=models.CASCADE, related_name='%(class)ss')
    biere = models.ForeignKey(
        'beers.Beer', null=True, blank=True,
        on_delete=models.CASCADE, related_name='%(class)ss')

    class Meta:
        abstract = True

    # -- Lecture ----------------------------------------------------------

    @property
    def cible(self) -> models.Model | None:
        """L'objet visé, quel que soit son type."""
        return self.match or self.recette or self.biere

    @property
    def type(self) -> str | None:
        """Le type tel que l'API l'expose : 'match', 'recette' ou 'biere'."""
        if self.match_id:
            return 'match'
        if self.recette_id:
            return 'recette'
        if self.biere_id:
            return 'biere'
        return None

    @property
    def reference_id(self) -> str | None:
        """
        L'identifiant tel que l'API l'expose.

        Un match est désigné par son `external_id` (« sdb_2528727 »), une
        recette et une bière par leur clé primaire numérique.
        """
        if self.match_id:
            return self.match.external_id
        if self.recette_id:
            return str(self.recette_id)
        if self.biere_id:
            return str(self.biere_id)
        return None

    # -- Écriture ---------------------------------------------------------

    def clean(self):
        """Double de la contrainte de base, pour un message lisible côté admin."""
        renseignees = [f for f in (self.match_id, self.recette_id, self.biere_id) if f]
        if len(renseignees) != 1:
            raise ValidationError(
                "Il faut viser exactement une cible : un match, une recette "
                "ou une bière."
            )

    def __str__(self) -> str:
        return f"{self.user} — {self.type} #{self.reference_id}"

    # -- Contraintes ------------------------------------------------------

    @staticmethod
    def contrainte_cible_unique(nom: str) -> models.CheckConstraint:
        """
        Exactement une des trois liaisons est renseignée.

        À déclarer dans le Meta de chaque modèle concret : un nom de contrainte
        est unique à l'échelle de la base.
        """
        exactement_une = (
            models.Q(match__isnull=False, recette__isnull=True,  biere__isnull=True)
            | models.Q(match__isnull=True,  recette__isnull=False, biere__isnull=True)
            | models.Q(match__isnull=True,  recette__isnull=True,  biere__isnull=False)
        )
        return models.CheckConstraint(condition=exactement_une, name=nom)
