from rest_framework import permissions


class IsOrganizer(permissions.BasePermission):
    """Only lets Organizers (or Admins) through."""

    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role in ("organizer", "admin")


class IsOwnerOrAdmin(permissions.BasePermission):
    """Lets you edit something only if YOU created it (or you're an Admin)."""

    def has_object_permission(self, request, view, obj):
        # Safe methods (GET, HEAD, OPTIONS) are always allowed - just viewing, no risk
        if request.method in permissions.SAFE_METHODS:
            return True

        if request.user.role == "admin":
            return True

        # obj could be an Event (has .organizer) - check they match the logged-in user
        return getattr(obj, "organizer", None) == request.user