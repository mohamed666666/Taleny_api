from django.db import models
from .Baseuser import UserBase


class Follow(models.Model):
    follow_from=models.ForeignKey(UserBase,on_delete=models.CASCADE,related_name='follow_from')
    follow_to=models.ForeignKey(UserBase,on_delete=models.CASCADE,related_name='Follow_to')
    status=models.BooleanField(default=False)
    
    class Meta:
        unique_together =('follow_from','follow_to')