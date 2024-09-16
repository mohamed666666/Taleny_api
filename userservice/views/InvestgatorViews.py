
from rest_framework import generics ,status
from ..serialzers.InvestgatorSerlaizer import InvesgatorRegistrationSerializer
from rest_framework.permissions import IsAuthenticated ,AllowAny


class InvestgatorRegistrationView(generics.CreateAPIView):
    serializer_class = InvesgatorRegistrationSerializer
    permission_classes = [AllowAny]
    
    

    
