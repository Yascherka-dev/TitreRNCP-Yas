from django.conf import settings
from django.db import models

from apps.cible import CibleReference


class Favorite(CibleReference):
    """
    Un utilisateur met en favori un match, une recette ou une bière.

    L'unicité par couple (utilisateur, cible) est portée par la base : c'est
    ce qui autorise à modéliser FAVORISER comme une association MERISE et non
    comme une entité — une occurrence par couple, pas davantage.
    """

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='favorites')
    date_ajout = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Favori"
        verbose_name_plural = "Favoris"
        constraints = [
            CibleReference.contrainte_cible_unique('favori_cible_unique'),
            models.UniqueConstraint(fields=['user', 'match'],   name='favori_unique_par_match'),
            models.UniqueConstraint(fields=['user', 'recette'], name='favori_unique_par_recette'),
            models.UniqueConstraint(fields=['user', 'biere'],   name='favori_unique_par_biere'),
        ]
