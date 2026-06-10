from django.contrib import admin
from .models import Beer


@admin.register(Beer)
class BeerAdmin(admin.ModelAdmin):
    list_display = ['nom', 'brasserie', 'pays', 'style', 'degre_alcool', 'times_served']
    list_filter = ['pays', 'style']
    search_fields = ['nom', 'brasserie', 'pays']
    ordering = ['pays', 'nom']
