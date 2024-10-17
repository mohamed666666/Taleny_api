from twilio.rest import Client
from random import randint
from django.conf import settings
from .models import SMSOTP


"""
# settings.py
TWILIO_ACCOUNT_SID = 'your_account_sid'
TWILIO_AUTH_TOKEN = 'your_auth_token'
TWILIO_PHONE_NUMBER = 'your_twilio_phone_number'
"""

class SMSService:
    def __init__(self):
        self.client = Client(settings.TWILIO_ACCOUNT_SID, settings.TWILIO_AUTH_TOKEN)

    def send_otp(self, user):
        otp = str(randint(100000, 999999))
        message = f"Your verification code is: {otp}"
        
        # Save the OTP to the database
        sms_otp = SMSOTP.objects.create(user=user, otp=otp)

        # Send the SMS
        self.client.messages.create(
            body=message,
            from_=settings.TWILIO_PHONE_NUMBER,
            to=user.phone_number
        )
        
        return sms_otp.session_id