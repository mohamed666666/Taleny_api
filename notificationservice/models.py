import uuid
from django.db import models
from fcm_django.models import AbstractFCMDevice
from django.conf import settings

class CustomDevice(AbstractFCMDevice):
    # fields could be overwritten
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    # could be added new fields
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='fcm_tokens')
    token = models.CharField(max_length=255, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)

    updated_at = models.DateTimeField(auto_now=True)