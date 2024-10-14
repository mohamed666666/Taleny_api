from django.contrib.auth import authenticate
from rest_framework import serializers
from ..models.Baseuser import UserBase
from ..models import Identifications  # Import Identifications model
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from notificationservice.models import CustomDevice
from ..models.Cover import CoverPhoto
        
class UserRegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    password_confirm = serializers.CharField(write_only=True)
    RegisterationFcmToken = serializers.CharField(write_only=True,required=False)
   
    identifications = serializers.ListField(
        child=serializers.FileField(allow_empty_file=False),
        write_only=True,
        required=False
    )

    class Meta:
        model = UserBase
        fields = ['user_name', 'full_name', 'email', 'phone_number',
                  'government', 'area', 'identifications',
                  'password', 'password_confirm','RegisterationFcmToken']

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
        # create fcm token 
        cover=CoverPhoto.objects.create(user=user)
        cover.save()
        #fcm=CustomDevice(user=user,token=validated_data['RegisterationFcmToken'])
        #fcm.save()
        # Save identification files
        for identification_file in identifications_data:
            Identifications.objects.create(user=user, url=identification_file)
        
        return user
    
    


class UserSerializer(serializers.ModelSerializer):
    role = serializers.SerializerMethodField()
    coverphoto = serializers.SerializerMethodField()
    class Meta:
        model = UserBase
        fields = [
            'id',
            'user_name',
            'full_name',
            'title',
            'profile_image',
            'role',
            'coverphoto'
        ]
        read_only_fields = ['user_name','id']
    
    def get_role(self, obj):
        if hasattr(obj, 'talentee'):
            return 'Talentee'
        elif hasattr(obj, 'investgator'):
            return 'Investigator'
        elif hasattr(obj, 'theadmin'):
            return 'Admin'
        
        return 'Un-known'  # In case the user is neither
    
    
    def get_coverphoto(self, obj):
        cover_photo = CoverPhoto.objects.filter(user=obj).first()
        
        if cover_photo:
            return cover_photo.image.url
        return None
    
    

