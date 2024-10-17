from django.shortcuts import render
from firebase_admin.messaging import Message, Notification

from .models import CustomDevice
# Create your views here.
#Notification(title="title", body="body", image="image_url") send_notfifcation  take it as parameter

def SendNotifications(title,body,users):
    devices = CustomDevice.objects.fliter(user__in=users)
    message=  Message(notification=Notification(title=title, body=body))
    devices.send_message(message)
    
    