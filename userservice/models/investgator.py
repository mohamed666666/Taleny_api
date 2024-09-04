from django.db import models
from .Baseuser import UserBase


class Investgator(models.Model):
    user=models.OneToOneField(UserBase,on_delete=models.CASCADE)
    company_name=models.CharField(max_length=50)
    cr=models.IntegerField()
    
    def __str__(self) -> str:
        return self.user.user_name