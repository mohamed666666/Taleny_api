from rest_framework import generics ,status
from ..serialzers.TalentSerlaizer import  TalentSerlaizer
from rest_framework.permissions import IsAuthenticated ,AllowAny
from rest_framework.views import APIView
from rest_framework.response import Response
from ..models.talent import Talent

class TalentView(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        talents=Talent.objects.all()
        data = TalentSerlaizer(talents, many=True).data
        return Response(data)
    
    
 