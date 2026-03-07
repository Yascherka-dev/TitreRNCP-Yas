from django.contrib import admin
from .models import Match

@admin.register(Match)
class MatchAdmin(admin.ModelAdmin):
    list_display = ['equipe_a', 'equipe_b', 'competition', 'sport', 'date_heure']
    list_filter = ['sport', 'competition']
