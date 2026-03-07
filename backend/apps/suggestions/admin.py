from django.contrib import admin
from .models import Suggestion

@admin.register(Suggestion)
class SuggestionAdmin(admin.ModelAdmin):
    list_display = ['match', 'recette_a', 'recette_b', 'date_generation']
