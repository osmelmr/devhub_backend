from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework import status
from ..models import User
from ..serializers import UserSerializer
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAuthenticated
from devhub.permissions import IsAdminUser
from devhub.pagination import StandardResultsSetPagination

from devhub.utils import delete_image
from django.shortcuts import get_object_or_404




@api_view(['GET'])
def list_users(request):
    users = User.objects.all()
    paginator = StandardResultsSetPagination()
    paginated_users = paginator.paginate_queryset(users, request)
    serializer = UserSerializer(paginated_users, many=True)
    return paginator.get_paginated_response(serializer.data)

@api_view(['GET'])
@permission_classes([IsAuthenticatedOrReadOnly])
def retrieve_user(request, pk):
    try:
        user = User.objects.get(pk=pk)
    except User.DoesNotExist:
        return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)
    serializer = UserSerializer(user)
    return Response(serializer.data)

@api_view(['POST'])
@permission_classes([IsAuthenticated, IsAdminUser])
def create_user(request):
    serializer = UserSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



@api_view(['PUT', 'PATCH'])
@permission_classes([IsAuthenticatedOrReadOnly, IsAdminUser])
def update_user(request, pk):
    user = get_object_or_404(User, pk=pk)

    # Guardamos la URL actual antes de actualizar
    old_avatar_url = user.avatar_url
    old_avatar_public_id = user.avatar_public_id

    serializer = UserSerializer(user, data=request.data, partial=True)
    if serializer.is_valid():
        # Obtenemos la nueva URL que viene en el request (si existe)
        new_avatar_url = serializer.validated_data.get("avatar_url")
        new_avatar_public_id = serializer.validated_data.get("avatar_public_id")

        # Si hay avatar nuevo y es distinto al anterior, borramos el viejo en Cloudinary
        if new_avatar_url and old_avatar_url and new_avatar_url != old_avatar_url:
            if old_avatar_public_id:
                delete_image(old_avatar_public_id)

        # Guardamos cambios en el usuario
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)

    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['DELETE'])
@permission_classes([IsAuthenticatedOrReadOnly, IsAdminUser])
def delete_user(request, pk):
    try:
        user = User.objects.get(pk=pk)
    except User.DoesNotExist:
        return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)
    user.delete()
    return Response(status=status.HTTP_204_NO_CONTENT)

@api_view(['DELETE'])
@permission_classes([IsAuthenticatedOrReadOnly, IsAdminUser])
def delete_users(request):
    ids = request.data.get('ids', [])
    User.objects.filter(id__in=ids).delete()
    return Response({'deleted_ids': ids}, status=status.HTTP_204_NO_CONTENT)

