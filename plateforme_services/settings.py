from pathlib import Path
import os
import dj_database_url  # Assurez-vous que c'est importé (déjà dans votre code)

BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = os.environ.get('SECRET_KEY', 'django-insecure-votre-cle-secrete-changez-ca-en-prod')  # Changez en prod

# DEBUG : True temporaire pour voir erreurs détaillées (remettez False en prod finale)
DEBUG = os.environ.get('DJANGO_DEBUG', 'True') == 'True'  # Changez 'True' en 'False' pour prod par défaut

# ALLOWED_HOSTS : Gardez seulement cette ligne (inclut Render pour fixer 400)
ALLOWED_HOSTS = ['localhost', '127.0.0.1', 'plateforme-services.onrender.com']

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework',
    'corsheaders',
    'service',
    # 'whitenoise.runserver_nostatic',  # Retiré : Seulement pour dev runserver ; middleware suffit en prod
]

MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',  # Pour statiques en prod (Render)
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'service.middleware.DebugCookiesMiddleware',  # Votre middleware custom (si existant)
]

ROOT_URLCONF = 'plateforme_services.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'service/templates')],  # Trouve appli.html
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'plateforme_services.wsgi.application'

DATABASES = {
    'default': dj_database_url.config(
        default='sqlite:///db.sqlite3',  # Fallback SQLite local
        conn_max_age=600
    )
}

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

LANGUAGE_CODE = 'fr-fr'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# Static Files
STATIC_URL = 'static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'service/static'),  # Statiques dans service/static si besoin
]

# WhiteNoise Storage pour prod (compression + cache)
STORAGES = {
    "staticfiles": {
        "BACKEND": "whitenoise.storage.CompressedManifestStaticFilesStorage",
    },
}

# CORS : Ajout https:// pour Render
CORS_ALLOW_ALL_ORIGINS = False  # Sécurisé
CORS_ALLOW_CREDENTIALS = True
CORS_EXPOSE_HEADERS = ['Content-Type', 'X-CSRFToken']
CORS_ALLOWED_ORIGINS = [
    'http://localhost:8000',
    'http://127.0.0.1:8000',
    'https://plateforme-services.onrender.com',  # Fix : Ajout https:// pour HTTPS Render
]

# CSRF : Ajout https:// pour Render (essentiel pour cookies en prod)
CSRF_TRUSTED_ORIGINS = [
    'http://localhost:8000',
    'http://127.0.0.1:8000',
    'https://plateforme-services.onrender.com',  # Fix : Ajout https://
]

# Sessions
SESSION_COOKIE_NAME = 'sessionid'
SESSION_COOKIE_AGE = 1209600  # 2 semaines
SESSION_SAVE_EVERY_REQUEST = True
SESSION_COOKIE_SAMESITE = 'Lax'
SESSION_COOKIE_SECURE = os.environ.get('SESSION_COOKIE_SECURE', 'False') == 'True'  # True sur Render HTTPS
SESSION_COOKIE_HTTPONLY = True
SESSION_COOKIE_DOMAIN = None

# CSRF (Clé pour votre JS React)
CSRF_COOKIE_NAME = 'csrftoken'
CSRF_COOKIE_SAMESITE = 'Lax'
CSRF_COOKIE_SECURE = os.environ.get('CSRF_COOKIE_SECURE', 'False') == 'True'  # True sur Render
CSRF_COOKIE_HTTPONLY = False  # Essentiel : False pour accès JS (getCSRFTokenFromCookie)
CSRF_USE_SESSIONS = False
CSRF_FAILURE_VIEW = 'django.views.csrf.csrf_failure'

# REST Framework
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework.authentication.SessionAuthentication',
        'rest_framework.authentication.BasicAuthentication',  # Optionnel pour tests
    ],
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.IsAuthenticatedOrReadOnly',
    ],
}

# Autres (optionnel pour prod)
SECURE_SSL_REDIRECT = False  # False local ; True sur Render si besoin de force HTTPS
SECURE_HSTS_SECONDS = 0  # Activez en prod si HSTS
