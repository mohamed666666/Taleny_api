from django.db import models
from userservice.models.Baseuser import UserBase
from .Post import Post


class Share(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    created_by=models.ForeignKey(UserBase,on_delete=models.CASCADE,related_name='sheared_by')
    post=models.ForeignKey(Post ,related_name='post_sheared',on_delete=models.CASCADE)
