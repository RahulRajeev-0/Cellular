from django.shortcuts import render,redirect
from django.shortcuts import HttpResponse
from django.contrib import messages
from account_management.models import Account , userAddressBook
from django.contrib.auth import authenticate,login,logout
from django.core.mail import send_mail
import random
import string
from django.views.decorators.cache import cache_control


from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode,urlsafe_base64_decode
from django.utils.encoding import force_bytes
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import EmailMessage
from account_management.models import HomeMainSlide,HomeSubBanner
from cart.models import Cart , CartItem
from cart.views import _cart_id

from wallet.models import Wallet




# Create your views here.



# ----------------------------------- function for rendering home page    ------------------------------------

@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def index(request):
    main_slid = HomeMainSlide.objects.all()
    sub_banners = HomeSubBanner.objects.all()
    context={'main_slid':main_slid, 'sub_banners':sub_banners}
    if request.user.is_authenticated is None:
        return redirect ('account_management:index')
    return render(request,'account_management/index.html',context)



#   ------------------------------------------   function for user login    ------------------------------------

@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def user_login(request):
    if request.user.is_authenticated:
        return redirect ('account_management:index')
    if request.method=="POST":
        uemail=request.POST.get('email')
        try:
            account=Account.objects.get(email=uemail)
        except:
            pass
        upass=request.POST.get('password')
        user=authenticate(request,email=uemail,password=upass)
        if user is not None:
            try:
                cart = Cart.objects.get(cart_id = _cart_id(request))
                is_cart_item_exits = CartItem.objects.filter(cart = cart).exists()
                if is_cart_item_exits:
                    cart_item = CartItem.objects.filter(cart = cart)
                    for item in cart_item:
                        item.user = user
                        item.save()
                    
            except:
                pass
            request.session['email']=uemail
            login(request,user)
            return redirect ('account_management:index')
        elif account is not None:
            if account.is_active==False:
                messages.warning(request,'Your are blocked !')
                return redirect('account_management:user_login')
            else:
                pass
            
        else:
            messages.warning(request,'Invalide Credential')
            return redirect('account_management:user_login')
   
    return render(request,'account_management/user_login.html')




#   ------------------------------------   function for user sign_up  ------------------------------------------------


@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def user_signUp(request):
    if request.user.is_authenticated:
        return redirect ('account_management:index')
    if request.method=="POST":
        uname=request.POST['name']
        email=request.POST.get('email')
        phone=request.POST.get('phone_no')
        pass1=request.POST.get('passw1')
        pass2=request.POST.get('passw2')
        refferal_code = request.POST.get('refferal_code')
        print("++++++++++++++++++++++++")
        print(refferal_code)
        user=Account.objects.all()
        print(user)
        if uname and email and phone and pass1 and pass2 :

            #code for checking the username 

            try:
                if len(uname)<=2:
                    messages.warning(request,'Username must contains atleast 3 letter')
                    return redirect('account_management:user_signUp')
            except:
                pass

            try:
                if Account.objects.get(user_name = uname):
                    messages.warning(request, 'Username already exist')
                    return redirect('account_management:user_signUp')
            except:
                pass
            
            #code for checking the email 
            try:
                if Account.objects.get(email = email):
                    messages.warning(request, 'Email already exist !')
                    return redirect ('account_management:user_signUp')
            except:
                pass

            if ' ' in email or '.com' not in email:
                messages.warning(request, "Enter a valid email id 🫤!")
                return redirect('account_management:user_signUp')
            else:
                pass


            #code for checking phone number 
            if len(phone) < 10 or len(phone) > 12:
                messages.warning(request,"Enter a valid phone number !")
                return redirect('account_management:user_signUp')
            else:
                pass
            if not phone.isdigit():
                messages.warning(request,"Please enter valid phone number !")
                return redirect('account_management:user_signUp')
            else:
                pass

            #code for checking the password 
            if pass1 != pass2:
                messages.warning(request, "Passwords do not match. Please make sure the password and confirm password fields are identical")
                return redirect('account_management:user_signUp')
            else:
                pass
            if len(pass1) < 8:
                messages.warning(request, "Password must contains atleast 8 characters")
                return redirect('account_management:user_signUp')

            else:
                pass
            if " " in pass1:
                messages.warning(request, "Blank space is not allowed in password")
                return redirect('account_management:user_signUp')

            user=Account.objects.create_user(uname, email, phone, pass1)
            Wallet.objects.create(user=user)
            messages.success(request, "OTP Sent to you email !")
            request.session['email'] = email

            # code for applying refferal offers 
            if refferal_code:
                try:
                    reffer = Account.objects.get(referral_code=refferal_code)
                    try:
                        user_wallet = Wallet.objects.get(user=reffer)
                        user_wallet.balance += 250
                        user_wallet.save()
                    except:
                        pass
                    user_wallet = Wallet.objects.get(user=user)
                    user_wallet.balance += 200
                    user_wallet.save()
                except:
                    messages.info(request,"Invalid refferal Code")
            try:
                cart = Cart.objects.get(cart_id = _cart_id(request))
                is_cart_item_exits = CartItem.objects.filter(cart = cart).exists()
                if is_cart_item_exits:
                    cart_item = CartItem.objects.filter(cart = cart)
                    for item in cart_item:
                        item.user = user
                        item.save()
            except:
                pass
            return redirect('account_management:otp_generation')
        

    return render(request,'account_management/user_signUp.html')







#    ---------------------------------------  function for logout  ----------------------------------------------
 
def logout_user(request):
    logout(request)
    return redirect('account_management:index')



#   ---------------------------------------------------  function for gerating otp  --------------------------------------

def otp_generation(request):
    otp_number=random.randint(1000,9999)
    request.session['otp_key']=otp_number
    send_mail(
        "OTP VERIFICATION CELLUAR ",
        f"OTP = {otp_number}",
        "ravanan0908@gmail.com",
        [request.session['email']],
        fail_silently=False,
    )
    return redirect('account_management:otp_verification')



# --------------------------------------------  function for opt rendering page  -----------------------------------

@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def otp_verification(request):
     if request.user.is_authenticated:
        return redirect ('account_management:index')
     user=Account.objects.get(email=request.session['email'])
     if request.method=="POST":
         inputed_otp=request.POST.get('otp')
         if str(inputed_otp)==str(request.session['otp_key']):
             login(request,user)
             return redirect('account_management:index')
         else:
             messages.error(request,'OTP verification failed !')
             return redirect('account_management:otp_verification')
    
     return render(request,'account_management/otp_page.html')







# --------------------------------- function for rendering the forgot password email input and checking fields.  -------------------------------------

@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def forgot_pass_email(request):
    if request.method=='POST':
        forEmail=request.POST.get('email')
        if Account.objects.filter(email=forEmail).exists():
            user=Account.objects.get(email__exact=forEmail)
           
            # reset password email 
            current_site=get_current_site(request)
            mail_subject='Reset your password '
            message=render_to_string('account_management/reset_password_email.html',
            {
                'user':user,
                'domain':current_site,
                'uid':urlsafe_base64_encode(force_bytes(user.pk)),
                'token':default_token_generator.make_token(user),

            })
            to_email=forEmail
            send_mail=EmailMessage(mail_subject,message,to=[to_email])
            send_mail.send()
            messages.info(request,"Password reset email has been sent to your email address ")



            request.session['email']=forEmail
            return redirect('account_management:user_login')
        else:
            messages.warning(request,"Account not found ! ")
            return redirect('account_management:forgot_pass_email')

    return render(request,'account_management/forgot_pass_email_page.html')





# --------------------------------  function for reset password decoding  ---------------------------------------------

def resetpassword_valid(request, uidb64, token):
    try:
        uid=urlsafe_base64_decode(uidb64).decode()
        user=Account._default_manager.get(pk=uid)
    except(TypeError,ValueError,OverflowError,Account.DoesNotExist):
        user=None
    
    if user is not None and default_token_generator.check_token(user,token):
        request.session['uid']=uid
        messages.success(request,'Please Reset your password')
        return redirect('account_management:reset_password')
    else:
        messages.warning(request,'This link is expired ! ')
        return redirect('account_management:user_login')





# ---------------------------------  function for reset password  creating new password page and validation for password --------------------------------------

@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def reset_password(request):
    if request.method=='POST':
        pass1=request.POST.get('password_new')
        pass2=request.POST.get('password_conf')
        if pass1==pass2:
            uid=request.session.get('uid')
            user=Account.objects.get(pk=uid)
            user.set_password(pass1)
            user.save()
            login(request,user)
            return redirect('account_management:index')
        else:
            messages.warning(request,"Password do not match !")
            return redirect('account_management:reset_password')
    return render(request,'account_management/reset_password.html')



    
def user_profile(request):
    user = Account.objects.get(email=request.user)
    addresses = userAddressBook.objects.filter(user=request.user)
    try:
        wallet_money = Wallet.objects.get(user=user)
    except:
        wallet_money = 0
    context = {
        'user':user,
        'addresses':addresses,
        'wallet_money':wallet_money,
    }
    return render(request, 'account_management/user_profile.html', context)