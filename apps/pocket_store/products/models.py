from django.db import models
from django.utils.text import slugify
from apps.pocket_store.categories.models import Category

class Product(models.Model):

    class Status(models.TextChoices):
        ACTIVE = "active", "Activo"
        INACTIVE = "inactive", "Inactivo"
        OUT_OF_STOCK = "out_of_stock", "Sin stock"

    # --- Información básica ---
    name = models.CharField(max_length=150)
    slug = models.SlugField(unique=True, blank=True)
    description = models.TextField(blank=True)

    # --- Categoría ---
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True)
    category_name = models.CharField(max_length=100, blank=True)

    # --- Precios ---
    price = models.DecimalField(max_digits=10, decimal_places=2)
    discount = models.DecimalField(
        max_digits=4,
        decimal_places=2,
        default=0,
        help_text="Porcentaje de descuento (0-100)"
    )

    # --- Stock ---
    stock = models.PositiveIntegerField(default=0)

    # --- Rating ---
    rating = models.DecimalField(
        max_digits=2,
        decimal_places=1,
        default=0,
        help_text="Valoración promedio (0-5)"
    )

    # --- Estado ---
    status = models.CharField(
        max_length=20,
        choices=Status.choices,
        default=Status.ACTIVE
    )

    # --- Imagen ---
    image = models.URLField(blank=True, null=True)

    # --- Fechas ---
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    # --- Métodos ---
    def save(self, *args, **kwargs):
        # Auto-generar slug si no existe
        if not self.slug:
            self.slug = slugify(self.name)

        # Copiar nombre de la categoría en texto plano
        if self.category:
            self.category_name = self.category.name

        super().save(*args, **kwargs)

    def __str__(self):
        return self.name

    @property
    def final_price(self):
        """Precio final con descuento aplicado."""
        if self.discount > 0:
            return self.price - (self.price * (self.discount / 100))
        return self.price



"""
----------------------------------------------
DESCRIPCIÓN DE CADA ATRIBUTO DEL MODELO PRODUCT
----------------------------------------------

name:
    Nombre del producto. Campo principal para identificarlo.
slug:
    Identificador textual único usado en URLs amigables. Se genera automáticamente.
description:
    Texto descriptivo del producto. Puede estar vacío.

category:
    Relación con el modelo Category. Permite clasificar productos.
category_name:
    Copia del nombre de la categoría. Útil para búsquedas rápidas sin joins.

price:
    Precio base del producto antes de descuentos.
discount:
    Porcentaje de descuento aplicado (0–100). Afecta el final_price.

stock:
    Cantidad disponible del producto. Se usa para mostrar si hay existencias.

rating:
    Promedio de valoración del producto (0–5). Útil para orden y filtros.

status:
    Estado del producto: activo, inactivo o sin stock. Controla su visibilidad.

image:
    URL de la imagen del producto. Ideal para usar con Cloudinary u otro CDN.

created_at:
    Fecha y hora en que el producto fue creado.
updated_at:
    Fecha y hora de la última modificación.

----------------------------------------------
DESCRIPCIÓN DE LOS MÉTODOS
----------------------------------------------

save():
    Sobrescribe el método de Django para:
        - Generar el slug automáticamente si no existe.
        - Copiar el nombre de la categoría a category_name.
    Luego guarda el producto normalmente.

__str__():
    Retorna el nombre del producto cuando se lo imprime o muestra.

final_price (property):
    Calcula el precio final aplicando el descuento.
    No se almacena en la base de datos; se genera al acceder.
"""
