from django.db import models

class Match(models.Model):
    SPORT_CHOICES = [('football', 'Football'), ('rugby', 'Rugby'), ('basketball', 'Basketball')]

    sport = models.CharField(max_length=50, choices=SPORT_CHOICES, default='football')
    competition = models.CharField(max_length=100)
    equipe_a = models.CharField(max_length=100)
    equipe_b = models.CharField(max_length=100)
    pays_a = models.CharField(max_length=10)
    pays_b = models.CharField(max_length=10)
    date_heure = models.DateTimeField()
    watch_url = models.URLField(blank=True)
    delivery_url = models.URLField(blank=True)

    def __str__(self):
        return f"{self.equipe_a} vs {self.equipe_b} — {self.competition}"

