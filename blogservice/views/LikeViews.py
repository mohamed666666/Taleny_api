from rest_framework import status, generics
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.contrib.contenttypes.models import ContentType
from ..Serializers.LikeSerializer import LikeSerializer
from ..models import Like
from rest_framework import serializers
from rest_framework.views import APIView
from ..models.Post import Post
from ..models.Comment import  Comment
from django.shortcuts import get_object_or_404



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


class GetLikesOnPost(APIView):
    permission_classes = [IsAuthenticated]
    
    def get(self,request,post_id):
        post = get_object_or_404(Post, id=post_id)
        likes=Like.objects.filter(content_type=ContentType.objects.get(model='post') ,object_id=post.id)
        serializer=LikeSerializer(likes,many=True)
        return Response(serializer.data,status=200)
    

class GetLikesOnComment(APIView):
    permission_classes = [IsAuthenticated]
    
    def get(self,request,comment_id):
        comment = get_object_or_404(Comment, id=comment_id)
        likes=Like.objects.filter(content_type=ContentType.objects.get(model='comment') ,object_id=comment.id)
        serializer=LikeSerializer(likes,many=True)
        return Response(serializer.data,status=200)