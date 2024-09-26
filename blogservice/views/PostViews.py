from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from django.shortcuts import get_object_or_404
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.permissions import IsAuthenticated 

from ..models.Post import Post ,Post_attachement
from ..models.Like import Like
from ..models.Comment import Comment
from django.contrib.contenttypes.models import ContentType
from ..Serializers.LikeSerializer import LikeSerializer

from ..Serializers.PostSerializer import PostSerializer ,RetrivePostSerializer
from ..Serializers.PostSerializer import PostAttachmentSerializer
from userservice.serialzers.BaseUserSerlaizer import UserSerializer


class GetAllPostsView(APIView):
    permission_classes = [IsAuthenticated] 
    
    


class CreatePostView(APIView):
    permission_classes = [IsAuthenticated]  # Ensure the user is authenticated
    parser_classes = [MultiPartParser, FormParser]  # Accept form-data and file uploads

    def post(self, request, *args, **kwargs): 
        serializer = PostSerializer(data=request.data,partial=True)
        
        if serializer.is_valid():
            # Set the logged-in user as the post creator
            serializer.save(created_by=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
        
class RetrivePost_by_id(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request, post_id):
        # Fetch the post object
        post = get_object_or_404(Post, id=post_id)
        # Fetch likes related to the post
        likes = Like.objects.filter(
            content_type=ContentType.objects.get_for_model(Post), 
            object_id=post.id
        )
        print(len(likes))
        
        # Serialize the post
        post_serializer = RetrivePostSerializer(post)
        # Add likes to the serialized data
        data = post_serializer.data
        data['likes_on_post'] = LikeSerializer(likes, many=True).data
        return Response(data, status=200)
        
        
        
class UpdatePostView(APIView):
    permission_classes = [IsAuthenticated]
    parser_classes = [MultiPartParser, FormParser]
    
    def put(self, request, post_id):
        post = get_object_or_404(Post, id=post_id)
        
        # Make sure to allow partial updates
        serializer = PostSerializer(post, data=request.data, partial=True)

        if serializer.is_valid():
            serializer.update(post, validated_data=serializer.validated_data)
            return Response(serializer.data, status=200)
        
        return Response(serializer.errors, status=400)





class DeletePost_by_id(APIView):
    permission_classes = [IsAuthenticated]
    
    def delete(self, request, post_id):
        post = get_object_or_404(Post, id=post_id)
        attachments = Post_attachement.objects.filter(post=post)
        # Serialize the attachments
        post.delete()
        attachments.delete()
        
        return Response( status=200)
        