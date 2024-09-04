from django.db import models
from .Baseuser import UserBase


class Interst(models.Model):
    name=models.CharField("name", max_length=50)
    icon=models.ImageField(upload_to='intrests_icons/')
    
    def __str__(self) -> str:
        return self.name
    
class Intersting_in(models.Model):
    user=models.ForeignKey(UserBase,on_delete=models.CASCADE)
    interst=models.ForeignKey(Interst,on_delete=models.CASCADE)
    
    