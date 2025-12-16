from rest_framework import permissions, viewsets
from rest_framework.exceptions import PermissionDenied
from .models import Theme
from .serializers import ThemeSerializer, ThemeUpdateSerializer
from user.permissions import AnyOfGroups
from django.db import models
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import permissions, viewsets, status

class ThemeViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows Themes to be viewed or edited.
    """
    queryset = Theme.objects.all().order_by("-created_at")
    serializer_class = ThemeSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_permissions(self):
        actions = {
            'create': [permissions.IsAuthenticated(), AnyOfGroups('Super Admin')],
            'update': [permissions.IsAuthenticated(), AnyOfGroups('Super Admin', 'Administrator')],
            'destroy': [permissions.IsAuthenticated(), AnyOfGroups('Super Admin', 'Administrator')],
            'retrieve': [permissions.IsAuthenticated(), AnyOfGroups('Super Admin', 'Administrator')],
            'list': [permissions.IsAuthenticated(), AnyOfGroups('Super Admin', 'Administrator')],
            'activate': [permissions.IsAuthenticated(), AnyOfGroups('Super Admin', 'Administrator')]
        }
        return actions.get(self.action, [permissions.AND(permissions.IsAuthenticated(), permissions.NOT(permissions.IsAuthenticated()))])
    
    def get_serializer_class(self):
        if self.action == "update":
            return ThemeUpdateSerializer
        return ThemeSerializer
    
    # === CREATE Theme, status is draft by default ===
    def perform_create(self, serializer):
        user = self.request.user
        serializer.save(is_active=False)
    
    # === UPDATE Theme ===
    def perform_update(self, serializer):
        serializer.save(); return
    
    
    # === DELETE Theme ===
    def perform_destroy(self, instance):
        if instance.is_active:
            raise PermissionDenied("You cannot delete a theme that is currently active.")
        instance.delete(); return
        
    @action(detail=True, methods=["post"])
    def activate(self, request, pk=None):
        """
        Activate this theme and deactivate others.
        """
        try:
            theme_to_activate = self.get_object()
        except Theme.DoesNotExist:
            return Response({"error": "Theme not found"}, status=status.HTTP_404_NOT_FOUND)

        # Deactivate currently active theme(s)
        Theme.objects.filter(is_active=True).update(is_active=False)

        # Activate selected theme
        theme_to_activate.is_active = True
        theme_to_activate.save()

        return Response({"status": f"Theme '{theme_to_activate.name}' activated"}, status=status.HTTP_200_OK)
