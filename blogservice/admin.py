from django.contrib import admin
from .models.Post import Post,Post_attachement
from .models.Like import Like
from .models.Comment import Comment
# Register your models here.
admin.site.register(Post)
admin.site.register(Post_attachement)

admin.site.register(Like)

admin.site.register(Comment)
