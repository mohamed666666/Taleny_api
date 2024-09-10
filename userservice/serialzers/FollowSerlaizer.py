from rest_framework import serializers
from ..models.follow import Follow
from ..models.Baseuser import UserBase

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
        follow = Follow.objects.create(follow_from=follow_from, follow_to=follow_to, status=True)
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
    
    
