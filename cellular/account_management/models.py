
# ------standard libary imports------ 
from django.db import models
from django.utils import timezone

# -------Related Third-Party Imports ------
from django.core.exceptions import ValidationError
from django.contrib.auth.models import AbstractBaseUser , BaseUserManager ,PermissionsMixin
from PIL import Image     #for maintaining aspect ratio 


import random
import string





#custom manager for Account model
class CustomAccountManager(BaseUserManager):

    def generate_referral_code(self):
        # Generate a random 6-character alphanumeric code
        return ''.join(random.choices(string.ascii_uppercase + string.digits, k=6))


    def create_superuser(self, user_name, email, phone_number, password ,**other_fields):
        other_fields.setdefault('is_active', True)
        other_fields.setdefault('is_staff', True)
        other_fields.setdefault('is_superuser', True)

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
        return self.create_user(user_name, email, phone_number, password, **other_fields)
    
    def create_user(self, user_name, email, phone_number, password, **other_fields):
        email = self.normalize_email(email)
        other_fields.setdefault('is_active', True)
        referral_code = self.generate_referral_code() 
        user=self.model(
            user_name=user_name, 
            email = email, 
            phone_number = phone_number,
            referral_code=referral_code,
            **other_fields
            )
        user.set_password(password)
        user.save()
        return user














# Create your models here.
class Account(AbstractBaseUser,PermissionsMixin):
    user_name = models.CharField(max_length = 50 , null = False)
    email = models.EmailField(unique = True)
    phone_number = models.CharField(max_length = 12)
    referral_code = models.CharField(max_length=10, unique=True, blank=True, null=True)
    #required field 
    date_joined = models.DateTimeField(auto_now_add = True)
    is_admin = models.BooleanField(default = False)
    is_staff = models.BooleanField(default = False)
    is_superuser = models.BooleanField(default = False)
    is_active = models.BooleanField(default = True)

    objects=CustomAccountManager()
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['user_name','phone_number']

    def __str__(self):
        return self.email





# user addresss book 

class userAddressBook(models.Model):
    user = models.ForeignKey(Account, on_delete = models.CASCADE, null = True)
    name = models.CharField(max_length = 30)
    phone = models.CharField(max_length = 20)
    address_line_1 = models.CharField(max_length = 50)
    address_line_2 = models.CharField(max_length = 50 , blank = True , null = True)
    country = models.CharField(max_length = 50 , null = True , blank = True )
    state = models.CharField(max_length = 50 , null = True , blank = True)
    city = models.CharField(max_length = 50 , null = True , blank = True)
    pincode = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_default = models.BooleanField(default = False)
    is_active = models.BooleanField(default = True)


    def save(self, *args, **kwargs):
        # Check the number of existing addresses for the user
        existing_addresses_count = userAddressBook.objects.filter(user=self.user).count()

        # Limit the user to create only two addresses
        if existing_addresses_count >= 2 and not self.pk:
            raise ValidationError("A user can only create two addresses.")

        if self.is_default:
            # Set is_default=False for other addresses of the same user
            userAddressBook.objects.filter(user=self.user).exclude(pk=self.pk).update(is_default=False)
        super(userAddressBook, self).save(*args, **kwargs)


    def __str__(self) -> str:
        return self.name








#------------------------------ Banner Management ---------------------------------



#model for home page main slide display contents 
class HomeMainSlide(models.Model):
    heading = models.CharField(max_length = 20, null = False)
    subheading = models.CharField(max_length = 30, null = True)
    slide_image = models.ImageField(upload_to = 'banners')

    def __str__(self):
        return self.heading
    
    # fucntion for validating the inputs of model mainly aspect ration of image
    def clean(self):
        max_width = 1920
        max_height = 1080
        aspect_ratio = max_width/max_height
        total_slides = HomeMainSlide.objects.count()


        if self.slide_image:
            image=Image.open(self.slide_image)
            img_width, img_height = image.size
            img_aspect_ratio = img_width/img_height

            if abs(img_aspect_ratio-aspect_ratio) > 1.2 and abs(img_aspect_ratio-aspect_ratio)< 1.8:
                raise ValidationError(f'The image aspect ratio must be {aspect_ratio}:1')
            
        if total_slides >= 3:
            raise ValidationError("You can only have a maximum of 3 slides in HomeMainSlide.")




class HomeSubBanner (models.Model):
    heading = models.CharField(max_length = 30, blank = False, null = False)
    sub_heading = models.CharField(max_length = 50)
    img = models.ImageField(upload_to = 'banners')

    def __str__(self):
        return self.heading
    
    def clean(self):
        max_width  = 1920
        max_height = 1080
        aspect_ratio = max_width/max_height
        total_slides = HomeSubBanner.objects.count()


        if self.img:
            image=Image.open(self.img)
            img_width,img_height = image.size
            img_aspect_ratio = img_width/img_height

            if abs(img_aspect_ratio-aspect_ratio) > 1.9 :
                raise ValidationError(f'The image aspect ratio must be {aspect_ratio}:1')
            
        if total_slides >= 2:
            raise ValidationError("You can only have a maximum of 2 slides in HomeMainSlide.")






