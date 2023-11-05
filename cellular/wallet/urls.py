from django.urls import path
from wallet import views

app_name = 'wallet'

urlpatterns = [
    path('apply_wallet/', views.apply_wallet, name="apply_wallet"),
]
