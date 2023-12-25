from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework import permissions

class IsOwnerOrReadOnly(permissions.BasePermission):
    """
    Custom permission to only allow owners of an object to edit it.
    """
    def has_object_permission(self, request, view, obj):
        # Read permissions are allowed to any request,
        # so we'll always allow GET, HEAD, or OPTIONS requests.
        if request.method in permissions.SAFE_METHODS:
            return True

        # Write permissions are only allowed to the owner of the snippet.
        return obj.user == request.user


class CommonAuthenticationMixin:
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        # Check if the user is authenticated before filtering the queryset
        if user.is_authenticated:
            queryset = super().get_queryset()
            return queryset.filter(user=user)
        else:
            # Handle the case where the user is not authenticated
            return super().get_queryset()

    def perform_create(self, serializer):
        # Ensure the user is authenticated before setting the user field
        if self.request.user.is_authenticated:
            serializer.save(user=self.request.user)
        else:
            # Handle the case where the user is not authenticated
            # You might want to raise an exception or handle it differently
            pass

