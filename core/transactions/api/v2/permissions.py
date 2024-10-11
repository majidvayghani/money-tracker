# transactions/permissions.py
from rest_framework import permissions

class IsProfileOwner(permissions.BasePermission):
    """
    Custom permission to only allow owners of a profile to access or modify their transactions.
    """
    def has_permission(self, request, view):
        # Ensure the user is authenticated
        return request.user and request.user.is_authenticated
    
    def has_object_permission(self, request, view, obj):
        # Checks if the profile associated with the transaction belongs to the authenticated user.
        profile = obj._profile._user_id
        user = request.user._id
        return profile == user
