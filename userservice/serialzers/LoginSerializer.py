
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from ..models.talent import Talentee
from ..models.investgator import Investgator
from rest_framework import serializers
from notificationservice.models import CustomDevice


class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    RegisterationFcmToken = serializers.CharField(write_only=True,required=False)
    
    @classmethod
    def get_token(cls, user):
        # Create the token object using the default implementation
        token = super().get_token(user)

        # Add custom claims for user data directly to the token payload
        token['email'] = user.email
        token['user_name'] = user.user_name
        token['full_name'] = user.full_name
        token['title'] = user.title
        token['about'] = user.about
        token['age'] = user.age
        token['phone_number'] = user.phone_number
        token['government'] = user.government
        token['area'] = user.area
        token['profile_image'] = user.profile_image.url if user.profile_image else None
        
        # Check the user's role explicitly using exists()
        if Talentee.objects.filter(user=user).exists():
            token['role'] = 'Talentee'
        elif Investgator.objects.filter(user=user).exists():
            token['role'] = 'Investigator'
        else:
            token['role'] = 'Admin'
            

        return token

    def validate(self, attrs):
        data = super().validate(attrs)

        # Extract the FCM token from the validated data
        fcm_token = attrs.get('RegisterationFcmToken', None)

        # If an FCM token is provided, create or update the CustomDevice object
        if fcm_token:
            fcm, created = CustomDevice.objects.get_or_create(user=self.user, defaults={'token': fcm_token})
            if not created:
                # If the device already exists, update the token
                fcm.registration_id = fcm_token
                
                fcm.save()
                

        # Get the access token with custom claims
        access = self.get_token(self.user).access_token

        # Convert the access token to a string to include in the response
        data['access'] = str(access)
        return data