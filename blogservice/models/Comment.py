from django.db import models
from userservice.models.Baseuser import UserBase
from .Post import Post

class Comment(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    content = models.TextField( 'content',  blank=True)
    on_post=models.ForeignKey(Post ,related_name='on_post',on_delete=models.CASCADE)

