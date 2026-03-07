from django.urls import path
from .views import FavoriteListView, FavoriteDeleteView

urlpatterns = [
    path('', FavoriteListView.as_view(), name='favorite-list'),
    path('<int:pk>/', FavoriteDeleteView.as_view(), name='favorite-delete'),
]
