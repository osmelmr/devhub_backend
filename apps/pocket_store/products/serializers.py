from rest_framework import serializers
from .models import Product

class ProductSerializer(serializers.ModelSerializer):
    final_price = serializers.ReadOnlyField()
    owner = serializers.ReadOnlyField(source="owner.id")

    class Meta:
        model = Product
        fields = [
            "id",
            "owner",
            "name",
            "slug",
            "description",
            "category",
            "category_name",
            "price",
            "discount",
            "final_price",
            "stock",
            "rating",
            "status",
            "image",
            "created_at",
            "updated_at",
        ]
        read_only_fields = ["slug", "category_name", "created_at", "updated_at"]

    # --- Validaciones que tú NO querías eliminar ---
    def validate_discount(self, value):
        """Evita descuentos fuera de 0–100."""
        if not (0 <= value <= 100):
            raise serializers.ValidationError("El descuento debe estar entre 0 y 100.")
        return value

    def validate_price(self, value):
        if value < 0:
            raise serializers.ValidationError("El precio no puede ser negativo.")
        return value
