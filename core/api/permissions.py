from rest_framework.permissions import BasePermission, SAFE_METHODS


class IsObjectOwner(BasePermission):
    """
    Object-level permission to only allow owners of an object to read or modify it.
    """

    def has_object_permission(self, request, view, user):
        return user == request.user


class IsOwnerOrReadOnly(BasePermission):
    """
    Object-level permission to only allow owners of an object to edit/delete it.
    """

    def has_object_permission(self, request, view, user):
        if request.method in SAFE_METHODS:
            return True
        return user == request.user
