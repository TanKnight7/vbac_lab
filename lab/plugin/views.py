from rest_framework import permissions, viewsets
from rest_framework.exceptions import PermissionDenied
from .models import Plugin
from .serializers import PluginSerializer, PluginUpdateSerializer
from user.permissions import AnyOfGroups
from django.db import models
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import permissions, viewsets, status


class PluginViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows Plugins to be viewed or edited.
    """
    queryset = Plugin.objects.all().order_by('-is_active', 'name')
    serializer_class = PluginSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_permissions(self):
        actions = {
            'create': [permissions.IsAuthenticated(), AnyOfGroups('Super Admin')],
            'update': [permissions.IsAuthenticated(), AnyOfGroups('Super Admin', 'Administrator')],
            'destroy': [permissions.IsAuthenticated(), AnyOfGroups('Super Admin', 'Administrator')],
            'retrieve': [permissions.IsAuthenticated(), AnyOfGroups('Super Admin', 'Administrator')],
            'list': [permissions.IsAuthenticated(), AnyOfGroups('Super Admin', 'Administrator')],
            'activate': [permissions.IsAuthenticated(), AnyOfGroups('Super Admin', 'Administrator')],
            'deactivate': [permissions.IsAuthenticated(), AnyOfGroups('Super Admin', 'Administrator')]
        }
        return actions.get(self.action, [permissions.AND(permissions.IsAuthenticated(), permissions.NOT(permissions.IsAuthenticated()))])
    
    def get_serializer_class(self):
        if self.action == "update":
            return PluginUpdateSerializer
        return PluginSerializer
    
    # === CREATE Plugin, status is draft by default ===
    def perform_create(self, serializer):
        user = self.request.user
        serializer.save(is_active=False)
    
    # === UPDATE Plugin ===
    def perform_update(self, serializer):
        serializer.save(); return
    
    
    # === DELETE Plugin ===
    def perform_destroy(self, instance):
        instance.delete(); return
        
    @action(detail=True, methods=["post"])
    def activate(self, request, pk=None):
        """
        Activate this plugin and deactivate others.
        """
        try:
            plugin_to_activate = self.get_object()
        except Plugin.DoesNotExist:
            return Response({"error": "Plugin not found"}, status=status.HTTP_404_NOT_FOUND)

        # Activate selected plugin
        plugin_to_activate.is_active = True
        plugin_to_activate.save()

        return Response({"status": f"Plugin '{plugin_to_activate.name}' activated"}, status=status.HTTP_200_OK)
    
    @action(detail=True, methods=["post"])
    def deactivate(self, request, pk=None):
        """
        Deactivate this plugin and deactivate others.
        """
        try:
            plugin_to_deactivate = self.get_object()
        except Plugin.DoesNotExist:
            return Response({"error": "Plugin not found"}, status=status.HTTP_404_NOT_FOUND)

        # Activate selected plugin
        plugin_to_deactivate.is_active = False
        plugin_to_deactivate.save()

        return Response({"status": f"Plugin '{plugin_to_deactivate.name}' deactivated"}, status=status.HTTP_200_OK)
