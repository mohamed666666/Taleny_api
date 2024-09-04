from django.db import models
from .talent import Talentee


class Skill(models.Model):
    name=models.CharField(max_length=50)
    skill_desc=models.CharField(max_length=150)
    
class Skill_attachments(models.Model):
    skill=models.ForeignKey(Skill,on_delete=models.CASCADE)
    uri=models.FileField(upload_to='skill_attachments/')


class skilled_in(models.Model):
    talentee=models.ForeignKey(Talentee,on_delete=models.CASCADE)
    skill=models.ForeignKey(Skill,on_delete=models.CASCADE)
    