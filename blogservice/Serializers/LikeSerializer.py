from rest_framework import serializers
from django.contrib.contenttypes.models import ContentType
from ..models.Comment import  Comment
from ..models.Like import Like
from ..models.Post import Post

class LikeSerializer(serializers.ModelSerializer):
    # Fields to accept the model type (Post/Comment) and the specific object (ID)
    content_type = serializers.SlugRelatedField(
        slug_field='model', queryset=ContentType.objects.all()
    )
    object_id = serializers.IntegerField()

    class Meta:
        model = Like
        fields = [ 'created_at', 'content_type', 'object_id']

    def validate(self, data):
        user = self.context['request'].user
        # Ensure the object being liked exists
        model = data['content_type'].model_class()
        try:
            content_object = model.objects.get(id=data['object_id'])
        except model.DoesNotExist:
            raise serializers.ValidationError(f"The {model.__name__} you're trying to like does not exist.")
        
        # Check if user already liked either the post or comment
        if isinstance(content_object, Comment):
            post = content_object.on_post
            if Like.objects.filter(created_by=user, content_type=ContentType.objects.get_for_model(Post), object_id=post.id).exists():
                raise serializers.ValidationError("You cannot like both the post and a comment on the same post.")
        elif isinstance(content_object, Post):
            comments_on_post = Comment.objects.filter(on_post=content_object)
            if Like.objects.filter(created_by=user, content_type=ContentType.objects.get_for_model(Comment), object_id__in=comments_on_post.values_list('id', flat=True)).exists():
                raise serializers.ValidationError("You cannot like both the post and a comment on the same post.")
        
        return data

    def create(self, validated_data):
        validated_data['created_by'] = self.context['request'].user
        return super().create(validated_data)