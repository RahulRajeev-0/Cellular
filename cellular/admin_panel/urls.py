from django.urls import path
from admin_panel import views

app_name = 'admin_panel'

urlpatterns = [
    path('',views.admin_index,name='admin_index'),
    path('admin_login/',views.admin_login,name='admin_login'),
    path('user_listing/',views.user_listing,name='user_listing'),
    path('user_block_unblock/<int:id>',views.user_block_unblock,name='user_block_unblock'),
]
