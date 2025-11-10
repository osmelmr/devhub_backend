"""
Django settings para devhub, combinado y funcional.
Usa django-environ para manejar variables de entorno.
"""

from pathlib import Path
from datetime import timedelta
import os
import environ

# -------------------------------
# Ruta base del proyecto
# -------------------------------
BASE_DIR = Path(__file__).resolve().parent.parent.parent

# -------------------------------
# Inicializar django-environ
# -------------------------------
env = environ.Env(
    DEBUG=(bool, False),  # Valor por defecto False si no está en .env
)

# Cargar .env si existe
env_file = BASE_DIR / ".env"
if env_file.exists():
    environ.Env.read_env(str(env_file))

# -------------------------------
# Variables básicas
# -------------------------------

SECRET_KEY = env("SECRET_KEY")
DEBUG = env("DEBUG")

# ALLOWED_HOSTS: usar env.list para obtener lista segura
ALLOWED_HOSTS = env.list("ALLOWED_HOSTS", default=[])

# -------------------------------
# Aplicaciones instaladas
# -------------------------------
INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    # apps de terceros
    "rest_framework",
    "rest_framework_simplejwt",
    "corsheaders",
    # apps locales
    "apps.users",
    "apps.projects",
]

# -------------------------------
# Middleware
# -------------------------------
MIDDLEWARE = [
    "corsheaders.middleware.CorsMiddleware",
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "devhub.urls"
AUTH_USER_MODEL = "users.User"  # antes estaba "users.User", cambiado por convención de apps

# -------------------------------
# Templates
# -------------------------------
TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION = "devhub.wsgi.application"

# -------------------------------
# Base de datos
# -------------------------------

# Antes estaba hardcodeada SQLite:
# DATABASES = {
#     "default": {
#         "ENGINE": "django.db.backends.sqlite3",
#         "NAME": BASE_DIR / "db.sqlite3",
#     }
# }
# <- eliminado porque ahora usamos django-environ para mayor flexibilidad

DATABASES = {
    "default": env.db(default=f"sqlite:///{BASE_DIR / 'db.sqlite3'}")
}
# Esto permite cambiar a PostgreSQL u otro motor solo cambiando DATABASE_URL en el .env

# -------------------------------
# Validación de contraseñas
# -------------------------------
AUTH_PASSWORD_VALIDATORS = [
    {"NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator"},
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator"},
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator"},
    {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator"},
]

# -------------------------------
# Internacionalización
# -------------------------------
LANGUAGE_CODE = "en-us"
TIME_ZONE = "UTC"
USE_I18N = True
USE_TZ = True

# -------------------------------
# Archivos estáticos
# -------------------------------
STATIC_URL = "static/"

# -------------------------------
# DRF + JWT
# -------------------------------
REST_FRAMEWORK = {
    "DEFAULT_AUTHENTICATION_CLASSES": (
        "rest_framework_simplejwt.authentication.JWTAuthentication",
    ),
}

ACCESS_MINUTES = env.int("ACCESS_TOKEN_LIFETIME_MINUTES", default=60)
REFRESH_DAYS = env.int("REFRESH_TOKEN_LIFETIME_DAYS", default=1)

SIMPLE_JWT = {
    "ACCESS_TOKEN_LIFETIME": timedelta(minutes=ACCESS_MINUTES),
    "REFRESH_TOKEN_LIFETIME": timedelta(days=REFRESH_DAYS),
    "AUTH_HEADER_TYPES": ("Bearer",),
}

# -------------------------------
# CORS
# -------------------------------
# Antes estaba hardcodeado True
# CORS_ALLOW_ALL_ORIGINS = True  # <- eliminado
CORS_ALLOW_ALL_ORIGINS = env.bool("CORS_ALLOW_ALL_ORIGINS", default=True)

# -------------------------------
# Campo por defecto para modelos
# -------------------------------
DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"
