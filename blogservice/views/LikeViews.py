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


class LikeCreateAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        serializer = LikeSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            like = serializer.save()
            return Response(
                {"message": "Like created successfully", "like": LikeSerializer(like).data},
                status=status.HTTP_201_CREATED
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class LikeDeleteAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def delete(self, request, *args, **kwargs):
        content_type = request.data.get('content_type')
        object_id = request.data.get('object_id')
        
        if not content_type or not object_id:
            return Response(
                {"error": "Both content_type and object_id are required."},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        try:
            # Retrieve the ContentType for the given model
            content_type_obj = ContentType.objects.get(model=content_type)
            model = content_type_obj.model_class()

            # Ensure the object being unliked exists
            model.objects.get(id=object_id)
        except ContentType.DoesNotExist:
            return Response(
                {"error": "Invalid content type."},
                status=status.HTTP_400_BAD_REQUEST
            )
        except model.DoesNotExist:
            return Response(
                {"error": f"The {content_type} object does not exist."},
                status=status.HTTP_404_NOT_FOUND
            )
        
        # Check if the like exists
        try:
            like = Like.objects.get(
                created_by=request.user,
                content_type=content_type_obj,
                object_id=object_id
            )
        except Like.DoesNotExist:
            return Response(
                {"error": "Like not found or you did not like this item."},
                status=status.HTTP_404_NOT_FOUND
            )
        
        # Delete the like
        like.delete()
        return Response(
            {"message": "Like deleted successfully."},
            status=status.HTTP_204_NO_CONTENT
        )


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