from django.urls import path
from orders import views



app_name = 'orders'

urlpatterns = [
    path('place_order/',views.place_order, name = 'place_order'),
]
