from rest_framework_simplejwt.views import TokenObtainPairView
from ..serialzers.BaseUserSerlaizer import CustomTokenObtainPairSerializer


class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer
    
    