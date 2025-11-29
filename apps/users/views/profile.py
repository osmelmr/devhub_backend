from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework import status
from ..models import User
from ..serializers import UserSerializer
from rest_framework.permissions import IsAuthenticated
from devhub.utils import delete_image
from django.shortcuts import get_object_or_404



@api_view(["GET"])
@permission_classes([IsAuthenticated])
def me(request):
    user = request.user  # DRF rellena este objeto gracias al token JWT
    return Response({
        "username": user.username,
        "email": user.email,
        "first_name": user.first_name,
        "last_name": user.last_name,
        "avatar_url": user.avatar_url,
    })

@api_view(['PUT', 'PATCH'])
@permission_classes([IsAuthenticated])
def update_user(request, pk):
    user = get_object_or_404(User, pk=pk)

    # Guardamos la URL actual antes de actualizar
    old_avatar_url = user.avatar_url
    old_avatar_public_id = user.avatar_public_id

    serializer = UserSerializer(user, data=request.data, partial=True)
    if serializer.is_valid():
        # Obtenemos la nueva URL que viene en el request (si existe)
        new_avatar_url = serializer.validated_data.get("avatar_url")

        # Si hay avatar nuevo y es distinto al anterior, borramos el viejo en Cloudinary
        if new_avatar_url and old_avatar_url and new_avatar_url != old_avatar_url:
            if old_avatar_public_id:
                delete_image(old_avatar_public_id)

        # Guardamos cambios en el usuario
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)

    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def delete_avatar(request):
    user = request.user

    # Si el usuario no tiene avatar registrado
    if not user.avatar_url:
        return Response(
            {"error": "No hay avatar para eliminar"},
            status=status.HTTP_400_BAD_REQUEST
        )
    
    if not user.avatar_public_id:
        return Response(
            {"error": "No hay public id para eliminar"},
            status=status.HTTP_400_BAD_REQUEST
        )

    # Intentar borrar en Cloudinary
    result = delete_image(user.avatar_public_id)

    if result.get("result") == "ok":
        # Limpiar campos en la base de datos
        user.avatar_url = None
        user.avatar_public_id = None
        user.save()

        return Response(
            {"message": "Avatar eliminado correctamente"},
            status=status.HTTP_200_OK
        )
    else:
        return Response(
            {"error": "No se pudo eliminar el avatar en Cloudinary"},
            status=status.HTTP_400_BAD_REQUEST
        )

@api_view(["DELETE"])
@permission_classes([IsAuthenticated])
def delete_my_account(request):
    user = request.user

    # Guardamos infos del avatar por si hay que borrarlo
    avatar_public_id = user.avatar_public_id

    # Si existe avatar, lo eliminamos en Cloudinary
    if avatar_public_id:
        delete_image(avatar_public_id)

    # Eliminamos el usuario
    user.delete()

    return Response(
        {"message": "Tu cuenta ha sido eliminada correctamente."},
        status=status.HTTP_200_OK
    )
