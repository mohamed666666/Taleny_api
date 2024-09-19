from django.db import models
from userservice.models.Baseuser import UserBase

class Post(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    content = models.TextField( 'content',  blank=True)
    created_by=models.ForeignKey(UserBase,on_delete=models.CASCADE,related_name='post_creator')


class Post_attachement(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    post=models.ForeignKey(Post,on_delete=models.CASCADE,related_name='post')