import random

from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.beers.models import Beer
from apps.recipes.models import Recipe

CLUB_REGION_MAP: dict[str, str] = {
    'paris saint-germain':       'Île-de-France',
    'olympique de marseille':    'Provence',
    'ogc nice':                  'Provence',
    'as monaco':                 'Provence',
    'olympique lyonnais':        'Bourgogne',
    'stade brest 29':            'Bretagne',
    'stade rennais fc':          'Bretagne',
    'stade rennais':             'Bretagne',
    'rc lens':                   'Nord',
    'losc lille':                'Nord',
    'rc strasbourg alsace':      'Alsace',
    'racing club de strasbourg': 'Alsace',
    'fc metz':                   'Lorraine',
    'toulouse fc':               'Occitanie',
    'montpellier hsc':           'Occitanie',
    'fc nantes':                 'Loire',
    'angers sco':                'Loire',
    'havre ac':                  'Normandie',
    'as saint-étienne':          'Bourgogne',
    'stade de reims':            'Champagne',
    'girondins de bordeaux':     'Provence',
}


class SuggestionView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        pays_a   = (request.data.get("paysA")   or "").lower().strip()
        pays_b   = (request.data.get("paysB")   or "").lower().strip()
        equipe_a = (request.data.get("equipeA") or "").strip()
        equipe_b = (request.data.get("equipeB") or "").strip()

        if not pays_a or not pays_b:
            return Response(
                {"error": "paysA et paysB sont requis"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        same_country = bool(pays_a and pays_b and pays_a == pays_b)
        region_a = CLUB_REGION_MAP.get(equipe_a.lower(), '') if same_country else ''
        region_b = CLUB_REGION_MAP.get(equipe_b.lower(), '') if same_country else ''

        return Response({
            "recette_a":      self._pick_recipe(equipe_a, pays_a, Recipe.TYPE_SALE,  region_a),
            "recette_b":      self._pick_recipe(equipe_b, pays_b, Recipe.TYPE_SALE,  region_b),
            "peche_mignon_a": self._pick_recipe(equipe_a, pays_a, Recipe.TYPE_SUCRE, region_a),
            "peche_mignon_b": self._pick_recipe(equipe_b, pays_b, Recipe.TYPE_SUCRE, region_b),
            "biere_a":        self._pick_beer(equipe_a, pays_a),
            "biere_b":        self._pick_beer(equipe_b, pays_b),
        })

    def _pick_recipe(self, equipe: str, pays: str, type_plat: str, region: str = '') -> dict | None:
        # 1. Par équipe exacte
        qs = Recipe.objects.filter(equipe__iexact=equipe, type_plat=type_plat) if equipe else Recipe.objects.none()
        # 2. Par région (matchs domestiques)
        if not qs.exists() and region:
            qs = Recipe.objects.filter(region__iexact=region, type_plat=type_plat)
        # 3. Fallback pays
        if not qs.exists():
            qs = Recipe.objects.filter(pays__iexact=pays, type_plat=type_plat)
        if not qs.exists():
            return None
        recipe = random.choice(list(qs))
        Recipe.objects.filter(pk=recipe.pk).update(times_served=recipe.times_served + 1)
        return self._recipe_dict(recipe)

    def _pick_beer(self, equipe: str, pays: str) -> dict | None:
        qs = Beer.objects.filter(equipe=equipe) if equipe else Beer.objects.none()
        if not qs.exists():
            qs = Beer.objects.filter(pays__iexact=pays)
        if not qs.exists():
            return None
        beer = random.choice(list(qs))
        Beer.objects.filter(pk=beer.pk).update(times_served=beer.times_served + 1)
        return self._beer_dict(beer)

    def _recipe_dict(self, r: Recipe) -> dict:
        return {
            "id":                str(r.id),
            "titre":             r.titre,
            "pays":              r.pays,
            "region":            r.region,
            "equipe":            r.equipe,
            "type_plat":         r.type_plat,
            "description":       r.description,
            "temps_preparation": r.temps_preparation,
            "temps_cuisson":     r.temps_cuisson,
            "nb_personnes":      r.nb_personnes,
            "difficulte":        r.difficulte,
            "ingredients":       r.ingredients,
            "etapes":            r.etapes,
            "tags":              r.tags,
            "image_url":         r.image_url,
        }

    def _beer_dict(self, b: Beer) -> dict:
        return {
            "id":           str(b.id),
            "nom":          b.nom,
            "brasserie":    b.brasserie,
            "pays":         b.pays,
            "region":       b.region,
            "equipe":       b.equipe,
            "style":        b.style,
            "description":  b.description,
            "degre_alcool": str(b.degre_alcool) if b.degre_alcool else None,
            "image_url":    b.image_url,
        }
