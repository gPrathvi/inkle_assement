from rest_framework.permissions import BasePermission

from rest_framework.permissions import SAFE_METHODS

class IsAuthorOrAdmin(BasePermission):
    def has_object_permission(self, request, view, obj):
        # Allow safe methods for any authenticated user
        if request.method in SAFE_METHODS:
            return True
        user = request.user
        if not user or not user.is_authenticated:
            return False
        # Author can modify their own post
        if obj.author_id == user.id:
            return True
        # Admins/Owners can modify
        return getattr(user, "is_admin", lambda: False)() or getattr(user, "is_owner", lambda: False)()

class IsCommentAuthorOrAdmin(BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in SAFE_METHODS:
            return True
        user = request.user
        if not user or not user.is_authenticated:
            return False
        if obj.author_id == user.id:
            return True
        return getattr(user, "is_admin", lambda: False)() or getattr(user, "is_owner", lambda: False)()
