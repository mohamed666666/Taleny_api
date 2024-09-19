from rest_framework import generics ,status
from ..serialzers.TalenteeSerializer import TalenteeRegistrationSerializer
from rest_framework.permissions import IsAuthenticated ,AllowAny
from rest_framework.parsers import MultiPartParser, FormParser

class TalenteeRegistrationView(generics.CreateAPIView):
    serializer_class = TalenteeRegistrationSerializer
    permission_classes = [AllowAny]
    parser_classes = [MultiPartParser, FormParser]
