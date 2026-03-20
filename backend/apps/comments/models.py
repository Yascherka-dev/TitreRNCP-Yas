from django.db import models
from django.conf import settings


class Comment(models.Model):
    TYPE_CHOICES = [('match', 'Match'), ('recette', 'Recette')]

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='comments')
    type = models.CharField(max_length=10, choices=TYPE_CHOICES)
    reference_id = models.CharField(max_length=100)
    contenu = models.TextField()
    date_soumission = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user} — {self.type} #{self.reference_id}"
