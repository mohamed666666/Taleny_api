from rest_framework.permissions import IsAuthenticated ,AllowAny
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from ..serialzers.ProfileSerailizer import ProfileUserUpdateSerializer
from ..serialzers.ProfileSerailizer import ProfileSerializer
from ..models.Baseuser import UserBase
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
    
    
 
class UserProflieByid(APIView):
    permission_classes = [IsAuthenticated]  

    def get(self, request, user_name):
        try:
            user = UserBase.objects.get(user_name=user_name)
            serializer = ProfileSerializer(user)
            return Response(serializer.data)
        except UserBase.DoesNotExist:
            return Response({"error": "User not found"}, status=404)
        

class CurrentUserProflie(APIView):
    permission_classes = [IsAuthenticated]  

    def get(self, request):
        try:
            serializer = ProfileSerializer(request.user)
            return Response(serializer.data)
        except UserBase.DoesNotExist:
            return Response({"error": "User not found"}, status=404)
        
        
 
