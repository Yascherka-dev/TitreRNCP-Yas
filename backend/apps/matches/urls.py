from django.urls import path
from .views import MatchListView, SynchronizeView

urlpatterns = [
    path('', MatchListView.as_view(), name='match-list'),
    path('synchroniser/', SynchronizeView.as_view(), name='match-synchroniser'),
]
