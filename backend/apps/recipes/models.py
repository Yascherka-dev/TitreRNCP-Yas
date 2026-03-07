from django.db import models


class Recipe(models.Model):
    titre = models.CharField(max_length=200)
    pays = models.CharField(max_length=10)
    description = models.TextField()
    temps_preparation = models.PositiveIntegerField(help_text="En minutes")
    image_url = models.URLField(blank=True)
    source_url = models.URLField(blank=True)

    def __str__(self):
        return f"{self.titre} ({self.pays})"
