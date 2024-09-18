from rest_framework import serializers
from ..models.follow import Follow
from ..models.Baseuser import UserBase
from .BaseUserSerlaizer import UserSerializer


class FollowReqesutsAcceptSerializer(serializers.ModelSerializer):
    follow_from = UserSerializer(read_only=True)

    class Meta:
        model = Follow
        fields = ['id', 'follow_from', 'status']

    def update(self, instance, validated_data):
        # Check if the follow_to is the current user
        request_user = self.context['request'].user
        if instance.follow_to != request_user:
            raise serializers.ValidationError("You are not authorized to accept this follow request.")

        # Set follow status to True (accept the follow)
        instance.status = True
        instance.save()
        return instance
    


class FollowToCurrentUserSerlaizer(serializers.ModelSerializer):
    
    follow_from = UserSerializer()
    class Meta:
        model = Follow
        fields=['id','follow_from','status']
        



class FollowCreateSerializer(serializers.ModelSerializer):
    follow_to = serializers.PrimaryKeyRelatedField(queryset=UserBase.objects.all())

    class Meta:
        model = Follow
        fields = ['follow_to']

    def validate(self, data):
        follow_from = self.context['request'].user
        follow_to = data['follow_to']

        if follow_from == follow_to:
            raise serializers.ValidationError("You cannot follow yourself.")

        # Check if the follow relationship already exists
        if Follow.objects.filter(follow_from=follow_from, follow_to=follow_to).exists():
            raise serializers.ValidationError("You are already following this user.")
        
        return data

    def create(self, validated_data):
        follow_from = self.context['request'].user
        follow_to = validated_data['follow_to']
        follow = Follow.objects.create(follow_from=follow_from, follow_to=follow_to)
        return follow


class FollowDeleteSerializer(serializers.Serializer):
    follow_to = serializers.PrimaryKeyRelatedField(queryset=UserBase.objects.all())

    def validate(self, data):
        follow_from = self.context['request'].user
        follow_to = data['follow_to']
        # Check if the follow relationship exists
        if not Follow.objects.filter(follow_from=follow_from, follow_to=follow_to).exists():
            raise serializers.ValidationError("Follow relationship does not exist.")
        return data


    
