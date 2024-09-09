from rest_framework import serializers
from ..models.talent import Talent


class TalentSerlaizer(serializers.ModelSerializer):

    class Meta:
        model=Talent
        fields=['id','name']