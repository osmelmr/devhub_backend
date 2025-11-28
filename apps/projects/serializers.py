from rest_framework import serializers
from .models import Project

class ProjectSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source='user.username', read_only=True)

    class Meta:
        model = Project
        fields = [
            'id',
            'title',
            'slug',
            'short_description',
            'description',
            'thumbnail_light',
            'thumbnail_dark',
            'tech_stack',
            'status',
            'user',
            'username',
            'created_at',
            'updated_at',
            'thumbnail_dark_public_id',
            'thumbnail_light_public_id',
        ]
        extra_kwargs = {
            'thumbnail_dark_public_id': {'write_only': True}, 
            'thumbnail_light_public_id': {'write_only': True}
        }