from rest_framework import generics
from rest_framework.permissions import IsAuthenticatedOrReadOnly
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
