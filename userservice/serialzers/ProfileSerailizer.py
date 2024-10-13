from django.contrib.auth import authenticate
from rest_framework import serializers
from ..models.Baseuser import UserBase
from ..models.Cover import CoverPhoto
from ..models.follow import Follow

class ProfileSerializer(serializers.ModelSerializer):
    role = serializers.SerializerMethodField()
    coverphoto = serializers.SerializerMethodField()
    following=serializers.SerializerMethodField()
    class Meta:
        model = UserBase
        fields = [
            'id',
            'user_name',
            'full_name',
            'about',
            'title',
            'profile_image',
            'role',
            'coverphoto',
            'following'
        ]
        read_only_fields = ['user_name','id']
    
    def get_role(self, obj):
        if hasattr(obj, 'talentee'):
            return 'Talentee'
        elif hasattr(obj, 'investgator'):
            return 'Investigator'
        
        return 'Admin'  # In case the user is neither
    
    
    def get_coverphoto(self, obj):
        cover_photo = CoverPhoto.objects.filter(user=obj).first()
        
        if cover_photo:
            return cover_photo.image.url
        return None

    def get_following(self,object):
        user = self.context.get('request_user')
        
        if user:
            try:
                # Check if there's a follow relationship between request.user and the post creator
                follow = Follow.objects.get(follow_from=user, follow_to=object)
                
                # Return status based on the follow status
                if follow.status:
                    return "following"
                else:
                    return "pending"
            except Follow.DoesNotExist:
                return "notfollowing"
        return None


class ProfileUserUpdateSerializer(serializers.ModelSerializer):
    coverphoto = serializers.ImageField(required=False)
    class Meta:
        model = UserBase
        fields = [
            'full_name',
            'age',
            'government',
            'area',
            'about',
            'phone_number',
            'title',
            'profile_image',
            'coverphoto'
        ]
        read_only_fields = ['id']
        
        
    def update(self, instance, validated_data):
        # Update the user fields
        coverphoto_data = validated_data.pop('coverphoto', None)
        if coverphoto_data:
            # Create or update the cover photo for the user
            CoverPhoto.objects.update_or_create(user=instance, defaults={'image': coverphoto_data})
        
        return super().update(instance, validated_data)
    def to_representation(self, instance):
        """
        Customize the serialized output.
        """
        representation = super().to_representation(instance)
        # Add attachments in the representation
        attachment = CoverPhoto.objects.get(user=instance)
        representation['coverphoto'] = attachment.image.url
         
        return representation