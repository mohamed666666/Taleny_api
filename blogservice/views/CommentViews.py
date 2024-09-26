from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from django.shortcuts import get_object_or_404
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.permissions import IsAuthenticated 

from ..models.Post import Post 
from ..models.Comment import Comment

from ..Serializers.CommentSerializer import CommentSerializer


class CommentRetrieveByIdView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, comment_id):
        try:
            comment = Comment.objects.get(id=comment_id)
        except Comment.DoesNotExist:
            return Response({"detail": "Comment not found."}, status=status.HTTP_404_NOT_FOUND)

        serializer = CommentSerializer(comment)
        return Response(serializer.data, status=status.HTTP_200_OK)


# Retrieve comments by post ID
class CommentRetrieveByPostIdView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, post_id):
        try:
            post = Post.objects.get(id=post_id)
        except Post.DoesNotExist:
            return Response({"detail": "Post not found."}, status=status.HTTP_404_NOT_FOUND)

        comments = Comment.objects.filter(on_post=post)
        serializer = CommentSerializer(comments, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


# Create a new comment
class CommentCreateView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        content = request.data.get('content')
        post_id = request.data.get('post_id')

        try:
            post = Post.objects.get(id=post_id)
        except Post.DoesNotExist:
            return Response({"detail": "Post not found."}, status=status.HTTP_404_NOT_FOUND)

        comment = Comment.objects.create(content=content, created_by=request.user, on_post=post)
        serializer = CommentSerializer(comment)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


# Update a comment by comment ID
class CommentUpdateView(APIView):
    permission_classes = [IsAuthenticated]

    def put(self, request, comment_id):
        try:
            comment = Comment.objects.get(id=comment_id)
        except Comment.DoesNotExist:
            return Response({"detail": "Comment not found."}, status=status.HTTP_404_NOT_FOUND)

        if comment.created_by != request.user:
            return Response({"detail": "You are not authorized to update this comment."}, status=status.HTTP_403_FORBIDDEN)

        comment.content = request.data.get('content', comment.content)
        comment.save()
        serializer = CommentSerializer(comment)
        return Response(serializer.data, status=status.HTTP_200_OK)


# Delete a comment by comment ID
class CommentDeleteView(APIView):
    permission_classes = [IsAuthenticated]

    def delete(self, request, comment_id):
        try:
            comment = Comment.objects.get(id=comment_id)
        except Comment.DoesNotExist:
            return Response({"detail": "Comment not found."}, status=status.HTTP_404_NOT_FOUND)

        if comment.created_by != request.user:
            return Response({"detail": "You are not authorized to delete this comment."}, status=status.HTTP_403_FORBIDDEN)

        comment.delete()
        return Response({"detail": "Comment deleted successfully."}, status=status.HTTP_204_NO_CONTENT)