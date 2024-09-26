from rest_framework.permissions import IsAuthenticated ,AllowAny
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from ..serialzers.BaseUserSerlaizer import UserSerializer,UserUpdateSerializer
from ..models.Baseuser import UserBase
from django.shortcuts import get_object_or_404
from rest_framework.parsers import MultiPartParser, FormParser


 
class UserProflieByid(APIView):
    permission_classes = [IsAuthenticated]  

    def get(self, request, user_id):
        try:
            user = UserBase.objects.get(id=user_id)
            serializer = UserSerializer(user)
            return Response(serializer.data)
        except UserBase.DoesNotExist:
            return Response({"error": "User not found"}, status=404)
        
        
 
class UpdateUserProflie(APIView):
    permission_classes = [IsAuthenticated]  
    parser_classes = [MultiPartParser, FormParser]

    def put(self, request):
        user = get_object_or_404(UserBase,pk=request.user.id)
        serializer = UserUpdateSerializer(user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    