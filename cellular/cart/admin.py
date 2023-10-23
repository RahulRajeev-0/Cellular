from django.contrib import admin

# models
from cart.models import Cart , CartItem , WishList
# Register your models here.

admin.site.register(Cart)
admin.site.register(CartItem)
admin.site.register(WishList)