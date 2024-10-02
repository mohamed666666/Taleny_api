from django.shortcuts import render
from firebase_admin.messaging import Message, Notification
from fcm_django.models import FCMDevice
# Create your views here.
#Notification(title="title", body="body", image="image_url") send_notfifcation  take it as parameter
def SendNotifications(title,body,user):
    devices = FCMDevice.objects.fliter(user=user)
    message=  Message(notification=Notification(title=title, body=body))
    devices.send_message(message)
    
    