from rest_framework import generics
from rest_framework.permissions import AllowAny
from .models import Beer
from .serializers import BeerSerializer


class BeerListView(generics.ListAPIView):
    """GET /api/beers/ — liste toutes les bières, filtre optionnel ?pays=france"""
    permission_classes = [AllowAny]
    serializer_class = BeerSerializer

    def get_queryset(self):
        queryset = Beer.objects.all()
        pays = self.request.query_params.get('pays')
        if pays:
            queryset = queryset.filter(pays=pays.lower().strip())
        return queryset


class BeerDetailView(generics.RetrieveAPIView):
    """GET /api/beers/<id>/"""
    permission_classes = [AllowAny]
    serializer_class = BeerSerializer
    queryset = Beer.objects.all()
