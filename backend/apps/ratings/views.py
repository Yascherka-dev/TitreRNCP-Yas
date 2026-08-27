from django.db import IntegrityError, transaction

from rest_framework import generics, status
from rest_framework.exceptions import ValidationError
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
from rest_framework.response import Response

from apps.cible_serializer import filtrer_par_cible
from .models import Rating
from .serializers import RatingSerializer

CIBLES = ('user', 'match', 'recette', 'biere')


class RatingListView(generics.ListCreateAPIView):
    permission_classes = [IsAuthenticatedOrReadOnly]
    serializer_class = RatingSerializer

    def get_queryset(self):
        return filtrer_par_cible(
            Rating.objects.select_related(*CIBLES),
            self.request.query_params.get('type'),
            self.request.query_params.get('reference_id'),
        )

    def perform_create(self, serializer):
        try:
            with transaction.atomic():
                serializer.save(user=self.request.user)
        except IntegrityError:
            raise ValidationError({"detail": "Une note existe déjà pour cet élément."})


class RatingDetailView(generics.DestroyAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = RatingSerializer

    def get_queryset(self):
        return Rating.objects.filter(user=self.request.user).select_related(*CIBLES)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response(status=status.HTTP_204_NO_CONTENT)
