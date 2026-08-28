# Match & Munch

Plateforme web qui répond à : "On mange quoi devant le match de ce soir ?"
Pour chaque match sélectionné, deux recettes inspirées des pays des équipes qui s'affrontent.

## Stack

- **Frontend** — Angular 19 standalone + Angular Material + Figtree
- **Backend** — Django 6 + Django REST Framework
- **BDD** — PostgreSQL (Railway addon)
- **Auth** — JWT via djangorestframework-simplejwt
- **Données sportives** — TheSportsDB (API v1 et v2) : football, basket, hockey, rugby

## Lancer en local

### Backend

```bash
cd backend
python -m venv venv && source venv/bin/activate
pip install -r requirements.txt
cp .env.example .env  # renseigner les clés API
python manage.py migrate
python manage.py runserver
```

### Frontend

```bash
cd frontend
npm install
ng serve
```

L'app tourne sur `http://localhost:4200`, l'API sur `http://localhost:8000`.

## Variables d'environnement

Copier `backend/.env.example` en `backend/.env` et remplir les valeurs :

```
SECRET_KEY=
DEBUG=True

# PostgreSQL (locale ou Railway)
DB_NAME=matchmuunch
DB_USER=postgres
DB_PASSWORD=
DB_HOST=localhost
DB_PORT=5432

CORS_ALLOWED_ORIGINS=http://localhost:4200
ALLOWED_HOSTS=localhost,127.0.0.1

SPORTSDB_KEY=           # TheSportsDB (synchro des matchs et scores)
```

> PostgreSQL doit tourner en local avec une base `matchmuunch` créée au préalable (`createdb matchmuunch`).

## Endpoints principaux

| Méthode | Route | Accès | Description |
|---|---|---|---|
| POST | `/api/auth/register/` | public | Inscription |
| POST | `/api/auth/login/` | public | Connexion, retourne les jetons JWT |
| POST | `/api/auth/token/refresh/` | public | Renouvelle le jeton d'accès |
| GET | `/api/auth/me/` | connecté | Profil de l'utilisateur |
| DELETE | `/api/auth/me/` | connecté | Supprime le compte, mot de passe exigé |
| GET | `/api/matches/` | public | Liste des matchs, filtrable par date et sport |
| GET | `/api/matches/livescores/` | public | Scores en direct |
| POST | `/api/matches/synchroniser/` | administrateur | Synchro depuis TheSportsDB |
| POST | `/api/suggestions/` | public | Recettes et bières suggérées pour un match |
| GET | `/api/recipes/` | public | Catalogue des recettes |
| GET | `/api/beers/` | public | Catalogue des bières |
| GET/POST | `/api/favorites/` | connecté | Favoris — match, recette ou bière |
| DELETE | `/api/favorites/{id}/` | connecté | Retire un favori |
| GET | `/api/comments/` | public | Commentaires, filtrables par cible |
| POST | `/api/comments/` | connecté | Dépose un commentaire |
| GET | `/api/ratings/` | public | Notes, filtrables par cible |
| POST | `/api/ratings/` | connecté | Note de 1 à 5, une seule par cible |

## Structure

```
backend/
├── apps/
│   ├── cible.py        # Socle des références : match, recette ou bière
│   ├── references.py   # Traduction (type, reference_id) ↔ clé étrangère
│   ├── matches/        # Modèle Match, intégration TheSportsDB, synchro
│   ├── recipes/        # Modèle Recipe, commandes de chargement
│   ├── beers/          # Modèle Beer
│   ├── suggestions/    # Moteur : équipe → région → pays, sans stockage
│   ├── users/          # Utilisateur sur mesure, authentification JWT
│   ├── favorites/      # Association porteuse (date d'ajout)
│   ├── comments/       # Entité : plusieurs commentaires par cible
│   └── ratings/        # Association porteuse (note de 1 à 5)
└── config/             # settings, urls, wsgi

frontend/src/app/
├── core/               # Modèles, services, intercepteur JWT, guards
├── features/           # landing, matches, recipes, favorites, auth,
│                       #   settings, legal, partners
└── shared/             # Menu compte, tab-bar, footer, squelettes
```
