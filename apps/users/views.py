from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework import status
from .models import User
from .serializers import UserSerializer
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAuthenticated
from devhub.permissions import IsAdminUser
from devhub.pagination import StandardResultsSetPagination
from rest_framework_simplejwt.tokens import RefreshToken


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def me(request):
    user = request.user  # DRF rellena este objeto gracias al token JWT
    return Response({
        "id": user.id,
        "username": user.username,
        "email": user.email,
        "first_name": user.first_name,
        "last_name": user.last_name,
        "role": user.role,
        "avatar_url": user.avatar_url,
    })

@api_view(['GET'])
@permission_classes([IsAuthenticatedOrReadOnly])
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
def create_user(request):
    serializer = UserSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
def register_user(request):
    serializer = UserSerializer(data=request.data)
    if serializer.is_valid():
        user = serializer.save()
        refresh = RefreshToken.for_user(user)
        access = refresh.access_token
        return Response({"user": serializer.data,"access": str(access), "refresh":str(refresh)}, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['PUT', 'PATCH'])
@permission_classes([IsAuthenticatedOrReadOnly, IsAdminUser])
def update_user(request, pk):
    try:
        user = User.objects.get(pk=pk)
    except User.DoesNotExist:
        return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)
    serializer = UserSerializer(user, data=request.data, partial=True)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)
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
