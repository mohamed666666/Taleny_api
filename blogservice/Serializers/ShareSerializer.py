from .PostSerializer import RetrivePostSerializer
from rest_framework import serializers
from ..models.share import Share 
from userservice.serialzers.BaseUserSerlaizer import UserSerializer
from ..models.Post import Post


class ShareSerializer(serializers.ModelSerializer):
    post = RetrivePostSerializer(read_only=True)  # Embedding RetrivePostSerializer for the post field
    created_by=UserSerializer(read_only=True)
    class Meta:
        model = Share
        fields = ['id', 'created_at', 'created_by', 'post']
        read_only_fields = ['id', 'created_at', 'created_by']

    def create(self, validated_data):
        request = self.context.get('request')
        post_id = self.context.get('post_id')

        # Fetch the Post instance using the post_id
        post = Post.objects.get(id=post_id)

        validated_data['created_by'] = request.user
        validated_data['post'] = post
        return super().create(validated_data)