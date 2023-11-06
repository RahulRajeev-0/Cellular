from django.urls import path
from wallet import views

app_name = 'wallet'

urlpatterns = [
    path('apply_wallet/', views.apply_wallet, name="apply_wallet"),
    path('wallet_page/', views.wallet_page, name="wallet_page"),
]
