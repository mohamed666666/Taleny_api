from rest_framework import serializers
from ..models.Skill import Skill ,Skill_attachments,skilled_in
from ..models.talent import Talentee

class SkillSerializer(serializers.ModelSerializer):
    class Meta:
        model = Skill
        fields = ['id', 'name', 'skill_desc']
    
    def update(self,skill_instance,validated_data):
        
        attachments_data = validated_data.pop('attachments', [])
        # Update other skill fields
        skill_instance.name = validated_data.get('name', skill_instance.name)
        skill_instance.skill_desc = validated_data.get('skill_desc', skill_instance.skill_desc)

        # Handle attachments: delete old and create new ones
        old_attachments = Skill_attachments.objects.filter(skill=skill_instance)
        old_attachments.delete()
        for file in attachments_data:
            Skill_attachments.objects.create(skill=skill_instance, uri=file)

        skill_instance.save()
        return skill_instance
        
# Serializer for the Skill_attachments model
class SkillAttachmentsSerializer(serializers.ModelSerializer):
    # Nested serializer to show skill details
    class Meta:
        model = Skill_attachments
        fields = ['id',  'uri']

# Serializer for the skilled_in model to link skills to a Talentee
class SkilledInSerializer(serializers.ModelSerializer):
    talentee = serializers.PrimaryKeyRelatedField(queryset=Talentee.objects.all())
    skill = SkillSerializer(read_only=True)
    attachments = SkillAttachmentsSerializer(source='skill.skill_attachments_set', many=True)

    class Meta:
        model = skilled_in
        fields = [ 'talentee', 'skill', 'attachments']
        
        