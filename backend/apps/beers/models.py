from django.db import models


class Beer(models.Model):
    SOURCE_IA     = 'ia'
    SOURCE_MANUAL = 'manual'
    SOURCE_CHOICES = [(SOURCE_IA, 'IA'), (SOURCE_MANUAL, 'Manuel')]

    nom          = models.CharField(max_length=200)
    brasserie    = models.CharField(max_length=200, blank=True)
    pays         = models.CharField(max_length=50)
    region       = models.CharField(max_length=100, blank=True)
    equipe       = models.CharField(max_length=150, blank=True)
    style        = models.CharField(max_length=100, blank=True)
    description  = models.TextField()
    degre_alcool = models.DecimalField(max_digits=4, decimal_places=1, null=True, blank=True)
    image_url    = models.URLField(max_length=500, blank=True)
    generated_by = models.CharField(max_length=10, choices=SOURCE_CHOICES, default=SOURCE_MANUAL)
    times_served = models.PositiveIntegerField(default=0)

    def __str__(self):
        return f"{self.nom} — {self.brasserie} ({self.pays})"
