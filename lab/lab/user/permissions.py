from rest_framework import permissions
    
class AnyOfGroups(permissions.BasePermission):
    def __init__(self, *groups):
        # Normalize all group names to lowercase
        self.groups = [g.lower() for g in groups]

    def has_permission(self, request, view):
        if not request.user.is_authenticated:
            return False

        # Compare group names case-insensitively
        user_groups = request.user.groups.values_list('name', flat=True)
        user_groups_lower = [g.lower() for g in user_groups]

        return any(g in user_groups_lower for g in self.groups)
