from django.db import models
from userservice.models.Baseuser import UserBase

class Comment(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    desc = models.TextField( 'desc',  blank=True)
    created_by=models.ForeignKey(UserBase,on_delete=models.CASCADE,related_name='post_creator')

