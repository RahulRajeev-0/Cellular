from django.shortcuts import render,HttpResponse,redirect
from account_management.models import Account
from django.contrib.auth import authenticate,login,logout
from django.contrib import messages
from django.views.decorators.cache import cache_control
from django.shortcuts import get_object_or_404


# ------------ from app imports ----------------

# >>>>>>>>>>>>>>>>>>> models <<<<<<<<<<<<<<<<<<<<
from account_management.models import Account
from account_management.models import HomeMainSlide,HomeSubBanner
from product.models import Brand,Product,RamVarient,ColorVarient

# >>>>>>>>>>>>>>>>>> forms <<<<<<<<<<<<<<<<<<<<<< 
from product.forms import BrandForm,ProductForm,RamForm,ColorForm
from account_management.forms import HomeMainSliderForm, HomeSubBannerForm






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



# -------------------------------------  function for adding product ----------------------------------

@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def add_product(request):
     if 'email' not in request.session:
        return redirect ('admin_panel:admin_login')
     if request.method=='POST':
          form=ProductForm(request.POST)
          if form.is_valid():
               form.save()
               return redirect('admin_panel:product_listing')
          
     form= ProductForm
     return render(request,'admin_templates/product/add_product.html',{'form':form})





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


# --------------- fucntion for ad logout ---------------------------

def ad_log_out(request):
    logout(request)
    return redirect('admin_panel:admin_login')


