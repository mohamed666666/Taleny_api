from ..models.Post import Post ,Post_attachement
from rest_framework import serializers
from userservice.serialzers.BaseUserSerlaizer import UserSerializer
from userservice.models.follow import Follow
from ..models.Like import Like
from ..models.Comment import Comment
from ..models.share import Share
from django.contrib.contenttypes.models import ContentType


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
    
    def to_representation(self, instance):
        """
        Customize the serialized output.
        """
        representation = super().to_representation(instance)
        # Add attachments in the representation
        attachments = Post_attachement.objects.filter(post=instance)
        representation['attachments'] = [
            {
                'id': attachment.id,
                'file_url': attachment.attachment_file.url
            }
            for attachment in attachments
        ]
        return representation






    

class RetrivePostSerializer(serializers.ModelSerializer):
    created_by = UserSerializer()  # Using the existing UserSerializer for user details
    attachments = PostAttachmentSerializer(many=True, read_only=True, source='post')  # Nested serializer for attachments
    likes_count=serializers.SerializerMethodField()
    comments_count=serializers.SerializerMethodField()
    following=serializers.SerializerMethodField()
    shares_count=serializers.SerializerMethodField()
    liked=serializers.SerializerMethodField()
    class Meta:
        model = Post
        fields = ['id','created_at',  'content','created_by', 'attachments',
                  'comments_count' ,'likes_count','following','shares_count','liked']
        read_only_fields = ['id', 'created_at']
        
    def get_likes_count(self,object):
        
        return(Like.objects.filter(content_type=ContentType.objects.get(model='post') ,object_id=object.id).count())
        
    
    def get_comments_count(self,object):
        return(Comment.objects.filter(on_post=object).count())
    
   
    def get_following(self,object):
        user = self.context.get('request_user')
        
        if user:
            try:
                # Check if there's a follow relationship between request.user and the post creator
                follow = Follow.objects.get(follow_from=user, follow_to=object.created_by)
                
                # Return status based on the follow status
                if follow.status:
                    return "following"
                else:
                    return "pending"
            except Follow.DoesNotExist:
                return "notfollowing"
        return None
    
    def get_shares_count(self,object):
        return(Share.objects.filter(post=object).count())
    
    def get_liked(self,object):
        user = self.context.get('request_user')
        return Like.objects.filter(content_type=ContentType.objects.get(model='post'), created_by=user,object_id=object.id).exists()
        