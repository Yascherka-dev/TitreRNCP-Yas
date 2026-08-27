from django.conf import settings
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models

from apps.cible import CibleReference


class Rating(CibleReference):
    """
    Un utilisateur note un match, une recette ou une bière, de 1 à 5.

    Comme FAVORISER, l'unicité par couple (utilisateur, cible) en fait une
    association MERISE : une note par utilisateur et par élément noté.
    """

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='ratings')
    valeur = models.PositiveSmallIntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)])
    date = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Note"
        verbose_name_plural = "Notes"
        constraints = [
            CibleReference.contrainte_cible_unique('note_cible_unique'),
            models.UniqueConstraint(fields=['user', 'match'],   name='note_unique_par_match'),
            models.UniqueConstraint(fields=['user', 'recette'], name='note_unique_par_recette'),
            models.UniqueConstraint(fields=['user', 'biere'],   name='note_unique_par_biere'),
            models.CheckConstraint(
                condition=models.Q(valeur__gte=1) & models.Q(valeur__lte=5),
                name='note_entre_1_et_5'),
        ]

    def __str__(self) -> str:
        return f"{super().__str__()} : {self.valeur}/5"
