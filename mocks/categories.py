# python -m mocks.categories 
# scripts/add_categories.py

import os
import django
import uuid

# Configuración de Django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "devhub.settings")
django.setup()

from apps.users.models import User
from apps.pocket_store.categories.models import Category  # Ajusta según la ruta de tu app

# Lista de categorías a crear
categorias = [
    {
        "id": uuid.UUID("aaaaaaaa-aaaa-aaaa-aaaa-aaaaaaaaaaaa"),
        "owner_email": "admin@example.com",
        "name": "Desarrollo Web"
    },
    {
        "id": uuid.UUID("bbbbbbbb-bbbb-bbbb-bbbb-bbbbbbbbbbbb"),
        "owner_email": "viewer1@example.com",
        "name": "Diseño UI/UX"
    },
    {
        "id": uuid.UUID("cccccccc-cccc-cccc-cccc-cccccccccccc"),
        "owner_email": "viewer2@example.com",
        "name": "Bases de Datos"
    },
]

for c in categorias:
    try:
        owner = User.objects.get(email=c["owner_email"])
    except User.DoesNotExist:
        print(f"No se encontró usuario con email {c['owner_email']}")
        continue

    if not Category.objects.filter(name=c["name"]).exists():
        category = Category(
            id=c["id"],
            owner=owner,
            name=c["name"]
        )
        category.save()
        print(f"Categoría creada: {category.name} ({category.id})")
    else:
        print(f"La categoría ya existe: {c['name']}")
