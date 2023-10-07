from django.urls import path
from admin_panel import views

app_name = 'admin_panel'

urlpatterns = [
    # ------------------admin authentication -----------------

    path('', views.admin_index, name='admin_index'),
    path('admin_login/', views.admin_login, name='admin_login'),
    path('ad_log_out/', views.ad_log_out, name='ad_log_out'),


    # -------------------user listing and block and unblock -------------

    path('user_listing/', views.user_listing, name='user_listing'),
    path('user_block_unblock/<int:id>', views.user_block_unblock, name='user_block_unblock'),


    # ------------------------------brand ----------------------------------

    path('brand_list/', views.brand_list, name='brand_list'),
    path('add_brand/', views.add_brand, name='add_brand'),
    path('brand_edit/<int:id>', views.brand_edit, name='brand_edit'),
    path('block_unblock_brand/<int:id>', views.block_unblock_brand, name='block_unblock_brand'),





    #------------------------------product -------------------------------------

    path('product_listing/', views.product_listing, name ='product_listing'),
    path('add_product/', views.add_product, name ='add_product'),
    path('ram_list/', views.ram_list, name ='ram_list'),
    path('color_list/', views.color_list, name ='color_list'),



    # -----------------------Home page heading and banner rendering -------------------

    path('home_main_slider/', views.home_main_slider, name='home_main_slider'),
    path('delete_slide/<int:slide_id>', views.delete_slide, name='delete_slide'),
    path('Home_sub_banner/', views.Home_sub_banner, name='Home_sub_banner'),
    path('delete_sub_banner/<int:id>', views.delete_sub_banner, name='delete_sub_banner')
   
]
