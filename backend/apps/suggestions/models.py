from django.db import models

from django.db import models
from apps.matches.models import Match
from apps.recipes.models import Recipe


class Suggestion(models.Model):
    match = models.ForeignKey(Match, on_delete=models.CASCADE, related_name='suggestions')
    recette_a = models.ForeignKey(Recipe, on_delete=models.SET_NULL, null=True, related_name='suggestions_a')
    recette_b = models.ForeignKey(Recipe, on_delete=models.SET_NULL, null=True, related_name='suggestions_b')
    date_generation = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Suggestion pour {self.match}"
