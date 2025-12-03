from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from .models import Category
from .serializers import CategorySerializer
from .permissions import user_can_mutate
from .services import search_categories
from .pagination import CategoryPagination
from django.shortcuts import get_object_or_404
from django.db.models import Q

# Create your views here.

@api_view(["GET"])
# @permission_classes([IsAuthenticated])
def list_categories(request):
    user = request.user

    if user.role == "admin":
        categories = Category.objects.all()
    else:
        categories = Category.objects.filter(Q(owner=user) | Q(owner__role="admin"))

    categories = search_categories(categories, request.query_params)

    paginate = request.query_params.get("paginate", "true").lower()
    if paginate == "false":
        serializer = CategorySerializer(categories, many=True)
        return Response(serializer.data)

    paginator = CategoryPagination()
    paginatedCategorys = paginator.paginate_queryset(categories, request)
    serializer = CategorySerializer(paginatedCategorys, many=True)
    return paginator.get_paginated_response(serializer.data)


@api_view(["POST"])
@permission_classes([IsAuthenticated])
def create_category(request):
    serializer = CategorySerializer(data=request.data)
    if serializer.is_valid():
        serializer.save(owner=request.user)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(["GET"])
@permission_classes([IsAuthenticated])
def retrieve_category(request, pk):
    category = get_object_or_404(Category,pk=pk)
    

    if (
        request.user.role == "admin"
        or category.owner == request.user
        or category.owner.role == "admin"
    ):
        serializer = CategorySerializer(category)
        return Response(serializer.data)

    return Response({"error": "No tienes permiso para ver este categoryo"}, status=status.HTTP_403_FORBIDDEN)

@api_view(["PUT", "PATCH"])
@permission_classes([IsAuthenticated])
def update_category(request, pk):
    category = get_object_or_404(Category,pk=pk)

    if not user_can_mutate(request, category):
        return Response({"error": "No tienes permiso para modificar este categoryo"}, status=status.HTTP_403_FORBIDDEN)

    serializer = CategorySerializer(category, data=request.data, partial=(request.method == "PATCH"))

    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)

    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(["DELETE"])
@permission_classes([IsAuthenticated])
def delete_category(request, pk):
    category = get_object_or_404(Category,pk=pk)
    if not user_can_mutate(request, category):
        return Response({"error": "No tienes permiso para eliminar este categoryo"}, status=status.HTTP_403_FORBIDDEN)

    category.delete()
    return Response(status=status.HTTP_204_NO_CONTENT)


@api_view(["DELETE"])
@permission_classes([IsAuthenticated])
def delete_categories(request):
    ids = request.data.get("ids")

    if not ids or not isinstance(ids, list):
        return Response(
            {"error": "Debes enviar una lista de IDs en 'ids'."},
            status=status.HTTP_400_BAD_REQUEST
        )

    user = request.user

    # 1. Obtiene categorías con esos IDs
    categories = Category.objects.filter(id__in=ids)

    if not categories.exists():
        return Response(
            {"error": "No se encontraron categorías con esos IDs."},
            status=status.HTTP_404_NOT_FOUND
        )

    # 2. Verifica permisos categoría por categoría
    unauthorized = []
    authorized = []

    for category in categories:
        if user_can_mutate(request, category):
            authorized.append(category)
        else:
            unauthorized.append(category.id)

    # 3. Borra solo las autorizadas
    deleted_count = 0
    if authorized:
        deleted_count = len(authorized)
        for c in authorized:
            c.delete()

    # 4. Respuesta
    return Response(
        {
            "deleted": deleted_count,
            "not_deleted_ids": unauthorized,
        },
        status=status.HTTP_200_OK
    )
