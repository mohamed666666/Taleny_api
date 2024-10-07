from django.db import models

# Create your models here.
from django.contrib.auth.models import (AbstractBaseUser, BaseUserManager,
                                        PermissionsMixin)

from django.db import models
class CustomAccountManager(BaseUserManager):

    def create_superuser(self, email, user_name, password, **other_fields):

        other_fields.setdefault('is_staff', True)
        other_fields.setdefault('is_superuser', True)
        other_fields.setdefault('is_active', True)

        if other_fields.get('is_staff') is not True:
            raise ValueError(
                'Superuser must be assigned to is_staff=True.')
        if other_fields.get('is_superuser') is not True:
            raise ValueError(
                'Superuser must be assigned to is_superuser=True.')

        return self.create_user(email, user_name, password, **other_fields)

    def create_user(self, email, user_name, password, **other_fields):

        if not email:
            raise ValueError(('You must provide an email address'))

        email = self.normalize_email(email)
        user = self.model(email=email, user_name=user_name,
                          **other_fields)
        user.set_password(password)
        user.save()
        return user



class UserBase(AbstractBaseUser, PermissionsMixin):

    email = models.EmailField('email address', unique=True)
    user_name = models.CharField(max_length=150, unique=True)
    full_name = models.CharField(max_length=150, blank=True)
    title = models.CharField(max_length=150, blank=True)
    about = models.TextField( 'about', max_length=500, blank=True)
    age=models.IntegerField(null=True)
    # Delivery details
    profile_image=models.ImageField(upload_to='profile_images/',default='profile_images/default.png' )
    phone_number = models.CharField(max_length=15, blank=True)
    government = models.CharField(max_length=150, blank=True)
    area = models.CharField(max_length=150, blank=True)
    # User Status
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    objects = CustomAccountManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['user_name']


