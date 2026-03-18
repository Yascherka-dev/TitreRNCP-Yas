from django.db import models
from django.conf import settings


class Favorite(models.Model):
    TYPE_CHOICES = [('match', 'Match'), ('recette', 'Recette'), ('equipe', 'Équipe')]

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='favorites')
    type = models.CharField(max_length=10, choices=TYPE_CHOICES)
    reference_id = models.CharField(max_length=100)
    date_ajout = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'type', 'reference_id')

    def __str__(self):
        return f"{self.user} — {self.type} #{self.reference_id}"
