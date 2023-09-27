from django.urls import path
from product import views


app_name='product'

urlpatterns = [
    path('shoping_page/',views.shoping_page,name='shoping_page'),
    path('product_details/<str:slug>',views.product_details,name='product_details'),
    
]
