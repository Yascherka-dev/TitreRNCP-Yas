from django.conf import settings
from django.db import models


class Recipe(models.Model):
    SOURCE_IA     = 'ia'
    SOURCE_MANUAL = 'manual'
    SOURCE_CHOICES = [(SOURCE_IA, 'IA'), (SOURCE_MANUAL, 'Manuel')]

    TYPE_SALE  = 'salé'
    TYPE_SUCRE = 'sucré'
    TYPE_CHOICES = [(TYPE_SALE, 'Salé'), (TYPE_SUCRE, 'Sucré')]

    titre             = models.CharField(max_length=200)
    pays              = models.CharField(max_length=50)
    region            = models.CharField(max_length=100, blank=True)
    equipe            = models.CharField(max_length=150, blank=True)
    description       = models.TextField()
    temps_preparation = models.PositiveIntegerField(help_text="En minutes")
    temps_cuisson     = models.PositiveIntegerField(default=0, help_text="En minutes")
    nb_personnes      = models.PositiveIntegerField(default=4)
    type_plat         = models.CharField(max_length=10, choices=TYPE_CHOICES, default=TYPE_SALE)
    difficulte        = models.CharField(max_length=20, default='Facile')
    ingredients       = models.JSONField(default=list)
    etapes            = models.JSONField(default=list)
    tags              = models.JSONField(default=list)
    image_url         = models.URLField(max_length=500, blank=True)
    generated_by      = models.CharField(max_length=10, choices=SOURCE_CHOICES, default=SOURCE_MANUAL)
    times_served      = models.PositiveIntegerField(default=0)


    # -- Relations ManyToMany (tables de liaison portées par Favorite/Rating) --
    # `through_fields` lève l'ambiguïté : Favorite et Rating portent trois clés
    # étrangères de cible, il faut désigner laquelle mène jusqu'ici.
    utilisateurs_favoris = models.ManyToManyField(
        settings.AUTH_USER_MODEL, through='favorites.Favorite',
        through_fields=('recette', 'user'),
        related_name='recettes_favorites', blank=True)
    utilisateurs_notes = models.ManyToManyField(
        settings.AUTH_USER_MODEL, through='ratings.Rating',
        through_fields=('recette', 'user'),
        related_name='recettes_notees', blank=True)

    def __str__(self):
        return f"{self.titre} ({self.pays})"
