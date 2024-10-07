from rest_framework.permissions import IsAuthenticated ,AllowAny
from rest_framework.views import APIView
from rest_framework.response import Response
from ..serialzers.FollowSerlaizer import( FollowCreateSerializer,FollowDeleteSerializer 
                                ,FollowToCurrentUserSerlaizer ,FollowReqesutsAcceptSerializer)
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
    
    

class FollowersToCurrentUserView(APIView):
    def get(self, request):
        # Check if the follow relationship exists
        follows=Follow.objects.filter(follow_to=request.user ,status=True)
        selaizer=FollowToCurrentUserSerlaizer(follows,many=True)
        return Response(selaizer.data ,status=200)
    

class usersFollowedByCurrentUserView(APIView):
    def get(self, request):
        # Check if the follow relationship exists
        follows=Follow.objects.filter(follow_from=request.user ,status=True)
        selaizer=FollowToCurrentUserSerlaizer(follows,many=True)
        return Response(selaizer.data ,status=200)


class FollowerRequestsToCurrentUserView(APIView):
    def get(self, request):
        # Check if the follow relationship exists
        follows=Follow.objects.filter(follow_to=request.user ,status=False)
        selaizer=FollowToCurrentUserSerlaizer(follows,many=True)
        return Response(selaizer.data ,status=200)
    



class AcceptFollowView(APIView):
    def post(self, request):
        try:
            follow_id = request.data.get('follow_id')  # Get the follow ID from the JSON payload
            follow = Follow.objects.get(id=follow_id)  # Retrieve the follow request
            
            # Check if the current user is the follow_to user
            if follow.follow_to != request.user:
                return Response({"error": "You are not authorized to accept this follow request."}, status=status.HTTP_403_FORBIDDEN)
            
            # Use the serializer to update the status
            serializer = FollowReqesutsAcceptSerializer(follow, data=request.data, context={'request': request}, partial=True)
            
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        except Follow.DoesNotExist:
            return Response({"error": "Follow request not found"}, status=status.HTTP_404_NOT_FOUND)

    

