import uuid
from django.db import models
from users.models import CustomUser
import boto3
from botocore.exceptions import ClientError
from core.settings import AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY
import os

class Case(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

def file_upload_to(instance, filename):
    case_id = str(instance.case.id) if instance.case else 'no_case'
    return f'cases/{case_id}/{filename}'

class File(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    case = models.ForeignKey('Case', related_name='files', on_delete=models.CASCADE)
    file_upload = models.FileField(upload_to=file_upload_to)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    filename = models.CharField(max_length=255)
    
    def generate_presigned_url(self, expiration=3600):
        """
        Generate a pre-signed URL for the file.
        :param expiration: Time in seconds until the URL expires (default is 1 hour).
        :return: Pre-signed URL or None if an error occurs.
        """
        s3_client = boto3.client('s3', aws_access_key_id=AWS_ACCESS_KEY_ID, aws_secret_access_key=AWS_SECRET_ACCESS_KEY)

        try:
            response = s3_client.generate_presigned_url(
                'get_object',
                Params={
                    'Bucket': 'dossierr',
                    'Key': str(self.file_upload),
                },
                ExpiresIn=expiration,
            )
            return response
        except ClientError as e:
            print(f"Error generating pre-signed URL: {e}")
            return None
    
    def save(self, *args, **kwargs):
        # Capture the filename without the path
        self.filename = os.path.basename(self.file_upload.name)
        super().save(*args, **kwargs)


