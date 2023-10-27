from django.shortcuts import render,HttpResponse,redirect
from account_management.models import Account
from django.contrib.auth import authenticate,login,logout
from django.contrib import messages
from django.views.decorators.cache import cache_control
from django.shortcuts import get_object_or_404


# ------------ from app imports ----------------

# >>>>>>>>>>>>>>>>>>> models <<<<<<<<<<<<<<<<<<<<
from account_management.models import Account
from account_management.models import HomeMainSlide, HomeSubBanner
from product.models import Brand, Product, RamVarient, ColorVarient , Product_varients , ProductImage 
from categoryManagement.models import Category
from orders.models import Order , OrderProduct , Payment
from orders.models import Coupon 

# >>>>>>>>>>>>>>>>>> forms <<<<<<<<<<<<<<<<<<<<<< 
from product.forms import BrandForm,ProductForm,RamForm,ColorForm , Product_varientsForm , ProductVarientImageForm
from account_management.forms import HomeMainSliderForm, HomeSubBannerForm 

from orders.forms import CouponForm





# Create your views here.





# --------------------------------------- function for rendering admin home page  ------------------------------------
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def admin_index (request):
    if 'email' not in request.session:
        return redirect ('admin_panel:admin_login')
    return render(request,'admin_templates/admin_index.html') 





@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def admin_login(request):
    if 'email' in request.session:
        return redirect ('admin_panel:admin_index')
    if request.method=='POST':
            ademail=request.POST.get("email")
            passw=request.POST.get('password')
           
            user=authenticate(email=ademail,password=passw)
           
            if user is not None and user.is_superuser:
                request.session['email']=ademail
                login(request,user)
                return redirect('admin_panel:admin_index')
            else:
                messages.warning(request, 'Invalid.')
                return redirect ('admin_panel:admin_login')
    return render(request,'admin_templates/admin_login.html') 







# ------------------------------------------- function for user listing ------------------------------------

@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def user_listing(request):
     if 'email' not in request.session:
        return redirect ('admin_panel:admin_login')
     users=Account.objects.all()
     context={'users':users}
     return render(request,'admin_templates/user_list.html',context)




# ----------------------   fucntion for user blocking and unblocking  ----------------------------

@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def user_block_unblock(request,id):
        user=Account.objects.get(id=id)
        if user.is_active:
            user.is_active=False
            user.save()
        else:
            user.is_active=True
            user.save()
        return redirect ('admin_panel:user_listing')
 




 # ----------------------------------- fucntion for rendering the list of brand  ----------------------------

@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def brand_list(request):
     if 'email' not in request.session:
        return redirect ('admin_panel:admin_login')
     # if 'emial' not in request.session:
     #    return redirect ('admin_panel:admin_login')
     brands=Brand.objects.all()
     context={'brands':brands}
     return render(request,'admin_templates/brand/brand_list.html',context)




# ----------------------------------- function for adding brand ----------------------------

@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def add_brand(request):
     if 'email' not in request.session:
        return redirect ('admin_panel:admin_login')
     if request.method=='POST':
          form=BrandForm(request.POST)
          if form.is_valid():
               form.save()
               return redirect('admin_panel:brand_list')
     form= BrandForm
     return render(request,'admin_templates/brand/brand_add.html',{'form':form})





# ----------------------------------------- function for blocking and unblocking brand     -------------------------------------------

@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def block_unblock_brand(request,id):
     brand=Brand.objects.get(id=id)
     if brand.is_active:
          brand.is_active=False
          brand.save()
     else:
          brand.is_active=True
          brand.save()

     return redirect('admin_panel:brand_list')





# ------------------------   function for editing brand -----------------------------------------------

def brand_edit(request,id):
     if 'email' not  in request.session:
        return redirect ('admin_panel:admin_login')
     brand = get_object_or_404(Brand, id=id)
    
     if request.method == 'POST':
        form = BrandForm(request.POST, instance=brand)
        if form.is_valid():
            form.save()
            return redirect('admin_panel:brand_list')
     else:
        form = BrandForm(instance=brand)

     return render(request, 'admin_templates/brand/brand_edit.html', {'form': form, 'brand': brand})
     





# -------------------------------------- function for product list --------------------------------

@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def product_listing(request):
     if 'email' not in request.session:
        return redirect ('admin_panel:admin_login')
     products=Product.objects.all()
     context={'products':products}
     return render(request,'admin_templates/product/product_list.html',context)




def product_edit(request, uid):
     if 'email' not  in request.session:
        return redirect ('admin_panel:admin_login')
     product = get_object_or_404(Product, uid = uid)
    
     if request.method == 'POST':
        form = ProductForm(request.POST, instance = product)
        if form.is_valid():
            form.save()
            return redirect('admin_panel:product_listing')
     else:
        form = ProductForm(instance = product)

     return render(request, 'admin_templates/product/product_edit.html', {'form': form, 'product': product})

# -------------------------------------  function for adding product ----------------------------------

@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def add_product(request):
    if 'email' not in request.session:
        return redirect('admin_panel:admin_login')
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('admin_panel:product_listing')
    else:
        # Filter active brands only
        active_category = Category.objects.filter(is_active = True)
        active_brands = Brand.objects.filter(is_active=True)
        form = ProductForm(initial={'brand': active_brands.first()})  # Preselect the first active brand
        form.fields['brand'].queryset = active_brands  # Set the queryset for the brand field
        form.fields['product_category'].queryset = active_category
    return render(request, 'admin_templates/product/add_product.html', {'form': form})




# fucntion to list the varient of product 

def product_varients_listing(request):
    varients = Product_varients.objects.all()
    context = {'varients':varients}
    return render (request, 'admin_templates/product/varients_listing.html',context)


def product_varients_edit(request, uid):
    if 'email' not in request.session :
        return redirect ('admin_panel:admin_login')
    
    product_varient = get_object_or_404(Product_varients, uid = uid)

    if request.method == "POST" :
        form = Product_varientsForm(request.POST, request.FILES, instance = product_varient)
        if form.is_valid():
            form.save()
            return redirect ('admin_panel:product_varients_listing')
        else:
            print(form.errors)
    else:
        active_product = Product.objects.filter(is_active = True)
        active_ram = RamVarient.objects.filter(is_active = True)
        active_color = ColorVarient.objects.filter(is_active = True)
        
        form = Product_varientsForm(instance = product_varient)
        form.fields['product'].queryset = active_product
        form.fields['ram'].queryset = active_ram
        form.fields['color'].queryset = active_color
        
    return render (request, 'admin_templates/product/edit_varients.html', {'form':form, 'product_varient':product_varient})





# fucntion to add product varients 

def product_varients_add(request):
    if 'email' not in request.session :
        return redirect ('admin_panel:admin_login')
    if request.method == "POST" :
        form = Product_varientsForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect ('admin_panel:product_varients_listing')
        else:
            print(form.errors)
    else:
        active_product = Product.objects.filter(is_active = True)
        active_ram = RamVarient.objects.filter(is_active = True)
        active_color = ColorVarient.objects.filter(is_active = True)
        form = Product_varientsForm(initial={'product':active_product.first(),
                                             'ram':active_ram.first(),
                                             'color':active_color.first()})
        form.fields['product'].queryset = active_product
        form.fields['ram'].queryset = active_ram
        form.fields['color'].queryset = active_color
    
    
    return render(request, 'admin_templates/product/edit_varients.html',{'form':form})


def product_images(request):
    images = ProductImage.objects.all()
    return render (request, 'admin_templates/product/product_images.html', {"images":images})

def product_img_add(request):
    if request.method == 'POST':
        form = ProductVarientImageForm(request.POST , request.FILES)
        if form.is_valid():
            form.save()
            return redirect ('admin_panel:product_images')
        else:
            print(form.errors)
    else:
        form = ProductVarientImageForm()
    return render (request, 'admin_templates/product/add_product_img.html', {'form':form})



def product_img_delete(request, uid):
    try:
        img_to_delete = ProductImage.objects.get(uid=uid)
        img_to_delete.delete()
    except:
        pass
    return redirect ('admin_panel:product_images')



# ------------------------------ fucntion for render the form page for adding Banners -------------------------

@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def home_main_slider(request):
     if 'email' not in request.session:
         return redirect ('admin_panel:admin_login')
     if request.method=='POST':
          form=HomeMainSliderForm(request.POST, request.FILES)
          if form.is_valid():
               form.save()
               return redirect('admin_panel:home_main_slider')
     else:

          form= HomeMainSliderForm
     list=HomeMainSlide.objects.all()
     return render(request,'admin_templates/banners/HomeMainSlider.html',{'form':form,'list':list})






# -------------------------------  function for deleting the banner  --------------------------------

@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def delete_slide(request, slide_id):
    try:
        slide_to_delete = HomeMainSlide.objects.get(pk=slide_id)
        slide_to_delete.delete()
    except HomeMainSlide.DoesNotExist:
        # Handle the case where the slide with the given ID does not exist.
        pass

    return redirect('admin_panel:home_main_slider')


def Home_sub_banner(request):
    if 'email' not in request.session:
        return redirect('admin_panel:admin_login')
    if request.method == 'POST':
        form = HomeSubBannerForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('admin_panel:Home_sub_banner')
    else:
        form = HomeSubBannerForm
    list = HomeSubBanner.objects.all()
    return render(request, "admin_templates/banners/HomeSubBanner.html", {'form':form, 'list':list})
    





# --------------------------------- function for deleting sub banners ---------------------------------------

def delete_sub_banner(request, id):
    try:
        banner = HomeSubBanner.objects.get(id=id)
        banner.delete()
    except:
        pass
    return redirect('admin_panel:Home_sub_banner')







# ----------------- fucntion to add ram ------------------- 

def ram_list(request):
    if request.method == 'POST':
        form = RamForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('admin_panel:ram_list')
    else:
        form = RamForm
    list=RamVarient.objects.all()
    return render(request, 'admin_templates/product/ram_variations.html', {'form':form, 'list':list})





# ----------------- function for editing existing ram -----------------

def ram_edit(request, uid):
     if 'email' not  in request.session:
        return redirect ('admin_panel:admin_login')
     ram = get_object_or_404(RamVarient, uid = uid)
    
     if request.method == 'POST':
        form = RamForm(request.POST, instance = ram)
        if form.is_valid():
            form.save()
            return redirect('admin_panel:ram_list')
     else:
        form = RamForm(instance = ram)

     return render(request, 'admin_templates/product/ram_edit.html', {'form': form, 'ram': ram})




# -----------------function to add color -------------------

def color_list(request):
    if request.method == 'POST':
        form = ColorForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect ('admin_panel:color_list')
    else:
        form = ColorForm
    list = ColorVarient.objects.all()
    return render(request,'admin_templates/product/color_variations.html', {'form':form, 'list':list})




# ----------------- function for editing color--------------------

def color_edit(request, uid):
     if 'email' not  in request.session:
        return redirect ('admin_panel:admin_login')
     color = get_object_or_404(ColorVarient, uid = uid)
    
     if request.method == 'POST':
        form = ColorForm(request.POST, instance = color)
        if form.is_valid():
            form.save()
            return redirect('admin_panel:color_list')
     else:
        form = ColorForm(instance = color)

     return render(request, 'admin_templates/product/color_edit.html', {'form': form, 'color': color})



                                        
# -----------------------------------------------------------------------------------------------------------------------------------------------------------------------
# ====================================== ORDERS ================================================================================================================

def order_listing(request):
    orders = Order.objects.filter(is_ordered = True)
    print(orders)
    context = {
        'orders':orders
    }
    return render(request, 'admin_templates/orders/order_listing.html', context)

def order_details(request,id):
    order = Order.objects.get(order_number=id)
    total = order.order_total
    tax = order.tax
    products = OrderProduct.objects.filter(order=order)

    context = {
        'order':order,
        'total':total,
        'tax':tax,
        'products':products,
    }
    return render(request, "admin_templates/orders/order_details.html", context )


def admin_order_cancel(request,id):
    order = Order.objects.get(order_number=id)
    order.status = "Cancelled by Admin"
    order.save()
    order_products = OrderProduct.objects.filter(order=order)
    for order_product in order_products:
        product = Product_varients.objects.get(uid=order_product.product.uid)
        product.stock_qty += order_product.quantity 
        product.save()
    return redirect('admin_panel:order_listing')


def admin_order_accept(request,id):
    order = Order.objects.get(order_number=id)
    order.status = "Accepted"
    order.save()
    return redirect('admin_panel:order_listing')

def admin_order_complete(request,id):
    order = Order.objects.get(order_number=id)
    order.status = "Completed"
    order.save()
    return redirect('admin_panel:order_listing')

def admin_order_returned(request,id):
    order = Order.objects.get(order_number=id)
    order.status = "Returned"
    order.save()
    order_products = OrderProduct.objects.filter(order=order)
    for order_product in order_products:
        product = Product_varients.objects.get(uid=order_product.product.uid)
        product.stock_qty += order_product.quantity 
        product.save()
    return redirect('admin_panel:order_listing')





#----------------------------- coupons -----------------------------------------



# ---------------------- coupon page --------------------
def coupons_listing(request):
    if request.method == 'POST':
        form = CouponForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("admin_panel:coupons_listing")
    else:
        form = CouponForm
    list = Coupon.objects.all()
    return render(request, 'admin_templates/coupons/coupon.html', {'form':form, "list":list})


def coupons_edit(request,id):
    coupon = get_object_or_404(Coupon,id=id)
    if request.method == "POST":
        form = CouponForm(request.POST, instance=coupon)
        if form.is_valid():
            form.save()
            return redirect("admin_panel:coupons_listing")
        else:
            print(form.errors)
    else:
        form = CouponForm(instance=coupon)
    return render(request, "admin_templates/coupons/coupons_edit.html", {'form':form})


# --------------- fucntion for ad logout ---------------------------

def ad_log_out(request):
    logout(request)
    return redirect('admin_panel:admin_login')


