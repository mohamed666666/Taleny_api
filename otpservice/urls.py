from django.urls import path
from .views import AccountActivator


app_name ='otpservice'

urlpatterns = [
    path('activate/<uidb64>/<token>/', AccountActivator.account_activate, name='activate_user_account'),
]