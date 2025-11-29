from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import permission_classes, api_view
from rest_framework.response import Response
from rest_framework import status
from ..serializers import UserSerializer
from django.contrib.auth import get_user_model
import jwt
from time import time
import requests as http_requests

User = get_user_model()

@api_view(["GET"])
@permission_classes([IsAuthenticated])
def me(request):
    user = request.user
    return Response({
        "id": user.id,
        "username": user.username,
        "email": user.email,
        "first_name": user.first_name,
        "last_name": user.last_name,
        "role": user.role,
        "avatar_url": user.avatar_url,
    })

@api_view(['POST'])
def register_user(request):
    serializer = UserSerializer(data=request.data)
    if serializer.is_valid():
        user = serializer.save()
        refresh = RefreshToken.for_user(user)
        access = refresh.access_token
        return Response({"user": serializer.data,"access": str(access), "refresh":str(refresh)}, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

def verify_id_token(id_token_string):
    """Verificación de ID Token"""
    try:
        payload = jwt.decode(id_token_string, options={"verify_signature": False})
        
        if payload.get("aud") != "641920284570-1if23hcfa9dl2hvn742qllmag3eg5g5v.apps.googleusercontent.com":
            return None
            
        if payload.get("exp", 0) < time():
            return None
            
        return {
            "email": payload["email"],
            "first_name": payload.get("name", ""),
            "avatar_url": payload.get("picture", ""),
        }
    except:
        return None
    

# Authenticaciones externas


# para id_token

# Versión segura para producción
# def verify_google_token_production(id_token_string):
#     try:
#         from google.oauth2 import id_token
#         from google.auth.transport import requests
        
#         id_info = id_token.verify_oauth2_token(
#             id_token_string, 
#             requests.Request(),
#             "tu-client-id"
#         )
#         return {
#             "email": id_info["email"],
#             "first_name": id_info.get("name", ""),
#             "avatar_url": id_info.get("picture", ""),
#         }
#     except:
#         return None


def verify_access_token(access_token):
    """Verificación de Access Token"""
    try:
        userinfo_url = "https://www.googleapis.com/oauth2/v3/userinfo"
        headers = {
            'Authorization': f'Bearer {access_token}',
            'Accept': 'application/json'
        }
        
        response = http_requests.get(userinfo_url, headers=headers, timeout=10)
        
        if response.status_code != 200:
            return None
        
        user_data = response.json()
        
        return {
            "email": user_data["email"],
            "first_name": user_data.get("name", ""),
            "avatar_url": user_data.get("picture", ""),
            "google_id": user_data.get("sub")
        }
        
    except Exception:
        return None

@api_view(["POST"])
def social_login(request):
    try:
        provider = request.data.get("provider")
        token = request.data.get("token")
        
        if not provider or not token:
            return Response({"detail": "provider y token son requeridos"}, status=400)

        if provider == "google":
            user_data = verify_access_token(token)
            
            if not user_data:
                user_data = verify_id_token(token)
        else:
            return Response({"detail": "Proveedor no soportado"}, status=400)

        if not user_data:
            return Response({"detail": "Token inválido"}, status=400)

        username = user_data["email"].split('@')[0]
        
        user, created = User.objects.get_or_create(
            email=user_data["email"],
            defaults={
                "username": username,
                "first_name": user_data.get("first_name", ""),
                "avatar_url": user_data.get("avatar_url", ""),
            }
        )

        refresh = RefreshToken.for_user(user)
        
        return Response({
            "access": str(refresh.access_token),
            "refresh": str(refresh),
            "user": {
                "id": str(user.id),
                "email": user.email,
                "username": user.username,
                "first_name": user.first_name,
                "avatar_url": user.avatar_url,
            },
            "is_new": created
        })
    
    except Exception:
        return Response({"detail": "Error interno del servidor"}, status=500)