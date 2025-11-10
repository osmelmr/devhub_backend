import os

_env = os.getenv("DJANGO_ENV", "dev").lower()

if _env == "prod":
    from .prod import *
else:
    from .dev import *