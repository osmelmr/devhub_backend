from rest_framework import serializers
from .models import User
from apps.projects.models import Project  # Asegúrate de que la ruta sea correcta

class UserSerializer(serializers.ModelSerializer):
    projects = serializers.PrimaryKeyRelatedField(many=True, read_only=True)

    class Meta:
        model = User
        fields = [
            'id',
            'username',
            'email',
            'first_name',
            'last_name',
            'role',
            'projects',
        ]
