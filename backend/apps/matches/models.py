from django.db import models


class Match(models.Model):
    external_id = models.CharField(max_length=50, unique=True)
    sport       = models.CharField(max_length=50, default='football')
    competition = models.CharField(max_length=100)
    league_id   = models.IntegerField(null=True, blank=True)
    equipe_a    = models.CharField(max_length=100)
    equipe_b    = models.CharField(max_length=100)
    pays_a      = models.CharField(max_length=50, blank=True)
    pays_b      = models.CharField(max_length=50, blank=True)
    date_heure  = models.DateTimeField()
    statut      = models.CharField(max_length=10, default='NS')
    score_a     = models.IntegerField(null=True, blank=True)
    score_b     = models.IntegerField(null=True, blank=True)
    logo_a      = models.URLField(blank=True)
    logo_b      = models.URLField(blank=True)
    venue       = models.CharField(max_length=200, blank=True)
    thumb_url   = models.URLField(blank=True)

    def __str__(self):
        return f"{self.equipe_a} vs {self.equipe_b} — {self.competition}"
