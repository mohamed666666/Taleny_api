from rest_framework.permissions import IsAuthenticated ,AllowAny
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status


class CurrentUserProflie(APIView):
    permission_classes = [IsAuthenticated]  
    def get(request):
        
        return Response({'ok':55})
        
        


class UserProflieByid(APIView):
    permission_classes = [IsAuthenticated]  
    def get(request):
        
        return Response({'ok':55})