from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.utils.http import urlsafe_base64_decode
from django.utils.encoding import force_str
from userservice.models.Baseuser import UserBase
from .EmailVerification import account_activation_token


class AccountActivator:
    def account_activate(request, uidb64, token):
        try:
            uid = force_str(urlsafe_base64_decode(uidb64))
            user = UserBase.objects.get(pk=uid)
        except (TypeError, ValueError, OverflowError, UserBase.DoesNotExist):
            user = None
        
        if user is not None and account_activation_token.check_token(user, token):
            user.is_active = True
            user.save()
            return HttpResponse("Your account has been activated successfully.")
        else:
            return HttpResponse("Activation link is invalid!")