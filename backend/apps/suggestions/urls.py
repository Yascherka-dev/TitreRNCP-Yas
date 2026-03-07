from django.urls import path
from .views import SuggestionView

urlpatterns = [
    path('', SuggestionView.as_view(), name='suggestions'),
]
