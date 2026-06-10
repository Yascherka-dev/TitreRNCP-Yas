from django.db import models


class Beer(models.Model):
    nom          = models.CharField(max_length=200)
    brasserie    = models.CharField(max_length=200)
    pays         = models.CharField(max_length=50, db_index=True)
    region       = models.CharField(max_length=100, blank=True)
    equipe       = models.CharField(max_length=200, blank=True)
    style        = models.CharField(max_length=100)
    description  = models.TextField()
    degre_alcool = models.DecimalField(max_digits=4, decimal_places=1)
    image_url    = models.URLField(blank=True)
    generated_by = models.CharField(max_length=50, blank=True, default='ia')
    times_served = models.PositiveIntegerField(default=0)

    class Meta:
        verbose_name        = "Bière"
        verbose_name_plural = "Bières"
        ordering            = ['pays', 'nom']

    def __str__(self) -> str:
        return f"{self.nom} ({self.pays}) — {self.degre_alcool}°"
