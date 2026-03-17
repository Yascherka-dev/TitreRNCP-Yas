# Match & Munch

Plateforme web qui répond à : "On mange quoi devant le match de ce soir ?"
Pour chaque match sélectionné, deux recettes inspirées des pays des équipes qui s'affrontent.

## Stack

- **Frontend** — Angular 19 standalone + Angular Material + Figtree
- **Backend** — Django 6 + Django REST Framework
- **BDD** — PostgreSQL (Railway addon)
- **Auth** — JWT via djangorestframework-simplejwt
- **API Football** — football-data.org v4 (Ligue 1 + Champions League)

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

API_FOOTBALL_KEY=       # football-data.org
ANTHROPIC_API_KEY=      # Claude API (suggestions, optionnel en dev)
```

> PostgreSQL doit tourner en local avec une base `matchmuunch` créée au préalable (`createdb matchmuunch`).

## Endpoints principaux

| Méthode | Route | Description |
|---|---|---|
| POST | `/api/auth/register/` | Inscription |
| POST | `/api/auth/login/` | Connexion (retourne JWT) |
| GET | `/api/matches/` | Liste des matchs (filtrables par date) |
| POST | `/api/matches/synchroniser/` | Synchro depuis football-data.org |
| POST | `/api/suggestions/` | Recettes suggérées pour un match |
| GET/POST | `/api/favorites/` | Favoris (auth requise) |

## Structure

```
backend/
├── apps/
│   ├── matches/        # Modèle Match, synchro API football
│   ├── recipes/        # Modèle Recipe, commande load_recipes
│   ├── suggestions/    # Endpoint suggestions (→ Claude API)
│   ├── users/          # Auth custom
│   ├── favorites/
│   ├── comments/
│   └── ratings/
└── config/             # settings, urls, wsgi

frontend/src/app/
├── core/               # Models, services, intercepteurs, guards
├── features/           # landing, matches, auth, recipes
└── shared/             # Skeleton loaders
```
