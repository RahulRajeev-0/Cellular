from django.urls import path,include
from account_management import views


app_name = 'account_management'
urlpatterns = [
    
   
    path('',views.index,name='index'),
    path('user_login/',views.user_login,name='user_login'),
    path('user_signUp/',views.user_signUp,name='user_signUp'),
    path('otp_verification/',views.otp_verification,name='otp_verification'),
    path('otp_generation/',views.otp_generation,name='otp_generation'),
    path('logout_user/',views.logout_user,name='logout_user'),
    path('forgot_pass_email/',views.forgot_pass_email,name='forgot_pass_email'),
    path('resetpassword_valid/<uidb64>/<token>',views.resetpassword_valid,name='resetpassword_valid'),
    path('reset_password/',views.reset_password,name='reset_password')

]
