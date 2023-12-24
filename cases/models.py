import uuid
from django.db import models
from users.models import CustomUser

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


