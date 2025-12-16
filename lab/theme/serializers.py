from rest_framework import serializers
from .models import Theme


class ThemeSerializer(serializers.HyperlinkedModelSerializer):
    
    class Meta:
        model = Theme
        fields = ['id', 'name', 'version', 'is_active', 'options', 'created_at', 'updated_at']
        read_only_fields = ['created_at', 'updated_at', 'is_active']

    def __str__(self):
        return f"{self.name} ({self.version})"
    
class ThemeUpdateSerializer(serializers.HyperlinkedModelSerializer):
    
    class Meta:
        model = Theme
        fields = ['id', 'name', 'version', 'is_active', 'options', 'created_at', 'updated_at']
        read_only_fields = ['created_at', 'updated_at', 'is_active']

    def __str__(self):
        return f"{self.name} ({self.version})"