from django.urls import path
from .views import RatingListView

urlpatterns = [
    path('', RatingListView.as_view(), name='rating-list'),
]
