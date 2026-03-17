# Service football : appelle l'API football-data.org et retourne les matchs
# dans le format attendu par le modèle Match de models.py.
# Ce fichier ne touche PAS à la base de données — il retourne juste des données propres.

import requests
from django.conf import settings
from django.utils.dateparse import parse_datetime

API_TIMEOUT = 10

# Liste des compétitions à synchroniser (codes football-data.org)
COMPETITIONS = ['FL1', 'CL']


def fetch_fixtures(date=None):
    """
    Boucle sur chaque compétition et accumule les matchs.
    Si date est fournie (YYYY-MM-DD) → matchs de ce jour seulement.
    Si date est None → tous les matchs de la saison en cours.
    """
    resultats = []

    for code in COMPETITIONS:
        resultats += _fetch_competition(code, date)

    return resultats


def _fetch_team_countries(code):
    """
    Appelle /v4/competitions/{code}/teams pour récupérer le pays de chaque équipe.
    Retourne un dict { team_id: country_name_lower }.
    """
    try:
        r = requests.get(
            f'https://api.football-data.org/v4/competitions/{code}/teams',
            headers={'X-Auth-Token': settings.API_FOOTBALL_KEY},
            timeout=API_TIMEOUT,
        )
        teams = r.json().get('teams', [])
        return {t['id']: t.get('area', {}).get('name', '').lower() for t in teams}
    except Exception:
        return {}


def _fetch_competition(code, date=None):
    """
    Appelle l'API pour une compétition donnée (ex: 'FL1', 'CL').
    Retourne une liste de dicts ou [] en cas d'erreur.
    """
    team_countries = _fetch_team_countries(code)

    params = {'dateFrom': date, 'dateTo': date} if date else {}

    try:
        r = requests.get(
            f'https://api.football-data.org/v4/competitions/{code}/matches',
            headers={'X-Auth-Token': settings.API_FOOTBALL_KEY},
            params=params,
            timeout=API_TIMEOUT,
        )
        matches = r.json().get('matches', [])
    except Exception:
        return []

    resultats = []

    for m in matches:
        home_team   = m.get('homeTeam', {})
        away_team   = m.get('awayTeam', {})
        competition = m.get('competition', {})
        score       = m.get('score', {})
        full_time   = score.get('fullTime', {})
        area        = m.get('area', {})

        # Ignorer les matchs dont les équipes ne sont pas encore connues
        if not home_team.get('name') or not away_team.get('name'):
            continue

        fallback = area.get('name', '').lower()

        match_data = {
            'external_id': f'football_{m.get("id")}',
            'sport':       'football',
            'competition': competition.get('name', ''),
            'equipe_a':    home_team.get('name', ''),
            'equipe_b':    away_team.get('name', ''),
            'pays_a':      team_countries.get(home_team.get('id'), fallback),
            'pays_b':      team_countries.get(away_team.get('id'), fallback),
            'date_heure':  parse_datetime(m.get('utcDate', '')),
            'statut':      m.get('status', 'SCHEDULED'),
            'score_a':     full_time.get('home'),
            'score_b':     full_time.get('away'),
            'logo_a':      home_team.get('crest', ''),
            'logo_b':      away_team.get('crest', ''),
        }

        resultats.append(match_data)

    return resultats
