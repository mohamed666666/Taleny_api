from django.contrib.auth import authenticate
from rest_framework import serializers
from .BaseUserSerlaizer import UserRegistrationSerializer
from ..models.investgator import Investgator

class InvesgatorRegistrationSerializer(serializers.ModelSerializer):
    user = UserRegistrationSerializer()
    class Meta:
        model = Investgator
        fields = ['user', 'cr','company_name']

    def create(self, validated_data):
        user_data = validated_data.pop('user')
        
        user_serializer = UserRegistrationSerializer(data=user_data)
        user_serializer.is_valid(raise_exception=True)
        user = user_serializer.save()
        investgator=Investgator.objects.create(user=user,cr=validated_data.pop('cr'))

        return investgator