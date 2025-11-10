from .base import *

# Forzar modo desarrollo
DEBUG = True
ALLOWED_HOSTS = ["127.0.0.1", "localhost"]

# Base de datos local por defecto
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "db.sqlite3",
    }
}

# Opcional: apps o middleware de desarrollo
INSTALLED_APPS += [
    # "debug_toolbar",
]
MIDDLEWARE += [
    # "debug_toolbar.middleware.DebugToolbarMiddleware",
]
