from rest_framework.permissions import IsAuthenticated ,AllowAny
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from ..serialzers.BaseUserSerlaizer import UserSerializer
from ..models.Baseuser import UserBase

class UserProflieByid(APIView):
    permission_classes = [IsAuthenticated]  

    def get(self, request, user_id):
        try:
            user = UserBase.objects.get(id=user_id)
            serializer = UserSerializer(user)
            return Response(serializer.data)
        except UserBase.DoesNotExist:
            return Response({"error": "User not found"}, status=404)
        

    