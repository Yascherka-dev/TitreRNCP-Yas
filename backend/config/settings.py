from pathlib import Path
from datetime import timedelta
import os
import sys
from dotenv import load_dotenv

load_dotenv()

BASE_DIR = Path(__file__).resolve().parent.parent

# True uniquement pendant l'exécution des tests, sert à neutraliser le throttling.
TESTING = 'test' in sys.argv

# Obligatoire : aucune valeur en dur. Lève une KeyError au démarrage si absente.
SECRET_KEY = os.environ['SECRET_KEY']

DEBUG = os.getenv('DEBUG', 'False') == 'True'

# Liste séparée par des virgules, à renseigner avec le domaine de prod une fois DEBUG=False.
ALLOWED_HOSTS = [
    h.strip() for h in os.getenv('ALLOWED_HOSTS', 'localhost,127.0.0.1').split(',')
    if h.strip()
]


# Applications

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    # Third-party
    'rest_framework',
    'rest_framework_simplejwt',
    'corsheaders',
    # Apps métier
    'apps.users',
    'apps.matches',
    'apps.recipes',
    'apps.suggestions',
    'apps.favorites',
    'apps.comments',
    'apps.ratings',
    'apps.beers',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'config.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'config.wsgi.application'


# Base de données — Railway en prod (DATABASE_URL), variables séparées en local

import dj_database_url

_DATABASE_URL = os.getenv('DATABASE_URL')
if _DATABASE_URL:
    DATABASES = {'default': dj_database_url.config(default=_DATABASE_URL, conn_max_age=600)}
else:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.postgresql',
            'NAME': os.getenv('DB_NAME', 'matchmuunch'),
            'USER': os.getenv('DB_USER', 'postgres'),
            'PASSWORD': os.getenv('DB_PASSWORD', ''),
            'HOST': os.getenv('DB_HOST', 'localhost'),
            'PORT': os.getenv('DB_PORT', '5432'),
        }
    }


# Modèle utilisateur custom

AUTH_USER_MODEL = 'users.User'


# Django REST Framework

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'config.authentication.SoftJWTAuthentication',
    ),
    'DEFAULT_PERMISSION_CLASSES': (
        'rest_framework.permissions.IsAuthenticatedOrReadOnly',
    ),
    'DEFAULT_THROTTLE_CLASSES': (
        'rest_framework.throttling.AnonRateThrottle',
        'rest_framework.throttling.UserRateThrottle',
    ),
    # Rates neutralisés en test (None) pour éviter les 429 sur 127.0.0.1.
    'DEFAULT_THROTTLE_RATES': {
        'anon':  None if TESTING else '60/min',
        'user':  None if TESTING else '120/min',
        'login': None if TESTING else '5/min',
    },
}


# JWT — SimpleJWT

SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(hours=1),
    'REFRESH_TOKEN_LIFETIME': timedelta(days=7),
    'AUTH_HEADER_TYPES': ('Bearer',),
}


# CORS — localhost:4200 en dev, domaine Vercel en prod (via l'env, séparés par virgules)

CORS_ALLOWED_ORIGINS = [
    o.strip().rstrip('/') for o in os.getenv('CORS_ALLOWED_ORIGINS', 'http://localhost:4200').split(',')
    if o.strip()
]


# Durcissement HTTPS — actif uniquement hors DEBUG, pour ne pas casser le dev local.

if not DEBUG:
    # Railway termine le TLS en amont : sans cet en-tête, Django croit recevoir du
    # HTTP et SECURE_SSL_REDIRECT provoque une boucle de redirection infinie.
    SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
    SECURE_SSL_REDIRECT = True

    SESSION_COOKIE_SECURE = True
    CSRF_COOKIE_SECURE = True

    # 1 an. Ne pas activer includeSubDomains/preload sans maîtriser tous les sous-domaines.
    SECURE_HSTS_SECONDS = 31536000


# Validation des mots de passe

AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]


# Internationalisation

LANGUAGE_CODE = 'fr-fr'
TIME_ZONE = 'Europe/Paris'
USE_I18N = True
USE_TZ = True


# Fichiers statiques — servis par WhiteNoise en prod

STATIC_URL = 'static/'
STATIC_ROOT = BASE_DIR / 'staticfiles'

STORAGES = {
    'default': {
        'BACKEND': 'django.core.files.storage.FileSystemStorage',
    },
    'staticfiles': {
        'BACKEND': 'whitenoise.storage.CompressedManifestStaticFilesStorage',
    },
}

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'


# Clés API externes (lues depuis .env)

SPORTSDB_KEY = os.getenv('SPORTSDB_KEY', '')


# ── Journalisation ───────────────────────────────────────────────────────────
# Sans elle, une panne de TheSportsDB passait inaperçue : la synchronisation
# renvoyait zéro match et les tâches planifiées affichaient un compte à zéro
# sans jamais dire pourquoi.
#
# Tout part sur la sortie standard : Railway la collecte, il n'y a pas de
# fichier à faire tourner ni de volume à prévoir.

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'simple': {
            'format': '{levelname} {asctime} {name} — {message}',
            'style': '{',
        },
    },
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
            'formatter': 'simple',
        },
    },
    'root': {
        'handlers': ['console'],
        # En développement, DEBUG noierait la console sous les requêtes SQL.
        'level': 'INFO',
    },
    'loggers': {
        # Le code du projet : c'est ici qu'on veut voir les échecs d'intégration.
        'apps': {
            'handlers': ['console'],
            'level': 'INFO',
            'propagate': False,
        },
        # Les erreurs serveur non rattrapées, avec leur trace.
        'django.request': {
            'handlers': ['console'],
            'level': 'ERROR',
            'propagate': False,
        },
    },
}
