# scripts/add_cart_items.py

import os
import django
import random

os.environ.setdefault("Django_SETTINGS_MODULE", "devhub.settings")
django.setup()

from apps.users.models import User
from apps.pocket_store.products.models import Product
from apps.pocket_store.cart.models import Cart, CartItem

# Cantidades posibles
quantities = [1, 1, 2, 3]

def get_cart(user):
    cart, created = Cart.objects.get_or_create(user=user)
    if created:
        print(f"🛒 Carrito creado → {user.email}")
    return cart


def add_item(cart, product, quantity):
    item, created = CartItem.objects.get_or_create(
        cart=cart,
        product=product,
        defaults={'quantity': quantity}
    )

    if not created:
        item.quantity += quantity
        item.save()
        print(f"🔄 Actualizado {product.name} → x{item.quantity}")
    else:
        print(f"➕ Añadido {product.name} → x{quantity}")


# ------------------------------------
# Configuración de productos por usuario
# ------------------------------------

productos_por_usuario = {
    "admin@example.com": [
        "Laptop ASUS VivoBook 15",
        "Micrófono HyperX QuadCast",
        "Libro 'PostgreSQL 16 Mastery'",
    ],
    "viewer1@example.com": [
        "Tableta Gráfica Wacom One",
        "Mouse Logitech MX Master 3S",
        "Teclado Mecánico Keychron K2",
    ],
    "viewer2@example.com": [
        "NAS Synology DS220+",
        "Auriculares Sony WH-1000XM4",
        "SSD Samsung NVMe 1TB",
    ],
}

# ------------------------------------
# PROCESAR TODO
# ------------------------------------

for user_email, product_names in productos_por_usuario.items():
    try:
        user = User.objects.get(email=user_email)
    except User.DoesNotExist:
        print(f"❌ Usuario no encontrado: {user_email}")
        continue

    cart = get_cart(user)

    for product_name in product_names:
        try:
            product = Product.objects.get(name=product_name)
        except Product.DoesNotExist:
            print(f"❌ Producto no existe: {product_name}")
            continue

        quantity = random.choice(quantities)
        add_item(cart, product, quantity)

print("\n✨ Carritos cargados exitosamente ✨")
