
# serializers.py
from rest_framework import serializers
from .models import Case, File

class CaseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Case
        fields = '__all__'

class FileSerializer(serializers.ModelSerializer):
    presigned_url = serializers.SerializerMethodField()

    class Meta:
        model = File
        fields = ['id', 'case', 'file_upload', 'created_at', 'updated_at', 'presigned_url']

    def get_presigned_url(self, obj):
        request = self.context.get('request')
        if request:
            # Get the expiration time from the request or use a default value
            expiration = request.GET.get('expiration', 3600)
        else:
            expiration = 3600

        return obj.generate_presigned_url(expiration)