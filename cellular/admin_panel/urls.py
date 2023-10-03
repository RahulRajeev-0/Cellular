from django.urls import path
from admin_panel import views

app_name = 'admin_panel'

urlpatterns = [
    path('',views.admin_index,name='admin_index'),
    path('admin_login/',views.admin_login,name='admin_login'),
    path('user_listing/',views.user_listing,name='user_listing'),
    path('user_block_unblock/<int:id>',views.user_block_unblock,name='user_block_unblock'),
    path('brand_list',views.brand_list,name='brand_list'),
    path('add_brand/',views.add_brand,name='add_brand'),
    # path('edit_brand/',views.edit_brand,name='edit_brand'),
    #path('block_unblock_brand/<int:uid>',views.block_unblock_brand,name='block_unblock_brand')
    path('product_listing/',views.product_listing,name='product_listing'),
    path('add_product',views.add_product,name='add_product'),
    path('home_main_slider/',views.home_main_slider,name='home_main_slider'),
    path('delete_slide/<int:slide_id>',views.delete_slide,name='delete_slide'),
    path('sample_check/',views.sample_check,name='sample_check'),
    path('ad_log_out/',views.ad_log_out,name='ad_log_out'),
]
