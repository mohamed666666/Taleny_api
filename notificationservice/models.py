import uuid
from django.db import models
from fcm_django.models import AbstractFCMDevice
from django.conf import settings
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from userservice.models.Baseuser import UserBase

class CustomDevice(AbstractFCMDevice):
    # fields could be overwritten
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    # could be added new fields
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='fcm_tokens')
    
    created_at = models.DateTimeField(auto_now_add=True)
    
    updated_at = models.DateTimeField(auto_now=True)
    
class Notification(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    title=models.CharField(max_length=150)
    message=models.CharField(max_length=250)
    
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')
    
class UserNotifications(models.Model):
    user= models.ForeignKey(UserBase, on_delete=models.CASCADE, related_name='notifications')
    notification=models.ForeignKey(Notification,on_delete=models.CASCADE)
    is_read=models.BooleanField(default=False)
    
    