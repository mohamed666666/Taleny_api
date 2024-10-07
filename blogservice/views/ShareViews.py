from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from ..models.share import Share
from ..Serializers.ShareSerializer import ShareSerializer
from django.shortcuts import get_object_or_404
from userservice.models.Baseuser import UserBase
from rest_framework.permissions import IsAuthenticated 

class ShareListCreateAPIView(APIView):
    permission_classes = [IsAuthenticated] 
    
    def get(self, request):
        # List all shares
        shares = Share.objects.filter(created_by=request.user)
        serializer = ShareSerializer(shares, many=True, context={'request': request})
        return Response(serializer.data)

    def post(self, request):
        # Extract the post ID from the request data
        post_id = request.data.get('post')
        if not post_id:
            return Response({'error': 'Post ID is required'}, status=status.HTTP_400_BAD_REQUEST)

        # Pass post_id in the context so it can be used in the serializer
        serializer = ShareSerializer(data=request.data, context={'request': request, 'post_id': post_id})
        
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ShareDetailAPIView(APIView):
    permission_classes = [IsAuthenticated]
    
    def get(self, request, share_id):
        # Retrieve a single share by id
        share = get_object_or_404(Share, pk=share_id)
        serializer = ShareSerializer(share, context={'request': request})
        return Response(serializer.data)

    def delete(self, request, share_id):
        # Delete a share by id
        
        share = get_object_or_404(Share, pk=share_id)
        if share.created_by!=request.user:
            return Response({'details':"U can not delete this share"}, status=status.HTTP_400_BAD_REQUEST)
        share.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    
    

class ShareListOfUserByUsernameView(APIView):
    permission_classes = [IsAuthenticated]
    
    def get(self, request , user_name):
        user=UserBase.objects.get(user_name=user_name)
        # List all shares
        shares = Share.objects.filter(created_by=user)
        serializer = ShareSerializer(shares, many=True, context={'request': request})
        return Response(serializer.data)