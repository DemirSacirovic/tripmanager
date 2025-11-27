"""
Custom permission classes for the trips API.

This module implements DRF permission classes following the principle of
defense in depth - combining view-level and object-level permissions.
"""
from rest_framework import permissions


class IsOwnerOrReadOnly(permissions.BasePermission):
    """
    Object-level permission to allow read access to any request,
    but only allow write access to the owner of the trip.

    This permission class implements a common pattern where:
    - GET, HEAD, OPTIONS (safe methods) are allowed for all authenticated users
    - POST, PUT, PATCH, DELETE require the user to be the trip's traveler

    Usage:
        permission_classes = [IsAuthenticated, IsOwnerOrReadOnly]

    Security Note:
        Always combine with IsAuthenticated to ensure unauthenticated
        users cannot access any resources.
    """

    def has_object_permission(self, request, view, obj):
        """
        Check if the request should be permitted for a specific object.

        Args:
            request: The incoming HTTP request
            view: The view handling the request
            obj: The Trip instance being accessed

        Returns:
            True if permission is granted, False otherwise
        """
        # Read permissions are allowed to any authenticated request
        if request.method in permissions.SAFE_METHODS:
            return True

        # Write permissions only for the trip's traveler
        # Using getattr for safety in case traveler is None
        traveler = getattr(obj, 'traveler', None)
        if traveler is None:
            return False

        return traveler.id == request.user.id


class IsManagerOrReadOnly(permissions.BasePermission):
    """
    Permission class for manager-level operations.

    Allows read access to all authenticated users, but restricts
    write operations to users in the 'Managers' group.

    This is useful for approval workflows where only managers
    can approve or reject trip requests.
    """

    def has_permission(self, request, view):
        """
        Check view-level permission.

        Returns:
            True for safe methods or if user is a manager
        """
        if request.method in permissions.SAFE_METHODS:
            return True

        return request.user.groups.filter(name='Managers').exists()
