from django.contrib import admin
from .models import Comment


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ['user', 'type', 'reference_id', 'date_soumission']
    list_select_related = ['user', 'match', 'recette', 'biere']
    list_filter = ['date_soumission']
