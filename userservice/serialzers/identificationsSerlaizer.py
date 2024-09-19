from rest_framework import serializers
from ..models.identfications import Identifications


class IdentifcationsSerlaizer(serializers.ModelSerializer):
    
    class Meta:
        model=Identifications
        fields = ['url']