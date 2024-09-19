from ..models.Post import Post ,Post_attachement
from rest_framework import serializers

class PostAttachmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post_attachement
        fields = ['id', 'post', 'created_at', 'updated_at']

    
class PostSerializer(serializers.ModelSerializer):
    attachments = PostAttachmentSerializer(many=True, required=False, write_only=True)

    class Meta:
        model = Post
        fields = ['id', 'content',  'attachments']

    def create(self, validated_data):
        attachments_data = validated_data.pop('attachments', [])
        print(attachment_data)
        post = Post.objects.create(**validated_data)
        for attachment_data in attachments_data:
            Post_attachement.objects.create(post=post, **attachment_data)
        return post