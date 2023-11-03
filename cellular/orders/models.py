from django.db import models
from datetime import datetime, timedelta
#from Account_management 
from account_management.models import Account ,userAddressBook 

# from Product
from product.models import Product , Product_varients
# Create your models here.

class Coupon(models.Model):
    coupon_code = models.CharField(max_length=10)
    expiration_date = models.DateField(blank=True,null=True)
    is_expired = models.BooleanField(default=False)
    discount_price = models.IntegerField(default=100)
    minimium_amount = models.IntegerField(default=5000)

    def is_valid(self):
        return not self.is_expired and self.expiration_date >= datetime.now().date()
    
    def __str__(self):
        return self.coupon_code
    

class Payment(models.Model):
    PAYMENT_STATUS_CHOICE = (
        ('PENDING', 'Pending'),
        ('FAILED', 'Failed'),
        ('SUCCESS', 'Success'),
    )
    PAYMENTT_METHOD = (
        ('COD', 'Cash on Delivery'),
        ('Razorpay', 'Razor Pay'),
    )
    user = models.ForeignKey(Account , on_delete = models.CASCADE)
    payment_id = models.CharField(max_length = 100)
    payment_order_id = models.CharField(max_length=100, null=True, blank=True)
    payment_method = models.CharField(choices=PAYMENTT_METHOD, max_length=100)

    rayzor_pay_order_id = models.CharField(max_length=100, null=True , blank=True)
    rayzor_pay_payment_id = models.CharField(max_length=100, null=True , blank=True)
    rayzor_pay_payment_signature = models.CharField(max_length=100, null=True , blank=True)
    amount_paid = models.CharField(max_length = 100)
    payment_status = models.CharField(choices=PAYMENT_STATUS_CHOICE, max_length=100,blank=True,default='PENDING')
    created_at = models.DateTimeField(auto_now_add = True)


    def __str__(self) -> str:
        return self.payment_order_id



class Order(models.Model):
    STATUS = ( 
    ('New' , 'New'),
    ('Accepted', 'Accepted'),
    ('Completed', 'Completed'),
    ('Cancel', 'Cancel' ),
    ('Cancelled', 'Cancelled' ),
    ('Cancelled by Admin', 'Cancelled by Admin' ),
    ('Return', 'Return' ),
    ('Returned', 'Returned' ),
    )

    user = models.ForeignKey(Account , on_delete = models.SET_NULL , null = True)
    payment = models.ForeignKey(Payment , on_delete = models.SET_NULL , null = True)
    order_number = models.CharField(max_length = 100)
    shipping_address = models.ForeignKey(userAddressBook, on_delete=models.SET_NULL, null=True)
    order_total = models.FloatField()
    discount = models.CharField(max_length = 200, null = True, blank=True )
    tax = models.FloatField()
    status = models.CharField(max_length = 30 , choices = STATUS, default = 'New')
    ip = models.CharField(blank = True, max_length = 20)
    is_ordered = models.BooleanField(default = False)
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)

    def __str__(self) -> str:
        return self.user.user_name
    


class OrderProduct(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    payment = models.ForeignKey(Payment, on_delete=models.SET_NULL, blank=True, null=True)
    user = models.ForeignKey(Account, on_delete=models.CASCADE)
    product = models.ForeignKey(Product_varients , on_delete=models.CASCADE)
    quantity = models.IntegerField()
    product_price = models.DecimalField(max_digits=12, decimal_places=2)
    ordered = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


    def __str__(self):
        return str(self.order)






