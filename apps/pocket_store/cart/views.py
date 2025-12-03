from .models import Cart, CartItem
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from ..products.models import Product
from rest_framework.response import Response
from .serializers import CartSerializer

# Create your views here.
# carts/views.py
def get_or_create_cart(user):
    cart, created = Cart.objects.get_or_create(user=user)
    return cart

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def add_to_cart(request):
    user = request.user
    cart = get_or_create_cart(user)

    product_id = request.data.get("product_id")
    quantity = int(request.data.get("quantity", 1))

    # Verificar que el producto existe
    try:
        product = Product.objects.get(id=product_id)
    except Product.DoesNotExist:
        return Response({"error": "Producto no encontrado"}, status=404)

    # Buscar si ya existe el item
    item, created = CartItem.objects.get_or_create(
        cart=cart,
        product=product,
        defaults={'quantity': quantity}
    )

    if not created:
        item.quantity += quantity
        item.save()

    return Response(CartSerializer(cart).data, status=200)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def increase_quantity(request):
    user = request.user
    cart = get_or_create_cart(user)

    item_id = request.data.get("item_id")

    try:
        item = CartItem.objects.get(id=item_id, cart=cart)
    except CartItem.DoesNotExist:
        return Response({"error": "Item no encontrado en tu carrito"}, status=404)

    item.quantity += 1
    item.save()

    return Response(CartSerializer(cart).data)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def decrease_quantity(request):
    user = request.user
    cart = get_or_create_cart(user)

    item_id = request.data.get("item_id")

    try:
        item = CartItem.objects.get(id=item_id, cart=cart)
    except CartItem.DoesNotExist:
        return Response({"error": "Item no encontrado en tu carrito"}, status=404)

    if item.quantity > 1:
        item.quantity -= 1
        item.save()
    else:
        item.delete()  # Se va como hoja llevada por el viento

    return Response(CartSerializer(cart).data)

@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def remove_from_cart(request):
    user = request.user
    cart = get_or_create_cart(user)

    item_id = request.data.get("item_id")

    try:
        item = CartItem.objects.get(id=item_id, cart=cart)
    except CartItem.DoesNotExist:
        return Response({"error": "Item no encontrado"}, status=404)

    item.delete()

    return Response(CartSerializer(cart).data)

@api_view(['GET'])
# @permission_classes([IsAuthenticated])
def get_cart(request):
    user = request.user
    cart = get_or_create_cart(user)
    return Response(CartSerializer(cart).data)
