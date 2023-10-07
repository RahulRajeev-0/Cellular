from django.db import models
from base.models import BaseModel
from django.utils import timezone
from django.utils.text import slugify



# ----------------- create your models here -------------------------------


# ------------------------- model for adding brand --------------

class Brand( models.Model ):
    brand_name          = models.CharField(max_length = 100)
    slug                = models.SlugField(unique = True, null = True ,blank = True)
    is_active           = models.BooleanField(default = True)
    
    def save(self, *args, **kwargs):
        self.slug = slugify(self.brand_name)
        super(Brand, self).save(*args , **kwargs)

    def __str__(self):
        return self.brand_name 





# ----------- model for add different color varients --------------------

class ColorVarient(BaseModel):
    color_name = models.CharField(max_length = 100,unique=True,null=False)
    

    def __str__(self):
        return self.color_name



# --------------- model for add different ram varients -------------

class RamVarient(BaseModel):
    ram_no = models.CharField(max_length=30,unique=True)


    def __str__(self):
        return self.ram_no





# ---------------- model for storing the product details --------------------

class Product(BaseModel):
    product_name        = models.CharField(max_length = 100)
    slug                = models.SlugField(unique = True, null = True ,blank = True)
    brand               = models.ForeignKey(Brand, on_delete = models.CASCADE, related_name = 'products')
    product_description = models.TextField()
    


    def save(self, *args, **kwargs):
        self.slug = slugify(self.product_name)
        super(Product, self).save(*args , **kwargs)

    def __str__(self):
        return self.product_name 





# ----------- model for storing the different types of varients of the different products --------

class Product_varients(BaseModel):
    product = models.ForeignKey(Product, on_delete = models.CASCADE)
    product_heading = models.TextField()
    model_id = models.TextField(max_length=30,unique=True)
    ram = models.ForeignKey(RamVarient, on_delete = models.CASCADE)
    color = models.ForeignKey(ColorVarient, on_delete = models.CASCADE )
    product_detailed_description = models.TextField()
    price = models.DecimalField(max_digits = 9, decimal_places = 2)
    stock_qty = models.IntegerField()
    is_active = models.BooleanField(default = True)
    thambnail = models.ImageField(upload_to = 'thambnail')

    def __str__(self):
        return f"{self.product.product_name} - {self.model_id}"












#  --------------model for storing the images of different varients --------------------

class ProductImage(BaseModel):
    product             = models.ForeignKey(Product_varients, on_delete = models.CASCADE , related_name= 'product_images')
    image               = models.ImageField(upload_to = 'product')


