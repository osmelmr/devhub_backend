from rest_framework import serializers
from .models import User
from apps.projects.models import Project

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
            'avatar_url',
            'projects',
            'password',
            'avatar_public_id',
        ]
        extra_kwargs = {
            'password': {'write_only': True},  # Nunca devolver la contraseña
            'avatar_public_id': {'write_only': True}
        }

    def create(self, validated_data):
        password = validated_data.pop('password', None)
        user = User(**validated_data)
        if password:
            user.set_password(password)  # Hash automático
        user.save()
        return user

    def update(self, instance, validated_data):
        password = validated_data.pop('password', None)
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        if password:
            instance.set_password(password)  # Hash automático
        instance.save()
        return instance
