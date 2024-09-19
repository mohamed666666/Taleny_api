from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from ..models.Post import Post 
from ..Serializers.PostSerializer import PostSerializer
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.permissions import IsAuthenticated 


class CreatePostView(APIView):
    permission_classes = [IsAuthenticated]  # Ensure the user is authenticated
    parser_classes = [MultiPartParser, FormParser]
    
    def post(self, request, *args, **kwargs):
        serializer = PostSerializer(data=request.data)
        print(request.data)
        if serializer.is_valid():
            # Set the logged-in user as the post creator
            serializer.save(created_by=request.user)
            
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)