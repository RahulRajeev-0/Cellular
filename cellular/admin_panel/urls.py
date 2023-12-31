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
    path('product_edit/<uid>', views.product_edit, name='product_edit'),
    path('ram_list/', views.ram_list, name ='ram_list'),
    path('ram_edit/<uid>', views.ram_edit, name = 'ram_edit'),
    path('color_list/', views.color_list, name ='color_list'),
    path('color_edit/<uid>', views.color_edit, name = 'color_edit'),
    path('product_varients_add/', views.product_varients_add, name='product_varients_add'),
    path('product_varients_listing/', views.product_varients_listing, name='product_varients_listing'),
    path('product_varients_edit/<uid>', views.product_varients_edit, name='product_varients_edit'),
    path('product_images/', views.product_images, name='product_images'),
    path("product_img_add/", views.product_img_add , name="product_img_add"),
    path('product_img_delete/<uid>', views.product_img_delete , name='product_img_delete'),


    
    # -----------------------Home page heading and banner rendering -------------------

    path('home_main_slider/', views.home_main_slider, name='home_main_slider'),
    path('delete_slide/<int:slide_id>', views.delete_slide, name='delete_slide'),
    path('Home_sub_banner/', views.Home_sub_banner, name='Home_sub_banner'),
    path('delete_sub_banner/<int:id>', views.delete_sub_banner, name='delete_sub_banner'),
   

    # ------------------------------ orders ----------------------------------------------------

    path('order_listing/', views.order_listing, name="order_listing"),
    path('order_details/<id>/', views.order_details , name='order_details'),\
    path('admin_order_cancel/<id>/', views.admin_order_cancel, name='admin_order_cancel'),
    path('admin_order_accept/<id>/', views.admin_order_accept, name='admin_order_accept'),
    path('admin_order_complete/<id>/', views.admin_order_complete, name='admin_order_complete'),
    path('admin_order_returned/<id>/', views.admin_order_returned, name='admin_order_returned'),



    # ----------------------------------- coupons --------------------------------------------
    path('coupons_listing/', views.coupons_listing , name="coupons_listing"),
    path('coupons_edit/<id>', views.coupons_edit , name="coupons_edit"),


    # ----------------------------------product offers ----------------------------------------
    path('product_offers/', views.product_offers, name='product_offers'),
    path('add_product_offers/', views.add_product_offers, name='add_product_offers'),
    path('edit_product_offer/<int:id>/', views.edit_product_offer, name="edit_product_offer"),
    path('delete_product_offer/<int:id>/', views.delete_product_offer, name='delete_product_offer'),

    # --------------------------- Category offers --------------------------------------------------

    path('category_offers/', views.category_offers, name="category_offers"),
    path('add_category_offers/', views.add_category_offers, name='add_category_offers'),
    path('edit_category_offer/<int:id>/', views.edit_category_offer, name='edit_category_offer'),
    path('delete_category_offer/<int:id>/', views.delete_category_offer, name="delete_category_offer"),

]
