from django.db import models
from .Baseuser import UserBase
from .investgator import Investgator
from .talent import Talentee


class TheAdmin(models.Model):
    user=models.OneToOneField(UserBase, verbose_name="Admin", on_delete=models.CASCADE)
    
    def __str__(self) -> str:
        return self.user.user_name
    
    
class ContactRequest(models.Model):
    request_creator=models.ForeignKey(Investgator ,on_delete=models.CASCADE)
    talentee_requested=models.ForeignKey(Talentee,on_delete=models.CASCADE)
    status=models.BooleanField(default=False)
    created_at= models.DateTimeField(auto_now_add=True)
    approved_at = models.DateTimeField(auto_now=True)
    