from django.db import models
from userservice.models.Baseuser import UserBase

class Post(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    content = models.TextField( 'content',  blank=True)
    created_by=models.ForeignKey(UserBase,on_delete=models.CASCADE,related_name='post_creator')
    
    def __str__(self) -> str:
        return str(self.id)


class Post_attachement(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    attachment_file=models.FileField(upload_to='post_attachments/')
    post=models.ForeignKey(Post,on_delete=models.CASCADE,related_name='post')
    
    def __str__(self) -> str:
        return 'attached_to'+str(self.post.id)