from django.contrib.auth import authenticate
from rest_framework import serializers
from ..models.Baseuser import UserBase
from ..models import Identifications  # Import Identifications model
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from ..models.talent import Talentee
from ..models.investgator import Investgator


class UserSerializer(serializers.ModelSerializer):
    role = serializers.SerializerMethodField()
    class Meta:
        model = UserBase
        fields = [
            'id',
            'user_name',
            'full_name',
            'title',
            'profile_image',
            'role',
        ]
        read_only_fields = ['id']
    
    def get_role(self, obj):
        if hasattr(obj, 'talentee'):
            return 'Talentee'
        elif hasattr(obj, 'investgator'):
            return 'Investigator'
        return 'None'  # In case the user is neither




class UserUpdateSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = UserBase
        fields = [
            'id',
            'user_name',
            'full_name',
            'age',
            'government',
            'area',
            'phone_number',
            'title',
            'profile_image',
            
        ]
        read_only_fields = ['id']
    


class UserRegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    password_confirm = serializers.CharField(write_only=True)
    
    identifications = serializers.ListField(
        child=serializers.FileField(allow_empty_file=False, use_url=False),
        write_only=True,
        required=False,
        allow_empty=True
    )

    class Meta:
        model = UserBase
        fields = ['user_name','full_name', 'email','title','phone_number',
                  'government','area','identifications'
                  , 'password', 'password_confirm']

    def validate(self, data):
        if data['password'] != data['password_confirm']:
            raise serializers.ValidationError("Passwords do not match.")
        return data

    def create(self, validated_data):
        validated_data.pop('password_confirm')
        profile_image = validated_data.pop('profile_image', None)
        identifications = validated_data.pop('identifications', [])  # Get images array, default to empty list if not provided
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
        
        # Create Identifications objects for each file
        for f in identifications:
            Identifications.objects.create(user=user, url=f)
        
        return user
    
    
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
