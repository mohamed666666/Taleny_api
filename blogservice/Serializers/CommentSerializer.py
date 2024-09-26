from ..models.Post import Post ,Post_attachement
from ..models.Comment import Comment
from rest_framework import serializers
from userservice.serialzers.BaseUserSerlaizer import UserSerializer



class CommentSerializer(serializers.ModelSerializer):
    created_by = UserSerializer()

    class Meta:
        model = Comment
        fields = ['id', 'content', 'created_by', 'created_at']