from django.contrib.auth.tokens import PasswordResetTokenGenerator
from six import text_type
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes,force_str
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import send_mail
from userservice.models.Baseuser  import UserBase



        
class EmailSender:
    def send_email(self,subject,message,email,from_mail):
        send_mail(
            subject,
            message,
            from_mail,
            [email],
            fail_silently=False,
        )

class AccountActivationToken(PasswordResetTokenGenerator):
    def _make_hash_value(self, user, timestamp):
        return (text_type(user.pk)+text_type(timestamp)+text_type(user.is_active))

account_activation_token=AccountActivationToken()

        
class EmailVerification:
    
    def VarifieAcount(self, User, request):
        current_site = get_current_site(request)
        subject = 'Activate your Account'
        message = render_to_string('user/account_activation_email.html', {
            'user': User,
            'domain': current_site.domain,
            'uid': urlsafe_base64_encode(force_bytes(User.pk)),
            'token': account_activation_token.make_token(User),
        })
        
        email_sender = EmailSender()
        from_email = 'your-email@example.com'  # Set your "from" email address here
        email_sender.send_email(subject, message, User.email, from_email)
    



