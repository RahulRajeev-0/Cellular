from django.urls import path
from cart import views


app_name='cart'

urlpatterns = [
    path('cart_page/',views.cart_page,name='cart_page'),
    
    
]
