from rest_framework import serializers
from ..models.Skill import Skill ,Skill_attachments,skilled_in
from ..models.talent import Talentee

class SkillSerializer(serializers.ModelSerializer):
    class Meta:
        model = Skill
        fields = ['id', 'name', 'skill_desc']

# Serializer for the Skill_attachments model
class SkillAttachmentsSerializer(serializers.ModelSerializer):
    skill = SkillSerializer(read_only=True)  # Nested serializer to show skill details
    class Meta:
        model = Skill_attachments
        fields = ['id', 'skill', 'uri']

# Serializer for the skilled_in model to link skills to a Talentee
class SkilledInSerializer(serializers.ModelSerializer):
    talentee = serializers.PrimaryKeyRelatedField(queryset=Talentee.objects.all())
    skill = SkillSerializer(read_only=True)
    attachments = SkillAttachmentsSerializer(source='skill.skill_attachments_set', many=True, read_only=True)

    class Meta:
        model = skilled_in
        fields = [ 'talentee', 'skill', 'attachments']