from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from django.shortcuts import get_object_or_404
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.permissions import IsAuthenticated 
from ..models.Post import Post ,Post_attachement
from ..Serializers.PostSerializer import PostSerializer ,RetrivePostSerializer
from rest_framework.pagination import PageNumberPagination
from userservice.models.Baseuser import UserBase

class GetAllPostsView(APIView):
    permission_classes = [IsAuthenticated] 

    def get(self, request):
        posts = Post.objects.all().order_by('-created_at')

        # Apply pagination
        paginator = PageNumberPagination()
        paginator.page_size = 3  # You can also set this dynamically
        paginated_posts = paginator.paginate_queryset(posts, request)

        serializer = RetrivePostSerializer(paginated_posts, many=True)
        return paginator.get_paginated_response(serializer.data)
    


class CreatePostView(APIView):
    permission_classes = [IsAuthenticated]  # Ensure the user is authenticated
    parser_classes = [MultiPartParser, FormParser]  # Accept form-data and file uploads

    def post(self, request): 
        serializer = PostSerializer(data=request.data,partial=True)
        
        
        if serializer.is_valid():
            # Set the logged-in user as the post creator
            serializer.save(created_by=request.user)
            
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    
    
    
        
class RetrivePost_by_id(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request, post_id):
        post = get_object_or_404(Post, id=post_id)
        post_serializer = RetrivePostSerializer(post)
        return Response(post_serializer.data, status=200)
        
        
        
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
    
    



class GetPostsOfCurrentUserView(APIView):
    permission_classes = [IsAuthenticated] 

    def get(self, request):
        posts = Post.objects.filter(created_by=request.user.id)

        # Apply pagination
        paginator = PageNumberPagination()
        paginator.page_size = 3  # You can also set this dynamically
        paginated_posts = paginator.paginate_queryset(posts, request)

        serializer = RetrivePostSerializer(paginated_posts, many=True)
        return paginator.get_paginated_response(serializer.data)
    

class GetPostsOfUserByIdView(APIView):
    permission_classes = [IsAuthenticated] 

    def get(self, request,user_name):
        user=UserBase.objects.get(user_name=user_name)
        posts = Post.objects.filter(created_by=user.id)

        # Apply pagination
        paginator = PageNumberPagination()
        paginator.page_size = 3  # You can also set this dynamically
        paginated_posts = paginator.paginate_queryset(posts, request)

        serializer = RetrivePostSerializer(paginated_posts, many=True)
        return paginator.get_paginated_response(serializer.data)
    