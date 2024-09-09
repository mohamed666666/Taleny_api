from rest_framework import serializers
from ..models.follow import Follow

class FollowSerlaizer(serializers.ModelSerializer):
    
    class Meta:
        model=Follow
        