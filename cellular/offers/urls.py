from django.urls import path
from offers import views

app_name = 'offers'

urlpatterns = [
    path('offers/', views.offers, name="offers"),
    path('shop_product_offer/<int:id>/', views.shop_product_offer, name='shop_product_offer'),
    path('shop_category_offer/<int:id>/', views.shop_category_offer, name='shop_category_offer'),
]
