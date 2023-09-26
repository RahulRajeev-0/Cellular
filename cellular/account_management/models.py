from django.db import models
from django.contrib.auth.models import AbstractBaseUser , BaseUserManager ,PermissionsMixin
from django.utils import timezone


#custom manager for Account model
class CustomAccountManager(BaseUserManager):

    def create_superuser(self,user_name,email,phone_number,password,**other_fields):
        other_fields.setdefault('is_active',True)
        other_fields.setdefault('is_staff',True)
        other_fields.setdefault('is_superuser',True)

        if other_fields.get('is_staff') is not True:
            raise ValueError(
                'Superuser must be assigned is_staff=True'
            )
        if other_fields.get('is_superuser') is not True:
            raise ValueError(
                'Superuser must be assigned is_superuser=True'
            )
        if other_fields.get('is_active') is not True:
            raise ValueError(
                'Superuser must be assigned is_active=True'
            )
        return self.create_user(user_name,email,phone_number,password,**other_fields)
    
    def create_user(self,user_name,email,phone_number,password,**other_fields):
        email=self.normalize_email(email)
        other_fields.setdefault('is_active',True)
        user=self.model(user_name=user_name,email=email,phone_number=phone_number,**other_fields)
        user.set_password(password)
        user.save()
        return user














# Create your models here.
class Account(AbstractBaseUser,PermissionsMixin):
    user_name           =models.CharField(max_length=50,null=False)
    email               =models.EmailField(unique=True)
    phone_number        =models.CharField(max_length=12)

    #required field 
    date_joined         =models.DateTimeField(auto_now_add=True)
    is_admin            =models.BooleanField(default=False)
    is_staff            =models.BooleanField(default=False)
    is_superuser        =models.BooleanField(default=False)
    is_active           =models.BooleanField(default=True)

    objects=CustomAccountManager()
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['user_name','phone_number']

    def __str__(self):
        return self.email

