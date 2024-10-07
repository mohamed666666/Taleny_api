from django.db import models
from .Baseuser import UserBase


class CoverPhoto(models.Model):
    user=models.ForeignKey(UserBase,on_delete=models.CASCADE,related_name='user_cover')
    image=models.ImageField(upload_to='covers/',default='profile_images/default.png')