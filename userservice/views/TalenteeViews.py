from rest_framework import generics ,status
from ..serialzers.TalenteeSerializer import TalenteeRegistrationSerializer
from rest_framework.permissions import IsAuthenticated ,AllowAny


class TalenteeRegistrationView(generics.CreateAPIView):
    serializer_class = TalenteeRegistrationSerializer
    permission_classes = [AllowAny]
    
