from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .sms_service import SMSService
from userservice.models import UserBase
   
from .models import SMSOTP
from datetime import timedelta
from django.utils import timezone

class SendOTPView(APIView):
    def post(self, request):
        phone_number = request.data.get("phone_number")
        try:
            user = UserBase.objects.get(phone_number=phone_number)
            sms_service = SMSService()
            session_id = sms_service.send_otp(user)
            return Response({"session_id": session_id}, status=status.HTTP_200_OK)
        except UserBase.DoesNotExist:
            return Response({"error": "User not found."}, status=status.HTTP_404_NOT_FOUND)
        
     

class VerifyOTPView(APIView):
    def post(self, request):
        phone_number = request.data.get("phone_number")
        otp = request.data.get("otp")
        session_id = request.data.get("session_id")
        
        try:
            sms_otp = SMSOTP.objects.get(user__phone_number=phone_number, session_id=session_id)
            
            # Check if OTP matches and is within valid timeframe
            if sms_otp.otp == otp and timezone.now() - sms_otp.created_at < timedelta(minutes=5):
                sms_otp.is_verified = True
                sms_otp.save()
                return Response({"message": "OTP verified successfully."}, status=status.HTTP_200_OK)
            else:
                return Response({"error": "Invalid or expired OTP."}, status=status.HTTP_400_BAD_REQUEST)

        except SMSOTP.DoesNotExist:
            return Response({"error": "Invalid session or user."}, status=status.HTTP_404_NOT_FOUND)