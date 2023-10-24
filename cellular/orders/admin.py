from django.contrib import admin
from orders.models import Order, OrderProduct , Payment , Coupon
# Register your models here.


admin.site.register(Order)
admin.site.register(OrderProduct)
admin.site.register(Payment)
admin.site.register(Coupon)