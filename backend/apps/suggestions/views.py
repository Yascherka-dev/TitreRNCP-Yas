import json
import random
import re
import uuid

import anthropic
from django.conf import settings
from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

MARCO_SYSTEM = """Tu es Marco, chef cuisinier passionné de football et de cuisine du monde.
Tu as grandi entre les stades et les marchés, tu connais les spécialités de chaque région par cœur.
Quand tu proposes une recette pour un match, tu le fais avec enthousiasme et une pointe d'humour.
Tes descriptions sont courtes, vivantes, appétissantes — elles donnent envie de cuisiner tout de suite.
Tu parles en français, avec chaleur, comme si tu expliquais la recette à un ami avant le coup d'envoi.
Tu réponds UNIQUEMENT en JSON valide, sans texte autour."""

THEMES = [
    "street food et snacks populaires",
    "plat de brasserie ou bistrot régional",
    "recette de grand-mère transmise de génération en génération",
    "spécialité de marché ou de fête locale",
    "plat mijoté réconfortant",
    "grillades et barbecue",
    "cuisine côtière ou de port",
    "plat de montagne ou de campagne",
    "recette de fête nationale",
    "cuisine ouvrière et populaire",
]

PROMPT_SAME_COUNTRY = """Ce soir c'est {equipe_a} contre {equipe_b}, deux clubs de {pays} — un duel qui mérite une belle table !
Thème du soir : {theme}.
Propose une recette par club, ancrée dans la région géographique du club (pas la capitale par défaut).
La description : 2 à 3 phrases max, vivantes et appétissantes, comme tu la raconterais à un ami avant le match.
JSON uniquement :
{{"recettes":[{{"titre":"...","pays":"{pays}","description":"...","temps_preparation":0,"temps_cuisson":0,"nb_personnes":4,"difficulte":"Facile","ingredients":["..."],"etapes":["..."],"tags":["..."]}},{{"titre":"...","pays":"{pays}","description":"...","temps_preparation":0,"temps_cuisson":0,"nb_personnes":4,"difficulte":"Facile","ingredients":["..."],"etapes":["..."],"tags":["..."]}}]}}
Règles : difficulte = "Facile"|"Moyen"|"Difficile", 5-8 ingredients, 4-6 etapes, 3-4 tags."""

PROMPT_DIFF_COUNTRIES = """Ce soir c'est {pays_a} contre {pays_b} — deux cultures, deux cuisines, une soirée mémorable !
Thème du soir : {theme}.
Propose une recette authentique par pays — évite les clichés touristiques, cherche dans la cuisine régionale vraie.
La description : 2 à 3 phrases max, vivantes et appétissantes, comme tu la raconterais à un ami avant le match.
JSON uniquement :
{{"recettes":[{{"titre":"...","pays":"{pays_a}","description":"...","temps_preparation":0,"temps_cuisson":0,"nb_personnes":4,"difficulte":"Facile","ingredients":["..."],"etapes":["..."],"tags":["..."]}},{{"titre":"...","pays":"{pays_b}","description":"...","temps_preparation":0,"temps_cuisson":0,"nb_personnes":4,"difficulte":"Facile","ingredients":["..."],"etapes":["..."],"tags":["..."]}}]}}
Règles : difficulte = "Facile"|"Moyen"|"Difficile", 5-8 ingredients, 4-6 etapes, 3-4 tags."""


def _parse_json(text: str) -> dict:
    try:
        return json.loads(text)
    except json.JSONDecodeError:
        pass
    match = re.search(r'```(?:json)?\s*([\s\S]*?)\s*```', text)
    if match:
        return json.loads(match.group(1))
    raise ValueError("Réponse Claude non parseable en JSON")


class SuggestionView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        pays_a   = (request.data.get('paysA')   or '').lower().strip()
        pays_b   = (request.data.get('paysB')   or '').lower().strip()
        equipe_a = (request.data.get('equipeA') or '').strip()
        equipe_b = (request.data.get('equipeB') or '').strip()

        if not pays_a or not pays_b:
            return Response({'error': 'paysA et paysB sont requis'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            recettes = self._generate(pays_a, pays_b, equipe_a, equipe_b)
            return Response({'recettes': recettes})
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def _generate(self, pays_a, pays_b, equipe_a, equipe_b):
        theme = random.choice(THEMES)

        if pays_a == pays_b:
            prompt = PROMPT_SAME_COUNTRY.format(
                equipe_a=equipe_a or pays_a,
                equipe_b=equipe_b or pays_b,
                pays=pays_a,
                theme=theme,
            )
        else:
            prompt = PROMPT_DIFF_COUNTRIES.format(
                pays_a=pays_a,
                pays_b=pays_b,
                theme=theme,
            )

        client = anthropic.Anthropic(api_key=settings.ANTHROPIC_API_KEY)
        message = client.messages.create(
            model="claude-haiku-4-5-20251001",
            max_tokens=1500,
            temperature=1,
            system=MARCO_SYSTEM,
            messages=[{"role": "user", "content": prompt}],
        )

        raw = message.content[0].text.strip()
        data = _parse_json(raw)

        result = []
        for r in data.get("recettes", [])[:2]:
            r["id"] = str(uuid.uuid4())
            r["image_url"] = ""
            result.append(r)
        return result
