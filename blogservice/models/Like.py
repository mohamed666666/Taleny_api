from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.db import models
from django.core.exceptions import ValidationError
from userservice.models.Baseuser import UserBase
from .Post import Post
from .Comment import Comment

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
        # Check if the user has already liked the post or the comment of the post
        if isinstance(self.content_object, Comment):
            post = self.content_object.on_post
            if Like.objects.filter(created_by=self.created_by, content_type=ContentType.objects.get_for_model(Post), object_id=post.id).exists():
                raise ValidationError("You cannot like both the post and a comment on the same post.")
        elif isinstance(self.content_object, Post):
            comments_on_post = Comment.objects.filter(on_post=self.content_object)
            if Like.objects.filter(created_by=self.created_by, content_type=ContentType.objects.get_for_model(Comment), object_id__in=comments_on_post.values_list('id', flat=True)).exists():
                raise ValidationError("You cannot like both the post and a comment on the same post.")
        
        super().save(*args, **kwargs)