from django.urls import path
from orders import views



app_name = 'orders'

urlpatterns = [
    path('place_order/',views.place_order, name = 'place_order'),
    path('cash_on_delivery/', views.cash_on_delivery, name='cash_on_delivery'),
    path('success/', views.success , name='success')
]
