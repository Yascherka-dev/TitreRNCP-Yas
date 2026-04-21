from django.db import models


class Recipe(models.Model):
    titre             = models.CharField(max_length=200)
    pays              = models.CharField(max_length=50)
    description       = models.TextField()
    temps_preparation = models.PositiveIntegerField(help_text="En minutes")
    temps_cuisson     = models.PositiveIntegerField(default=0, help_text="En minutes")
    nb_personnes      = models.PositiveIntegerField(default=4)
    difficulte        = models.CharField(max_length=20, default='Facile')
    ingredients       = models.JSONField(default=list)
    etapes            = models.JSONField(default=list)
    tags              = models.JSONField(default=list)
    image_url         = models.URLField(max_length=500, blank=True)

    def __str__(self):
        return f"{self.titre} ({self.pays})"
