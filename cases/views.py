from rest_framework import serializers, viewsets
from .models import Case, File
from .permissions import IsOwnerOrReadOnly, CommonAuthenticationMixin
from .serializers import CaseSerializer, FileSerializer

# Viewsets
class CaseViewSet(CommonAuthenticationMixin, viewsets.ModelViewSet):
    serializer_class = CaseSerializer
    permission_classes = [IsOwnerOrReadOnly]

    def get_queryset(self):
        user = self.request.user
        # Check if the user is authenticated before filtering the queryset
        if user.is_authenticated:
            return Case.objects.filter(user=user)
        else:
            # Handle the case where the user is not authenticated
            return Case.objects.none()  # Return an empty queryset or handle it differently

    def perform_create(self, serializer):
        # Ensure the user is authenticated before setting the user field
        if self.request.user.is_authenticated:
            serializer.save(user=self.request.user)
        else:
            # Handle the case where the user is not authenticated
            # You might want to raise an exception or handle it differently
            pass


class FileViewSet(CommonAuthenticationMixin, viewsets.ModelViewSet):
    serializer_class = FileSerializer
    permission_classes = [IsOwnerOrReadOnly]

    def get_queryset(self):
        user = self.request.user
        # Check if the user is authenticated before filtering the queryset
        if user.is_authenticated:
            return File.objects.filter(case__user=user)
        else:
            # Handle the case where the user is not authenticated
            return File.objects.none()  # Return an empty queryset or handle it differently

    def perform_create(self, serializer):
        # Ensure the user is authenticated before setting the user field
        if self.request.user.is_authenticated:
            serializer.save(case__user=self.request.user)
        else:
            # Handle the case where the user is not authenticated
            # You might want to raise an exception or handle it differently
            pass
