from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
from rest_framework.response import Response

from apps.cible_serializer import filtrer_par_cible
from .models import Comment
from .serializers import CommentSerializer

CIBLES = ('user', 'match', 'recette', 'biere')


class CommentListView(generics.ListCreateAPIView):
    permission_classes = [IsAuthenticatedOrReadOnly]
    serializer_class = CommentSerializer

    def get_queryset(self):
        return filtrer_par_cible(
            Comment.objects.select_related(*CIBLES),
            self.request.query_params.get('type'),
            self.request.query_params.get('reference_id'),
        )

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class CommentDetailView(generics.DestroyAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = CommentSerializer

    def get_queryset(self):
        return Comment.objects.filter(user=self.request.user).select_related(*CIBLES)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response(status=status.HTTP_204_NO_CONTENT)
