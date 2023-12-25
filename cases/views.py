from rest_framework import serializers, viewsets
from .models import Case, File
from .permissions import IsOwnerOrReadOnly, CommonAuthenticationMixin
from .serializers import CaseSerializer, FileSerializer
from rest_framework.decorators import action
from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from django.utils import timezone
import requests
from rq import Queue
from core.settings import redis_client


def reindex_files(case_id):
    pass

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
        
    @action(detail=False, methods=['post'])
    def reindex(self, request):
        """
        Reindexes the files in a case
        """
        user = self.request.user

        # Check if the user is authenticated
        if not user.is_authenticated:
            return Response({"error": "Authentication required"}, status=401)

        # Store the request body before accessing request.data
        request_body = request.body

        # Get the case_id from the request data
        case_id = request.data.get('case')

        # Check if case_id is provided
        if not case_id:
            return Response({"error": "Case ID is required"}, status=400)

        # Get the case object or return 404 if not found
        case = get_object_or_404(Case, id=case_id, user=user)
        case_id = str(case.id)

        # Add your reindexing logic here using the case object
        File.objects.filter(case=case).update(updated_at=timezone.now())
        # Enqueue the task
        queue = Queue(connection=redis_client)
        result = queue.enqueue(reindex_files, case_id)


        return Response({"message": f"Task {result.id} enqueued for reindexing files in Case {case_id}"}, status=200)