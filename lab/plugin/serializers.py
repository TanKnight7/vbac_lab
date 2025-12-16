from rest_framework import serializers
from .models import Plugin


class PluginSerializer(serializers.HyperlinkedModelSerializer):
    
    class Meta:
        model = Plugin
        fields = ['id', 'name', 'version', 'is_active', 'settings', 'created_at', 'updated_at']
        read_only_fields = ['created_at', 'updated_at', 'is_active']

    def __str__(self):
        return f"{self.name} ({self.version})"

class PluginUpdateSerializer(serializers.HyperlinkedModelSerializer):
    
    class Meta:
        model = Plugin
        fields = ['id', 'name', 'version', 'is_active', 'settings', 'created_at', 'updated_at']
        read_only_fields = ['created_at', 'updated_at', 'is_active']

    def __str__(self):
        return f"{self.name} ({self.version})"