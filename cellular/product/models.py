from django.db import models
from base.models import BaseModel
from django.utils import timezone
from django.utils.text import slugify

class Brand(BaseModel):
    brand_name          =models.CharField(max_length=100)
    slug                =models.SlugField(unique=True,null=True,blank=True)
    brand_image         =models.ImageField(upload_to='logos',blank=True)
    is_active           =models.BooleanField(default=True)
    
    def save(self, *args, **kwargs):
        self.slug=slugify(self.brand_name)
        super(Brand,self).save(*args ,**kwargs)

    def __str__(self):
        return self.brand_name 


class ColorVarient(BaseModel):
    color_name=models.CharField(max_length=100)
    price      =models.IntegerField(default=0)

    def __str__(self):
        return self.color_name


class RamVarient(BaseModel):
    ram_no=models.CharField(max_length=100)
    price     =models.IntegerField(default=0)

    def __str__(self):
        return self.ram_no





class Product(BaseModel):
    product_name        =models.CharField(max_length=100)
    slug                =models.SlugField(unique=True,null=True,blank=True)
    brand               =models.ForeignKey(Brand,on_delete=models.CASCADE,related_name='products')
    price               =models.IntegerField()
    product_description =models.TextField()
    color_varient       =models.ManyToManyField(ColorVarient,blank=True)
    ram_varient         =models.ManyToManyField(RamVarient,blank=True)




    def save(self, *args, **kwargs):
        self.slug=slugify(self.product_name)
        super(Product,self).save(*args , **kwargs)

    def __str__(self):
        return self.product_name 


class ProductImage(BaseModel):
    product             =models.ForeignKey(Product, on_delete=models.CASCADE , related_name= 'product_images')
    image               =models.ImageField(upload_to='product')


