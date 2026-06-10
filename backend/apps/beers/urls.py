from django.urls import path
from .views import BeerListView, BeerDetailView

urlpatterns = [
    path('', BeerListView.as_view(), name='beer-list'),
    path('<int:pk>/', BeerDetailView.as_view(), name='beer-detail'),
]
