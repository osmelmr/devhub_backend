from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from .models import Product
from .serializers import ProductSerializer
from .permissions import user_can_mutate
from .services import filter_products, search_products
from .pagination import ProductPagination
from django.shortcuts import get_object_or_404
from django.db.models import Q

# Create your views here.

@api_view(["GET"])
@permission_classes([IsAuthenticated])
def list_products(request):
    user = request.user

    if user.role == "admin":
        products = Product.objects.all()
    else:
        products = Product.objects.filter(Q(owner=user) | Q(owner__role="admin"))

    products = filter_products(products, request.query_params)
    products = search_products(products, request.query_params)

    paginate = request.query_params.get("paginate", "true").lower()
    if paginate == "false":
        serializer = ProductSerializer(products, many=True)
        return Response(serializer.data)

    paginator = ProductPagination()
    paginatedProducts = paginator.paginate_queryset(products, request)
    serializer = ProductSerializer(paginatedProducts, many=True)
    return paginator.get_paginated_response(serializer.data)


@api_view(["POST"])
@permission_classes([IsAuthenticated])
def create_product(request):
    serializer = ProductSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save(owner=request.user)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(["GET"])
@permission_classes([IsAuthenticated])
def retrieve_product(request, pk):
    product = get_object_or_404(Product,pk=pk)
    

    if (
        request.user.role == "admin"
        or product.owner == request.user
        or product.owner.role == "admin"
    ):
        serializer = ProductSerializer(product)
        return Response(serializer.data)

    return Response({"error": "No tienes permiso para ver este producto"}, status=status.HTTP_403_FORBIDDEN)

@api_view(["PUT", "PATCH"])
@permission_classes([IsAuthenticated])
def update_product(request, pk):
    product = get_object_or_404(Product,pk=pk)

    if not user_can_mutate(request, product):
        return Response({"error": "No tienes permiso para modificar este producto"}, status=status.HTTP_403_FORBIDDEN)

    serializer = ProductSerializer(product, data=request.data, partial=(request.method == "PATCH"))

    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)

    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(["DELETE"])
@permission_classes([IsAuthenticated])
def delete_product(request, pk):
    product = get_object_or_404(Product,pk=pk)
    if not user_can_mutate(request, product):
        return Response({"error": "No tienes permiso para eliminar este producto"}, status=status.HTTP_403_FORBIDDEN)

    product.delete()
    return Response(status=status.HTTP_204_NO_CONTENT)


@api_view(["DELETE"])
@permission_classes([IsAuthenticated])
def delete_products(request):
    ids = request.data.get("ids")

    if not ids or not isinstance(ids, list):
        return Response(
            {"error": "Debes enviar una lista de IDs en 'ids'."},
            status=status.HTTP_400_BAD_REQUEST
        )

    user = request.user

    # 1. Obtiene productos con esos IDs
    products = Product.objects.filter(id__in=ids)

    if not products.exists():
        return Response(
            {"error": "No se encontraron productos con esos IDs."},
            status=status.HTTP_404_NOT_FOUND
        )

    # 2. Verifica permisos producto por producto
    unauthorized = []
    authorized = []

    for product in products:
        if user_can_mutate(request, product):
            authorized.append(product)
        else:
            unauthorized.append(product.id)

    # 3. Borra solo los autorizados
    deleted_count = 0
    if authorized:
        deleted_count = len(authorized)
        for p in authorized:
            p.delete()

    # 4. Respuesta
    return Response(
        {
            "deleted": deleted_count,
            "not_deleted_ids": unauthorized,
        },
        status=status.HTTP_200_OK
    )


