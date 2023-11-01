from django.urls import path
from orders import views



app_name = 'orders'

urlpatterns = [
    path('place_order/',views.place_order, name = 'place_order'),
    path('cash_on_delivery/', views.cash_on_delivery, name='cash_on_delivery'),
    path('success/', views.success , name='success'),
    path('order_listing_user/', views.order_listing_user , name='order_listing_user'),
    path('order_details_user/<id>/', views.order_details_user , name='order_details_user'),
    path('user_order_cancel/<id>/', views.user_order_cancel, name="user_order_cancel"),
    path('user_order_return/<id>/', views.user_order_return, name="user_order_return"),

    path('sales-report/', views.sales_report, name='sales-report'),

    path('ajax_coupon/', views.ajax_coupon, name="ajax_coupon"),
]
