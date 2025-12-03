# scripts/add_products.py

import os
import django
import uuid

# Inicializar Django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "devhub.settings")
django.setup()

from apps.users.models import User
from apps.pocket_store.categories.models import Category
from apps.pocket_store.products.models import Product

# --- Catálogo estilo Amazon ---
productos = [
    # ------------------ ADMIN PRODUCTS ------------------
    {
        "id": uuid.UUID("20000000-0000-0000-0000-000000000001"),
        "owner_email": "admin@example.com",
        "category_name": "Desarrollo Web",
        "name": "Laptop ASUS VivoBook 15",
        "description": "Intel Core i5, 16GB RAM, SSD 512GB. Equipo equilibrado para desarrollo web.",
        "price": 659.99,
        "discount": 5,
        "stock": 20,
        "rating": 4.4,
        "image": "https://placehold.co/600x400/asus-vivobook.png"
    },
    {
        "id": uuid.UUID("20000000-0000-0000-0000-000000000002"),
        "owner_email": "admin@example.com",
        "category_name": "Desarrollo Web",
        "name": "Monitor LG UltraWide 29''",
        "description": "Pantalla panorámica ideal para abrir el editor y la documentación al mismo tiempo.",
        "price": 279.99,
        "discount": 0,
        "stock": 15,
        "rating": 4.6,
        "image": "https://placehold.co/600x400/lg-ultrawide.png"
    },
    {
        "id": uuid.UUID("20000000-0000-0000-0000-000000000003"),
        "owner_email": "admin@example.com",
        "category_name": "Bases de Datos",
        "name": "Libro 'PostgreSQL 16 Mastery'",
        "description": "Guía avanzada para administradores, desarrolladores y analistas de datos.",
        "price": 39.99,
        "discount": 10,
        "stock": 30,
        "rating": 4.8,
        "image": "https://placehold.co/600x400/postgres-book.png"
    },

    # ------------------ VIEWER 1 PRODUCTS ------------------
    {
        "id": uuid.UUID("20000000-0000-0000-0000-000000000004"),
        "owner_email": "viewer1@example.com",
        "category_name": "Diseño UI/UX",
        "name": "Tableta Gráfica Wacom One",
        "description": "Ideal para diseñadores que buscan precisión y un trazo natural.",
        "price": 269.99,
        "discount": 15,
        "stock": 40,
        "rating": 4.5,
        "image": "https://placehold.co/600x400/wacom-one.png"
    },
    {
        "id": uuid.UUID("20000000-0000-0000-0000-000000000005"),
        "owner_email": "viewer1@example.com",
        "category_name": "Diseño UI/UX",
        "name": "Teclado Mecánico Keychron K2",
        "description": "Interruptores Brown, compacto, Bluetooth. Perfecto para diseñadores y devs.",
        "price": 89.99,
        "discount": 5,
        "stock": 50,
        "rating": 4.7,
        "image": "https://placehold.co/600x400/keychron-k2.png"
    },
    {
        "id": uuid.UUID("20000000-0000-0000-0000-000000000006"),
        "owner_email": "viewer1@example.com",
        "category_name": "Desarrollo Web",
        "name": "Micrófono HyperX QuadCast",
        "description": "Micrófono profesional ideal para grabar cursos o transmisiones en vivo.",
        "price": 119.99,
        "discount": 0,
        "stock": 25,
        "rating": 4.8,
        "image": "https://placehold.co/600x400/hyperx-quadcast.png"
    },

    # ------------------ VIEWER 2 PRODUCTS ------------------
    {
        "id": uuid.UUID("20000000-0000-0000-0000-000000000007"),
        "owner_email": "viewer2@example.com",
        "category_name": "Bases de Datos",
        "name": "NAS Synology DS220+",
        "description": "Servidor NAS perfecto para copias de seguridad, multimedia y hosting personal.",
        "price": 319.99,
        "discount": 10,
        "stock": 10,
        "rating": 4.9,
        "image": "https://placehold.co/600x400/synology-nas.png"
    },
    {
        "id": uuid.UUID("20000000-0000-0000-0000-000000000008"),
        "owner_email": "viewer2@example.com",
        "category_name": "Desarrollo Web",
        "name": "SSD Samsung NVMe 1TB",
        "description": "Velocidad brutal para proyectos pesados y entornos de desarrollo.",
        "price": 129.99,
        "discount": 20,
        "stock": 35,
        "rating": 4.9,
        "image": "https://placehold.co/600x400/nvme-ssd.png"
    },
    {
        "id": uuid.UUID("20000000-0000-0000-0000-000000000009"),
        "owner_email": "viewer2@example.com",
        "category_name": "Diseño UI/UX",
        "name": "Mouse Logitech MX Master 3S",
        "description": "Ergonómico, silencioso y preciso. El favorito de diseñadores y programadores.",
        "price": 109.99,
        "discount": 5,
        "stock": 60,
        "rating": 4.9,
        "image": "https://placehold.co/600x400/mx-master.png"
    },

    # ----------- EXTRA PRODUCTS (Cualquier usuario) -----------
    {
        "id": uuid.UUID("20000000-0000-0000-0000-000000000010"),
        "owner_email": "admin@example.com",
        "category_name": "Bases de Datos",
        "name": "Libro 'MongoDB from Zero to Hero'",
        "description": "Un camino práctico hacia las bases de datos NoSQL.",
        "price": 24.99,
        "discount": 0,
        "stock": 70,
        "rating": 4.3,
        "image": "https://placehold.co/600x400/mongodb-book.png"
    },
    {
        "id": uuid.UUID("20000000-0000-0000-0000-000000000011"),
        "owner_email": "viewer1@example.com",
        "category_name": "Diseño UI/UX",
        "name": "Samsung Smartwatch Galaxy Watch 5",
        "description": "Pantalla AMOLED brillante, medición de salud, batería de larga duración.",
        "price": 239.99,
        "discount": 10,
        "stock": 18,
        "rating": 4.6,
        "image": "https://placehold.co/600x400/galaxy-watch.png"
    },
    {
        "id": uuid.UUID("20000000-0000-0000-0000-000000000012"),
        "owner_email": "viewer2@example.com",
        "category_name": "Desarrollo Web",
        "name": "Auriculares Sony WH-1000XM4",
        "description": "Cancelación de ruido legendaria. Perfectos para estudiar o programar.",
        "price": 349.99,
        "discount": 15,
        "stock": 22,
        "rating": 4.9,
        "image": "https://placehold.co/600x400/sony-xm4.png"
    },
]

# --- Crear productos ---
for p in productos:
    try:
        owner = User.objects.get(email=p["owner_email"])
    except User.DoesNotExist:
        print(f"❌ Usuario no existe → {p['owner_email']}")
        continue

    try:
        category = Category.objects.get(name=p["category_name"])
    except Category.DoesNotExist:
        print(f"❌ Categoría no existe → {p['category_name']}")
        continue

    if Product.objects.filter(id=p["id"]).exists():
        print(f"⚠️ Producto ya existe → {p['name']}")
        continue

    product = Product(
        id=p["id"],
        owner=owner,
        category=category,
        name=p["name"],
        description=p["description"],
        price=p["price"],
        discount=p["discount"],
        stock=p["stock"],
        rating=p["rating"],
        image=p["image"],
    )

    product.save()
    print(f"✅ Producto creado → {product.name} ({product.id})")
