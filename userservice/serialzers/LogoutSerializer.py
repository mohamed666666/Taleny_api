
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from ..models.talent import Talentee
from ..models.investgator import Investgator
from rest_framework import serializers


class LogoutSerializer(serializers.Serializer):
    pass