from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.db import models
from userservice.models.Baseuser import UserBase


class Like(models.Model):
    created_by = models.ForeignKey(UserBase, on_delete=models.CASCADE, related_name='likes')
    created_at = models.DateTimeField(auto_now_add=True)
    
    # GenericForeignKey to support liking a post or a comment
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')
    
    class Meta:
        unique_together = ('created_by', 'content_type', 'object_id')  # Ensure no duplicate likes on the same object

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)