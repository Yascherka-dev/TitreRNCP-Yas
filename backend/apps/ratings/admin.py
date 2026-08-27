from django.contrib import admin
from .models import Rating


@admin.register(Rating)
class RatingAdmin(admin.ModelAdmin):
    list_display = ['user', 'type', 'reference_id', 'valeur', 'date']
    list_select_related = ['user', 'match', 'recette', 'biere']
    list_filter = ['valeur', 'date']
