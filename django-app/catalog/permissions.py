from rest_framework.permissions import BasePermission

class IsEditor(BasePermission):
    def has_permission(self, request, view):
        return getattr(request.user, "role", None) == "editor"

class IsArtist(BasePermission):
    """
    Allows access only to users with the 'artist' permission.
    """
    def has_permission(self, request, view):
        return request.user.is_authenticated and getattr(request.user, "role", None) == "artist"

class IsViewer(BasePermission):
    """
    Allows access only to users with the 'viewer' permission.
    """
    def has_permission(self, request, view):
        return request.user.is_authenticated and getattr(request.user, "role", None) == "viewer"
    
class IsViewerOrEditor(BasePermission):
    def has_permission(self, request, view):
        return request.user.role in ['editor', 'viewer', 'artist']