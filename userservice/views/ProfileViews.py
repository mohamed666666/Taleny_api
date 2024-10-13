from rest_framework.permissions import IsAuthenticated ,AllowAny
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from ..serialzers.ProfileSerailizer import ProfileUserUpdateSerializer
from ..serialzers.ProfileSerailizer import ProfileSerializer
from ..models.Baseuser import UserBase
from ..models.follow import Follow
from django.db.models import Count
from django.db.models import Sum,Q,F
from django.contrib.contenttypes.models import ContentType
from blogservice.models.Post import Post
from blogservice.models.Like import Like
from django.shortcuts import get_object_or_404
from rest_framework.parsers import MultiPartParser, FormParser

class UpdateUserProflie(APIView):
    permission_classes = [IsAuthenticated]  
    parser_classes = [MultiPartParser, FormParser]

    def put(self, request ,user_name):
        requesteduser = get_object_or_404(UserBase,pk=request.user.id)
        user_by_username=UserBase.objects.filter(user_name=user_name).first()
        if (requesteduser!=user_by_username):
            return Response({'details':'must update your profile'}, status=405)
            
        serializer = ProfileUserUpdateSerializer(user_by_username, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CurrentUserProflie(APIView):
    permission_classes = [IsAuthenticated]  

    def get(self, request):
        try:
            serializer = ProfileSerializer(request.user)
            return Response(serializer.data)
        except UserBase.DoesNotExist:
            return Response({"error": "User not found"}, status=404)
        
    
 
class UserProflieByid(APIView):
    permission_classes = [IsAuthenticated]  

    def get(self, request, user_name):
        try:
            user = UserBase.objects.get(user_name=user_name)
            serializer = ProfileSerializer(user,context={'request_user':request.user})
            return Response(serializer.data)
        except UserBase.DoesNotExist:
            return Response({"error": "User not found"}, status=404)
        
class UserProflieStastics(APIView):
    permission_classes = [IsAuthenticated]  

    def get(self, request, user_name):
        try:
            user = UserBase.objects.get(user_name=user_name)
            return Response(StatsticsResponseData(user=user),status=200)
        except UserBase.DoesNotExist:
            return Response({"error": "User not found"}, status=404)
        
        

class CurrentUserProflieStastics(APIView):
    permission_classes = [IsAuthenticated]  

    def get(self, request):
        try:
            user = UserBase.objects.get(id=request.user.id)
        except UserBase.DoesNotExist:
            return Response({"error": "User not found"}, status=404)
        return Response(StatsticsResponseData(user=user), status=200)
        

def StatsticsResponseData(user):
    post_content_type = ContentType.objects.get_for_model(Post)
    user_posts = Post.objects.filter(created_by_id=user.id)
    
    return {
            "followers": Follow.objects.filter(follow_to=user,status=True).count(),
            "followings": Follow.objects.filter(follow_from=user,status=True).count(),
            "posts": Post.objects.filter(created_by=user).count(),
            "requests": Follow.objects.filter(follow_to=user,status=False).count(),
            'likes':Like.objects.filter(
        content_type=post_content_type,  # Only likes for posts
        object_id__in=user_posts.values_list('id', flat=True)  # Match post IDs
    ).count()
        }