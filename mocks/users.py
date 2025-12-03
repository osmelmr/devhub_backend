# scripts/add_users.py
# python -m mocks.users

import os
import django
import uuid

# Configuración de Django para usar este script fuera del manage.py
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "devhub.settings")
django.setup()

from apps.users.models import User  # Ajusta según la ruta de tu app

# Lista de usuarios a crear
usuarios = [
    {
        "id": uuid.UUID("11111111-1111-1111-1111-111111111111"),
        "email": "admin@example.com",
        "username": "AdminUser",
        "password": "Admin1234!",
        "role": "admin",
        "avatar_url": "",
        "avatar_public_id": ""
    },
    {
        "id": uuid.UUID("22222222-2222-2222-2222-222222222222"),
        "email": "viewer1@example.com",
        "username": "ViewerOne",
        "password": "Viewer123!",
        "role": "viewer",
        "avatar_url": "",
        "avatar_public_id": ""
    },
    {
        "id": uuid.UUID("33333333-3333-3333-3333-333333333333"),
        "email": "viewer2@example.com",
        "username": "ViewerTwo",
        "password": "Viewer123!",
        "role": "viewer",
        "avatar_url": "",
        "avatar_public_id": ""
    },
]

for u in usuarios:
    if not User.objects.filter(email=u["email"]).exists():
        user = User(
            id=u["id"],
            email=u["email"],
            username=u["username"],
            role=u["role"],
            avatar_url=u["avatar_url"],
            avatar_public_id=u["avatar_public_id"]
        )
        user.set_password(u["password"])
        user.save()
        print(f"Usuario creado: {user.username} ({user.id})")
    else:
        print(f"Usuario ya existe: {u['email']}")
