from rest_framework import serializers
from ..models.Skill import Skill ,Skill_attachments


class SkillSerlaizer(serializers.ModelSerializer):

    class Meta:
        model=Skill
        fields=['id','name','skill_desc']
        
    
        