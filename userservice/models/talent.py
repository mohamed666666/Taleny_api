from django.db import models
from .Baseuser import UserBase

class Talent(models.Model):
    name=models.CharField(max_length=50)
    def __str__(self) -> str:
        return self.name
    
    
class Talentee(models.Model):
    user=models.OneToOneField(UserBase , on_delete=models.CASCADE,primary_key=True)
    talent=models.ForeignKey(Talent,on_delete=models.SET_NULL,null=True)

    def __str__(self) -> str:
        return self.user.user_name