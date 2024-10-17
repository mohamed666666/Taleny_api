
import uuid
from django.db import models
from userservice.models.Baseuser import UserBase


class SMSOTP(models.Model):
    user = models.ForeignKey(UserBase, on_delete=models.CASCADE)
    otp = models.CharField(max_length=6)
    created_at = models.DateTimeField(auto_now_add=True)
    is_verified = models.BooleanField(default=False)
    session_id = models.UUIDField(default=uuid.uuid4, editable=False)