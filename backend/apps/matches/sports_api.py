"""
Service TheSportsDB — remplace football_api.py.
V1 (clé dans l'URL) pour les fixtures saisonnières.
V2 (header X-API-KEY) pour les livescores.
"""

import requests
from django.conf import settings
from django.utils.dateparse import parse_datetime
from django.utils.timezone import make_aware, is_aware

API_V1 = 'https://www.thesportsdb.com/api/v1/json'
API_V2 = 'https://www.thesportsdb.com/api/v2/json'
TIMEOUT = 15

# ── Ligues configurées ────────────────────────────────────────────────────────
# country=None → multi-pays (CL, Coupe du monde...) → lookup par équipe
LEAGUES = [
    dict(id=4334, sport='football',          season='2025-2026', country='france'),  # Ligue 1
    dict(id=4480, sport='football',          season='2025-2026', country=None),      # CL
    dict(id=4387, sport='basketball',        season='2025-2026', country='usa'),     # NBA
    dict(id=4391, sport='american_football', season='2025-2026', country='usa'),     # NFL
    dict(id=4380, sport='ice_hockey',        season='2025-2026', country='usa'),     # NHL
    dict(id=4430, sport='rugby',             season='2025-2026', country='france'),  # Top 14
    dict(id=4714, sport='rugby',             season='2026',      country=None),      # Six Nations
    dict(id=4429, sport='football',          season='2026',      country=None),      # FIFA World Cup 2026
]

# Cache en mémoire : idTeam (str) → pays normalisé
_team_country_cache: dict[str, str] = {}

# Statuts longs (schedule) → codes courts
_STATUS_MAP = {
    # Generiques
    'Not Started':       'NS',
    'Match Finished':    'FT',
    'Game Finished':     'FT',
    'After Extra Time':  'AET',
    'After Overtime':    'AET',
    'AOT':               'AET',
    'After Penalties':   'PEN',
    'Match Postponed':   'PST',
    'Postponed':         'PST',
    'Match Abandoned':   'ABD',
    'Cancelled':         'CANC',
    'Match Suspended':   'SUSP',
    # Football / Soccer
    'First Half':        '1H',
    'Half Time':         'HT',
    'Second Half':       '2H',
    'Extra Time':        'ET',
    'Penalty Shootout':  'P',
    'Break Time':        'BT',
    # Rugby / Basketball / autres sports
    '1st Half':          '1H',
    '2nd Half':          '2H',
    'Half-Time':         'HT',
    'Half Time Break':   'HT',
    'In Progress':       '2H',
    'Live':              '2H',
    'Q1':                '1H',
    'Q2':                '1H',
    'Q3':                '2H',
    'Q4':                '2H',
    'OT':                'ET',
    'Overtime':          'ET',
    'Period 1':          '1H',
    'Period 2':          '2H',
    'Period 3':          '2H',
}

# Noms de sports TheSportsDB → clés internes
_SPORT_MAP = {
    'Soccer':            'football',
    'Basketball':        'basketball',
    'Ice Hockey':        'ice_hockey',
    'American Football': 'american_football',
    'Rugby':             'rugby',
    'Tennis':            'tennis',
    'Baseball':          'baseball',
    'Cricket':           'cricket',
}


def _parse_aware(value: str):
    dt = parse_datetime(value or '')
    if dt is None:
        return None
    return dt if is_aware(dt) else make_aware(dt)


def _key() -> str:
    return settings.SPORTSDB_KEY


def _v1(endpoint: str, **params) -> dict:
    url = f'{API_V1}/{_key()}/{endpoint}'
    r = requests.get(url, params=params, timeout=TIMEOUT)
    r.raise_for_status()
    return r.json()


def _v2(path: str) -> dict:
    url = f'{API_V2}/{path}'
    r = requests.get(url, headers={'X-API-KEY': _key()}, timeout=TIMEOUT)
    r.raise_for_status()
    return r.json()


def _map_status(raw: str) -> str:
    return _STATUS_MAP.get(raw, raw or 'NS')


def _map_sport(raw: str) -> str:
    return _SPORT_MAP.get(raw, raw.lower() if raw else 'football')


def _normalise_country(name: str) -> str:
    return (name or '').strip().lower()


def _build_team_country_map(league_name: str) -> dict[str, str]:
    """Fetch all teams for a league and return {idTeam: country}."""
    try:
        data = _v1('search_all_teams.php', l=league_name)
        teams = data.get('teams') or []
        return {
            str(t['idTeam']): _normalise_country(t.get('strCountry', ''))
            for t in teams
        }
    except Exception:
        return {}


def _get_team_country(team_id: str, league_name: str) -> str:
    if team_id in _team_country_cache:
        return _team_country_cache[team_id]
    # Batch-load the whole league into cache on first miss
    mapping = _build_team_country_map(league_name)
    _team_country_cache.update(mapping)
    return _team_country_cache.get(team_id, '')


def _parse_score(val) -> int | None:
    try:
        return int(val)
    except (TypeError, ValueError):
        return None


def _to_match_dict(event: dict, league_cfg: dict) -> dict | None:
    home_name = event.get('strHomeTeam', '')
    away_name = event.get('strAwayTeam', '')
    if not home_name or not away_name:
        return None

    status_raw = event.get('strStatus', 'Not Started')
    statut = _map_status(status_raw)

    if league_cfg['country']:
        pays_a = pays_b = league_cfg['country']
    else:
        pays_a = _get_team_country(str(event.get('idHomeTeam', '')), event.get('strLeague', ''))
        pays_b = _get_team_country(str(event.get('idAwayTeam', '')), event.get('strLeague', ''))
        # Pour les tournois internationaux le nom d'équipe = pays quand le lookup échoue
        if not pays_a:
            pays_a = _normalise_country(home_name)
        if not pays_b:
            pays_b = _normalise_country(away_name)

    return {
        'external_id': f'sdb_{event["idEvent"]}',
        'sport':       league_cfg['sport'],
        'competition': event.get('strLeague', ''),
        'league_id':   int(event.get('idLeague') or league_cfg['id']),
        'equipe_a':    home_name,
        'equipe_b':    away_name,
        'pays_a':      pays_a,
        'pays_b':      pays_b,
        'date_heure':  _parse_aware(event.get('strTimestamp', '')),
        'statut':      statut,
        'score_a':     _parse_score(event.get('intHomeScore')),
        'score_b':     _parse_score(event.get('intAwayScore')),
        'logo_a':      event.get('strHomeTeamBadge') or '',
        'logo_b':      event.get('strAwayTeamBadge') or '',
        'venue':       event.get('strVenue') or '',
        'thumb_url':   event.get('strThumb') or event.get('strPoster') or '',
    }


# ── API publique ──────────────────────────────────────────────────────────────

def fetch_fixtures(date: str | None = None) -> list[dict]:
    """
    Récupère les fixtures depuis TheSportsDB V2 pour toutes les ligues configurées.
    Si date (YYYY-MM-DD) → filtre par jour via V1 eventsday.
    Si None → saison complète via V2 schedule/league.
    """
    results: list[dict] = []

    if date:
        # Récupération par jour : on appelle eventsday pour chaque ligue
        league_ids = {str(cfg['id']) for cfg in LEAGUES}
        cfg_by_id = {str(cfg['id']): cfg for cfg in LEAGUES}
        try:
            data = _v1('eventsday.php', d=date, s='Soccer')
            events = data.get('events') or []
            # TheSportsDB peut retourner plusieurs sports sur eventsday
            # on filtre sur nos ligues
            for event in events:
                lid = str(event.get('idLeague', ''))
                cfg = cfg_by_id.get(lid)
                if cfg:
                    m = _to_match_dict(event, cfg)
                    if m:
                        results.append(m)
        except Exception:
            pass
        return results

    # Saison complète
    for cfg in LEAGUES:
        try:
            data = _v2(f'schedule/league/{cfg["id"]}/{cfg["season"]}')
            events = data.get('schedule') or []
            for event in events:
                m = _to_match_dict(event, cfg)
                if m:
                    results.append(m)
        except Exception:
            continue

    return results


def fetch_livescores() -> list[dict]:
    """
    Combine livescores V2 (matchs en direct) + résultats du jour via eventsday V1.
    Garantit que les matchs terminés dans la journée passent bien en FT.
    """
    from datetime import date
    results: list[dict] = []
    seen: set[str] = set()
    tracked_league_ids = {cfg['id'] for cfg in LEAGUES}
    cfg_by_id = {cfg['id']: cfg for cfg in LEAGUES}

    # 1. Livescores en direct (V2)
    try:
        data = _v2('livescore/all')
        for event in (data.get('livescore') or []):
            league_id = int(event.get('idLeague') or 0)
            if league_id not in tracked_league_ids:
                continue
            ext_id = f'sdb_{event["idEvent"]}'
            results.append({
                'external_id': ext_id,
                'statut':  _map_status(event.get('strStatus', 'NS')),
                'score_a': _parse_score(event.get('intHomeScore')),
                'score_b': _parse_score(event.get('intAwayScore')),
            })
            seen.add(ext_id)
    except Exception:
        pass

    # 2. Résultats du jour (V1) — met à jour les matchs terminés hors livescore
    today = date.today().strftime('%Y-%m-%d')
    for sport_label, sports in [('Soccer', {'football'}), ('Basketball', {'basketball'}),
                                  ('Ice Hockey', {'ice_hockey'}), ('Rugby', {'rugby'})]:
        try:
            data = _v1('eventsday.php', d=today, s=sport_label)
            for event in (data.get('events') or []):
                league_id = int(event.get('idLeague') or 0)
                if league_id not in tracked_league_ids:
                    continue
                ext_id = f'sdb_{event["idEvent"]}'
                if ext_id in seen:
                    continue  # déjà couvert par le livescore
                statut = _map_status(event.get('strStatus', 'NS'))
                if statut == 'NS':
                    continue  # pas encore commencé, inutile de mettre à jour
                results.append({
                    'external_id': ext_id,
                    'statut':  statut,
                    'score_a': _parse_score(event.get('intHomeScore')),
                    'score_b': _parse_score(event.get('intAwayScore')),
                })
                seen.add(ext_id)
        except Exception:
            continue

    return results
