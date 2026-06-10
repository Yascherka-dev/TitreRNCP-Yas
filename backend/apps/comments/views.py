from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
from rest_framework.response import Response
from .models import Comment
from .serializers import CommentSerializer


class CommentListView(generics.ListCreateAPIView):
    permission_classes = [IsAuthenticatedOrReadOnly]
    serializer_class = CommentSerializer

    def get_queryset(self):
        type_ = self.request.query_params.get('type')
        ref = self.request.query_params.get('reference_id')
        qs = Comment.objects.all()
        if type_:
            qs = qs.filter(type=type_)
        if ref:
            qs = qs.filter(reference_id=ref)
        return qs

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class CommentDetailView(generics.DestroyAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = CommentSerializer

    def get_queryset(self):
        return Comment.objects.filter(user=self.request.user)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response(status=status.HTTP_204_NO_CONTENT)
