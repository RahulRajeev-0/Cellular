from django.urls import path
from cart import views


app_name='cart'

urlpatterns = [
    path('cart_page/',views.cart_page,name='cart_page'),
    path('add_cart/<uuid:product_uid>/', views.add_cart , name='add_cart'),
    path('remove_cart/<uuid:product_uid>/', views.remove_cart , name='remove_cart'),
    path('remove_cart_item/<uuid:product_uid>/', views.remove_cart_item , name='remove_cart_item'),
    
    
]