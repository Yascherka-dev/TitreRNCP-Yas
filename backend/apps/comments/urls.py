from django.urls import path
from .views import CommentListView, CommentDetailView

urlpatterns = [
    path('', CommentListView.as_view(), name='comment-list'),
    path('<int:pk>/', CommentDetailView.as_view(), name='comment-detail'),
]
