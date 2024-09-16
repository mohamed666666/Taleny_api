from rest_framework.permissions import IsAuthenticated ,AllowAny
from rest_framework.views import APIView
from rest_framework.response import Response
from ..serialzers.FollowSerlaizer import FollowCreateSerializer,FollowDeleteSerializer
from rest_framework import status
from ..models.follow import Follow

class FollowCreateView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = FollowCreateSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save()  # This will call the create method of the serializer
            return Response({'message': 'Follow successful.'}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class FollowDeleteView(APIView):
    permission_classes = [IsAuthenticated]

    def delete(self, request):
        serializer = FollowDeleteSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            # If validation passes, delete the follow relationship
            follow_from = request.user
            follow_to = serializer.validated_data['follow_to']
            follow_instance = Follow.objects.get(follow_from=follow_from, follow_to=follow_to)
            follow_instance.delete()
            return Response({'message': 'Unfollow successful.'}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    

class UserFollowersView(APIView):
    def get(self, request):
        # Check if the follow relationship exists
        follows=Follow.objects.filter(follow_to=request.user)
        return Response({"following_to_this_user":follows})
    

