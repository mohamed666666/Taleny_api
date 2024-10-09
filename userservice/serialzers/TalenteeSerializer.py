from django.contrib.auth import authenticate
from rest_framework import serializers
from .BaseUserSerlaizer import UserRegistrationSerializer
from ..models.talent import Talentee, Talent
from .BaseUserSerlaizer import UserSerializer

def get_talent_by_id(id):
    try:
        t = Talent.objects.get(id=id)
        return t
    except Talent.DoesNotExist:
        return None

class TalenteeRegistrationSerializer(serializers.ModelSerializer):
    user = UserRegistrationSerializer()
    talent_id = serializers.IntegerField()
   

    class Meta:
        model = Talentee
        fields = [ 'user','talent_id']

    def create(self, validated_data):
        talent = get_talent_by_id(validated_data.pop('talent_id'))
        
        if talent is None:
            raise serializers.ValidationError({"detail": "No valid Talent found."})
        user_data = validated_data.pop('user')
        
        user_serializer = UserRegistrationSerializer(data=user_data, context=self.context)
        user_serializer.is_valid(raise_exception=True)
        user = user_serializer.save()
        

        talentee_profile = Talentee.objects.create(user=user, talent=talent)
        return talentee_profile
    


class TalenteeRetriveSerializer(serializers.ModelSerializer):
    user=UserSerializer()
    class Meta:
        model=Talentee
        fields = [ 'user','talent_id']