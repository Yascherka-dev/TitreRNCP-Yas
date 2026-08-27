from django.conf import settings
from django.db import models

from apps.cible import CibleReference


class Comment(CibleReference):
    """
    Un utilisateur commente un match, une recette ou une bière.

    Contrairement à FAVORISER et NOTER, aucune contrainte d'unicité : un même
    utilisateur peut commenter plusieurs fois le même élément. C'est pourquoi
    le MCD en fait une **entité** et non une association — une association
    n'admet qu'une occurrence par couple, le second commentaire écraserait le
    premier. Voir docs/MERISE.md.
    """

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='comments')
    contenu = models.TextField()
    date_soumission = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Commentaire"
        verbose_name_plural = "Commentaires"
        ordering = ['-date_soumission']
        constraints = [
            CibleReference.contrainte_cible_unique('commentaire_cible_unique'),
        ]
