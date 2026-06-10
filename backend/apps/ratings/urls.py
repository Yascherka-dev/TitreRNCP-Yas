from django.urls import path
from .views import RatingListView, RatingDetailView

urlpatterns = [
    path('', RatingListView.as_view(), name='rating-list'),
    path('<int:pk>/', RatingDetailView.as_view(), name='rating-detail'),
]
