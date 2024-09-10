from rest_framework import serializers
from ..models.inetrsts import Interst,Intersting_in


class InterstSerlaizer(serializers.ModelSerializer):
    
    class Meta:
        model=Interst
        fields=['id','name','icon']
    
        