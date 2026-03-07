from rest_framework import generics
from rest_framework.permissions import AllowAny
from .models import Recipe
from .serializers import RecipeSerializer


class RecipeListView(generics.ListAPIView):
    permission_classes = [AllowAny]
    serializer_class = RecipeSerializer
    queryset = Recipe.objects.all()
