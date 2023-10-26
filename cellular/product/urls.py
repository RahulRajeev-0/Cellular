from django.urls import path
from product import views


app_name='product'

urlpatterns = [
    path('shoping_page/',views.shoping_page,name='shoping_page'),
    path('product_details/<vuid>/',views.product_details,name='product_details'),
    path('shop_sreach/', views.shop_sreach , name='shop_sreach'),
    path('filter_by_price/', views.filter_by_price, name="filter_by_price"),
    
    
]
