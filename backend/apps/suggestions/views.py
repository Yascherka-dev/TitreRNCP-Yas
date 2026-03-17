import random
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from rest_framework import status
from apps.recipes.models import Recipe
from apps.recipes.serializers import RecipeSerializer


class SuggestionView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        pays_a = (request.data.get('paysA') or '').lower().strip()
        pays_b = (request.data.get('paysB') or '').lower().strip()

        if not pays_a or not pays_b:
            return Response({'error': 'paysA et paysB sont requis'}, status=status.HTTP_400_BAD_REQUEST)

        recettes_a = list(Recipe.objects.filter(pays=pays_a))
        recettes_b = list(Recipe.objects.filter(pays=pays_b))

        if not recettes_a:
            return Response({'error': f'Aucune recette pour le pays : {pays_a}'}, status=status.HTTP_404_NOT_FOUND)
        if not recettes_b:
            return Response({'error': f'Aucune recette pour le pays : {pays_b}'}, status=status.HTTP_404_NOT_FOUND)

        return Response({
            'recettes': [
                RecipeSerializer(random.choice(recettes_a)).data,
                RecipeSerializer(random.choice(recettes_b)).data,
            ]
        })
