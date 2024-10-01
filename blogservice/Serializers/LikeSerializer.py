from rest_framework import serializers
from django.contrib.contenttypes.models import ContentType
from ..models.Like import Like




class LikeSerializer(serializers.ModelSerializer):
    # Fields to accept the model type (Post/Comment) and the specific object (ID)
    content_type = serializers.SlugRelatedField(
        slug_field='model', queryset=ContentType.objects.all()
    )
    object_id = serializers.IntegerField()

    class Meta:
        model = Like
        fields = ['created_at', 'content_type', 'object_id']

    def validate(self, data):
        user = self.context['request'].user
        model = data['content_type'].model_class()

        # Ensure the object being liked exists
        try:
            content_object = model.objects.get(id=data['object_id'])
        except model.DoesNotExist:
            raise serializers.ValidationError(f"The {model.__name__} you're trying to like does not exist.")
        
        # Check if the like already exists
        if Like.objects.filter(
            created_by=user,
            content_type=data['content_type'],
            object_id=data['object_id']
        ).exists():
            raise serializers.ValidationError("You have already liked this item.")

        return data

    def create(self, validated_data):
        validated_data['created_by'] = self.context['request'].user
        return super().create(validated_data)