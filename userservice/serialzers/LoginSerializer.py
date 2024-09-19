
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from ..models.talent import Talentee
from ..models.investgator import Investgator
from .identificationsSerlaizer import IdentifcationsSerlaizer


class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
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
            token['role'] = 'Unknown'

        return token

    def validate(self, attrs):
        data = super().validate(attrs)

        # Get the access token with custom claims
        access = self.get_token(self.user).access_token

        # Convert the access token to a string to include in the response
        data['access'] = str(access)

        return data