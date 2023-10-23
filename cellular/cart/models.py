from django.db import models
from product.models import Product_varients
from account_management.models import Account

# Create your models here.



class Cart(models.Model):
    cart_id = models.CharField(max_length = 250, blank = True)
    date_added = models.DateField(auto_now_add = True)

    def __str__(self):
        return self.cart_id
    

class CartItem(models.Model):
    user = models.ForeignKey(Account, on_delete = models.CASCADE , null = True)
    product = models.ForeignKey(Product_varients, on_delete = models.CASCADE)
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE , null = True)
    quantity = models.IntegerField()
    is_active = models.BooleanField(default = True)


    def sub_total(self):
        return self.product.price * self.quantity

    def __str__(self) -> str:
        return self.product.product.product_name



class WishList(models.Model):
    user = models.ForeignKey(Account, on_delete = models.CASCADE, null = True)
    product = models.ForeignKey(Product_varients, on_delete = models.CASCADE , null= True)
    create_at = models.DateField(auto_now_add = True)

    def __str__(self):
        return self.user.user_name
    

    
    