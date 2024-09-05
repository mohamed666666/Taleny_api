from django.contrib.auth import authenticate
from rest_framework import serializers
from ..models.Baseuser import UserBase


class UserRegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    password_confirm = serializers.CharField(write_only=True)
    profile_image=serializers.ImageField(required=False)

    class Meta:
        model = UserBase
        fields = ['user_name','full_name', 'email','title','phone_number',
                  'government','area','profile_image'
                  , 'password', 'password_confirm']

    def validate(self, data):
        if data['password'] != data['password_confirm']:
            raise serializers.ValidationError("Passwords do not match.")
        return data

    def create(self, validated_data):
        validated_data.pop('password_confirm')
        profile_image = validated_data.pop('profile_image', None)
        user = UserBase(
            user_name=validated_data['user_name'],
            email=validated_data['email'],
            full_name=validated_data['full_name'],
            phone_number=validated_data['phone_number'],
            government=validated_data['government'],
            area=validated_data['area'],
            profile_image=profile_image,
        )
        user.set_password(validated_data['password'])
        user.save()
        return user