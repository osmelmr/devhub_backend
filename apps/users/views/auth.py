from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import permission_classes, api_view
from rest_framework.response import Response
from rest_framework import status
from ..serializers import UserSerializer
from django.contrib.auth import get_user_model
import requests

User = get_user_model()

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

@api_view(['POST'])
def register_user(request):
    serializer = UserSerializer(data=request.data)
    if serializer.is_valid():
        user = serializer.save()
        refresh = RefreshToken.for_user(user)
        access = refresh.access_token
        return Response({"user": serializer.data,"access": str(access), "refresh":str(refresh)}, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# Authenticaciones externas

def verify_google_token(token):
    url = f"https://oauth2.googleapis.com/tokeninfo?id_token={token}"
    res = requests.get(url)
    if res.status_code != 200:
        return None
    data = res.json()
    if "email" not in data:
        return None
    return {
        "email": data["email"],
        "name": data.get("name", ""),
        "avatar": data.get("picture", "")
    }

def verify_github_token(token):
    headers = {"Authorization": f"Bearer {token}"}
    res = requests.get("https://api.github.com/user", headers=headers)
    if res.status_code != 200:
        return None
    data = res.json()
    email = data.get("email")
    if not email:
        res_emails = requests.get("https://api.github.com/user/emails", headers=headers)
        if res_emails.status_code != 200:
            return None
        emails = res_emails.json()
        primary_emails = [e["email"] for e in emails if e.get("primary") and e.get("verified")]
        email = primary_emails[0] if primary_emails else None
    if not email:
        return None
    return {
        "email": email,
        "name": data.get("login", ""),
        "avatar": data.get("avatar_url", "")
    }


PROVIDERS = {
    "google": verify_google_token,
    "github": verify_github_token,
}

@api_view(["POST"])
def social_login(request):
    provider = request.data.get("provider")
    token = request.data.get("access_token") or request.data.get("id_token")

    if not provider or not token:
        return Response({"detail": "provider y token son requeridos"}, status=400)

    if provider not in PROVIDERS:
        return Response({"detail": "Proveedor no soportado"}, status=400)

    # Validar token con el proveedor
    user_data = PROVIDERS[provider](token)
    if not user_data:
        return Response({"detail": "Token inválido"}, status=400)

    # Crear o recuperar usuario
    user, created = User.objects.get_or_create(
        email=user_data["email"],
        defaults={
            "username": user_data["name"],
            "avatar": user_data["avatar"],
        }
    )

    # Generar tokens JWT
    refresh = RefreshToken.for_user(user)

    return Response({
        "access": str(refresh.access_token),
        "refresh": str(refresh),
        "user": {
            "email": user.email,
            "username": user.username,
            "avatar": user.avatar,
        },
        "is_new": created
    })



