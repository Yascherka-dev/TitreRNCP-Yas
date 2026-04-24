from django.urls import path
from .views import MatchListView, SynchronizeView, LivescoresView

urlpatterns = [
    path('', MatchListView.as_view(), name='match-list'),
    path('synchroniser/', SynchronizeView.as_view(), name='match-synchroniser'),
    path('livescores/', LivescoresView.as_view(), name='livescores'),
]
