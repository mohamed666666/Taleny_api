from rest_framework import serializers
from ..models.Cover import CoverPhoto


class CoverPhotoSerializer(serializers.ModelSerializer):
    class Meta:
        model = CoverPhoto
        fields = ['id', 'user', 'image']
        
        
    def create(self, validated_data):
        # Create a new CoverPhoto object using the validated data
        return CoverPhoto.objects.create(**validated_data)

    def update(self, instance, validated_data):
        # Update the existing CoverPhoto instance with new validated data
        instance.user = validated_data.get('user', instance.user)
        instance.image = validated_data.get('image', instance.image)
        instance.save()
        return instance