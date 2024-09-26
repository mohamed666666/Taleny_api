from django.contrib.auth import authenticate
from rest_framework import serializers
from ..models.Baseuser import UserBase
from ..models import Identifications  # Import Identifications model
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer



        
class UserRegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    password_confirm = serializers.CharField(write_only=True)
    
    identifications = serializers.ListField(
        child=serializers.FileField(allow_empty_file=False),
        write_only=True,
        required=False
    )

    class Meta:
        model = UserBase
        fields = ['user_name', 'full_name', 'email', 'phone_number',
                  'government', 'area', 'identifications',
                  'password', 'password_confirm']

    def validate(self, data):
        if data['password'] != data['password_confirm']:
            raise serializers.ValidationError("Passwords do not match.")
        return data

    def create(self, validated_data):
        validated_data.pop('password_confirm')
        
        # Get the identifications from the request files
        request = self.context.get('request')
       
        identifications_data = request.FILES.getlist('identifications')
        
        # Create the User object
        user = UserBase(
            user_name=validated_data['user_name'],
            email=validated_data['email'],
            full_name=validated_data['full_name'],
            phone_number=validated_data['phone_number'],
            government=validated_data['government'],
            area=validated_data['area'],
        )
        user.set_password(validated_data['password'])
        user.save()
        
        # Save identification files
        for identification_file in identifications_data:
            print(identification_file)
            Identifications.objects.create(user=user, url=identification_file)
        
        return user
    
    


class UserSerializer(serializers.ModelSerializer):
    role = serializers.SerializerMethodField()
    class Meta:
        model = UserBase
        fields = [
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
        return 'Admin'  # In case the user is neither




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
            'about',
            'phone_number',
            'title',
            'profile_image',
        ]
        read_only_fields = ['id']