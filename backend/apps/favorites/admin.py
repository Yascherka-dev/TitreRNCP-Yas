from django.contrib import admin
from .models import Favorite


@admin.register(Favorite)
class FavoriteAdmin(admin.ModelAdmin):
    list_display = ['user', 'type', 'reference_id', 'date_ajout']
    list_select_related = ['user', 'match', 'recette', 'biere']
    list_filter = ['date_ajout']
