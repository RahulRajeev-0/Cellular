from django.urls import path,include
from account_management import views

urlpatterns = [
   
    path('',views.index,name='index'),
    path('user_login/',views.user_login,name='user_login'),
    path('user_signUp/',views.user_signUp,name='user_signUp'),
]
