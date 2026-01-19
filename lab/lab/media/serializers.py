from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Media
from rest_framework.exceptions import ValidationError

class MediaSerializer(serializers.HyperlinkedModelSerializer):
    author_username = serializers.CharField(source='author.username', read_only=True)
    
    class Meta:
        model = Media
        fields = ['id', 'name', 'file', 'author', 'author_username', 'created_at', 'updated_at']
        read_only_fields = ['created_at', 'updated_at', 'author']

    def validate_file(self, value):
        # 5 MB limit
        max_size = 5 * 1024 * 1024  
        if value.size > max_size:
            raise ValidationError("File too large. Maximum allowed size is 5 MB.")

        return value