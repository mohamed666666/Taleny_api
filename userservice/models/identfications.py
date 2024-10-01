from django.db import models
from .Baseuser import UserBase


class Identifications(models.Model):
    user=models.ForeignKey(UserBase,on_delete=models.CASCADE)
    url=models.FileField(upload_to='identifications/')
    
    def __str__(self):
        return 'identification of '+self.user.user_name
    