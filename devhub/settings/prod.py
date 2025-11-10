from .base import *
import os
import environ

env = environ.Env()
# cargar .env.prod (usar str para compatibilidad)
environ.Env.read_env(str(BASE_DIR / ".env.prod"))

# Siempre False en producción
DEBUG = False

# Hosts de producción (usar env.list)
ALLOWED_HOSTS = env.list("ALLOWED_HOSTS", default=[])

# Base de datos desde DATABASE_URL
DATABASES = {
    "default": env.db()
}

# Seguridad en producción
CSRF_COOKIE_SECURE = True
SESSION_COOKIE_SECURE = True
SECURE_BROWSER_XSS_FILTER = True
SECURE_CONTENT_TYPE_NOSNIFF = True

# Archivos estáticos
STATIC_ROOT = BASE_DIR / "staticfiles"
