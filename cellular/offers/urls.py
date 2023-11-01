from django.urls import path
from offers import views

app_name = 'offers'

urlpatterns = [
    path('offers/', views.offers, name="offers"),
]
