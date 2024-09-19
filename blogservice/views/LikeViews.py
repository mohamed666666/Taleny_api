from rest_framework import status, generics
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.contrib.contenttypes.models import ContentType
from ..Serializers.LikeSerializer import LikeSerializer
from ..models import Like

class LikeCreateView(generics.CreateAPIView):
    serializer_class = LikeSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)

class LikeDeleteView(generics.DestroyAPIView):
    permission_classes = [IsAuthenticated]

    def get_object(self):
        # Extract content_type and object_id from query params or request body
        content_type = self.request.query_params.get('content_type')
        object_id = self.request.query_params.get('object_id')

        if not content_type or not object_id:
            raise serializers.ValidationError("content_type and object_id must be provided.")
        
        # Fetch the content type model and like instance
        content_type_model = ContentType.objects.get(model=content_type)
        like = Like.objects.filter(
            created_by=self.request.user,
            content_type=content_type_model,
            object_id=object_id
        ).first()

        if like is None:
            raise serializers.ValidationError("Like not found.")
        
        return like

