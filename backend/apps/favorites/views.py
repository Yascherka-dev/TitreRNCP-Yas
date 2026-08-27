from django.db import IntegrityError, transaction

from rest_framework import generics
from rest_framework.exceptions import ValidationError
from rest_framework.permissions import IsAuthenticated

from .models import Favorite
from .serializers import FavoriteSerializer

# Les trois cibles sont chargées avec le favori : sans cela, chaque
# `reference_id` du listing déclencherait sa propre requête.
CIBLES = ('match', 'recette', 'biere')


class FavoriteListView(generics.ListCreateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = FavoriteSerializer

    def get_queryset(self):
        return (Favorite.objects
                .filter(user=self.request.user)
                .select_related(*CIBLES))

    def perform_create(self, serializer):
        try:
            # `atomic` isole l'échec : sans lui, l'IntegrityError laisserait
            # la transaction PostgreSQL inutilisable pour la suite de la requête.
            with transaction.atomic():
                serializer.save(user=self.request.user)
        except IntegrityError:
            raise ValidationError({"detail": "Ce favori existe déjà."})


class FavoriteDeleteView(generics.DestroyAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = FavoriteSerializer

    def get_queryset(self):
        return Favorite.objects.filter(user=self.request.user).select_related(*CIBLES)
