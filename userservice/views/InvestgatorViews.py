
from rest_framework import generics ,status
from ..serialzers.InvestgatorSerlaizer import InvesgatorRegistrationSerializer
from rest_framework.permissions import IsAuthenticated ,AllowAny
from rest_framework.parsers import MultiPartParser, FormParser

class InvestgatorRegistrationView(generics.CreateAPIView):
    serializer_class = InvesgatorRegistrationSerializer
    permission_classes = [AllowAny]
    parser_classes = [MultiPartParser, FormParser]
    

    
