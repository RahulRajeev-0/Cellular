from django.shortcuts import render,redirect
from django.shortcuts import HttpResponse
from django.contrib import messages
from account_management.models import Account
from django.contrib.auth import authenticate,login,logout
from django.core.mail import send_mail
import random
from django.views.decorators.cache import cache_control


from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode,urlsafe_base64_decode
from django.utils.encoding import force_bytes
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import EmailMessage

# Create your views here.



#      function for rendering home page
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def index(request):
    if request.user.is_authenticated is None:
        return redirect ('account_management:index')
    return render(request,'account_management/index.html')



#      function for user login 
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def user_login(request):
    if request.user.is_authenticated:
        return redirect ('account_management:index')
    if request.method=="POST":
        uemail=request.POST.get('email')
        upass=request.POST.get('password')
        user=authenticate(request,email=uemail,password=upass)
        if user is not None:
           
            messages.success(request,"Loged In successfully")
            messages.info(request,"Now please enter the OTP ")
            request.session['email']=uemail
            return redirect ('account_management:otp_generation')
        else:
            messages.warning(request,'Invalide Credential')
            return redirect('account_management:user_login')
   
    return render(request,'account_management/user_login.html')




#      function for user sign_up
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
                if Account.objects.get(user_name=uname):
                    messages.warning(request,'Username already exist')
                    return redirect('account_management:user_signUp')
            except:
                pass
            
            #code for checking the email 
            try:
                if Account.objects.get(email=email):
                    messages.warning(request,'Email already exist !')
                    return redirect ('account_management:user_signUp')
            except:
                pass

            if ' ' in email or '.com' not in email:
                messages.warning(request,"Enter a valid email id 🫤!")
                return redirect('account_management:user_signUp')
            else:
                pass


            #code for checking phone number 
            if len(phone)<10 or len(phone)>12:
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
            if pass1!=pass2:
                messages.warning(request,"Passwords do not match. Please make sure the password and confirm password fields are identical")
                return redirect('account_management:user_signUp')
            else:
                pass
            if len(pass1)<8:
                messages.warning(request,"Password must contains atleast 8 characters")
                return redirect('account_management:user_signUp')
            else:
                pass

            user=Account.objects.create_user(uname,email,phone,pass1)
            messages.success(request,"Registed successfully")
            return redirect('account_management:user_login')

    return render(request,'account_management/user_signUp.html')


#function for logout 
def logout_user(request):
    logout(request)
    return redirect('account_management:index')



#function for gerating otp 

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



# function for opt rendering page
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def otp_verification(request):
     if request.user.is_authenticated:
        return redirect ('account_management:index')
     user=Account.objects.get(email=request.session['email'])
     if request.method=="POST":
         inputed_otp=request.POST.get('otp')
         if str(inputed_otp)==str(request.session['otp_key']):
             messages.success(request,"OTP VERIFICATION SUCCESSFUL")
             login(request,user)
             return redirect('account_management:index')
         else:
             messages.error(request,'OTP verification failed !')
             return redirect('account_management:otp_verification')
    
     return render(request,'account_management/otp_page.html')


# function for rendering the forgot password email input and checking fields.
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def forgot_pass_email(request):
    if request.user.is_authenticated:
        return redirect ('account_management:index')
    
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




            return redirect('account_management:user_login')
        else:
            messages.warning(request,"Account not found ! ")
            return redirect('account_management:forgot_pass_email')

    return render(request,'account_management/forgot_pass_email_page.html')


def resetpassword_valid(request,uidb64,token):
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

def reset_password(request):
    if request.method=='POST':
        pass1=request.POST.get('password_new')
        pass2=request.POST.get('password_conf')
        if pass1==pass2:
            uid=request.session.get('uid')
            user=Account.objects.get(pk=uid)
            user.set_password(pass1)
            user.save()
            messages.success(request,"Password reset successful")
            return redirect('account_management:user_login')
        else:
            messages.warning(request,"Password do not match !")
            return redirect('account_management:reset_password')
    return render(request,'account_management/reset_password.html')
