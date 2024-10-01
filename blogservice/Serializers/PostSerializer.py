from ..models.Post import Post ,Post_attachement
from rest_framework import serializers
from userservice.serialzers.BaseUserSerlaizer import UserSerializer
from .CommentSerializer import CommentSerializer
        

class PostAttachmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post_attachement
        fields = [ 'attachment_file']


class PostSerializer(serializers.ModelSerializer):
    attachments = serializers.ListField(
        child=serializers.FileField(allow_empty_file=True), write_only=False, required=False
    )

    class Meta:
        model = Post
        fields = ['id', 'content', 'attachments']

    def create(self, validated_data):
        attachments_data = validated_data.pop('attachments', [])
        post = Post.objects.create(**validated_data)
        # Save each attachment
        for attachment in attachments_data:
            if attachment:
                Post_attachement.objects.create(post=post, attachment_file=attachment)
        return post

    def update(self, post, validated_data):
        attachments_data = validated_data.pop('attachments', [])
        
        post.content = validated_data.get('content', post.content)
        # Remove old attachments
        Post_attachement.objects.filter(post=post).delete()
        # Save each new attachment
        for attachment in attachments_data:
            if attachment:
                Post_attachement.objects.create(post=post, attachment_file=attachment)
        post.save()

        return post





    

class RetrivePostSerializer(serializers.ModelSerializer):
    created_by = UserSerializer()  # Using the existing UserSerializer for user details
    attachments = PostAttachmentSerializer(many=True, read_only=True, source='post')  # Nested serializer for attachments
    comments = CommentSerializer(many=True, read_only=True, source='on_post')  # Nested serializer for comments

    class Meta:
        model = Post
        fields = ['id','created_at',  'content','created_by', 'attachments', 'comments' ]
        read_only_fields = ['id', 'created_at']