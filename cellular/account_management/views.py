from django.shortcuts import render,redirect
from django.shortcuts import HttpResponse
from django.contrib import messages
from account_management.models import Account
from django.contrib.auth import authenticate,login,logout


# Create your views here.




def index(request):
    return render(request,'account_management/index.html')

def user_login(request):
    if request.method=="POST":
        uemail=request.POST.get('email')
        upass=request.POST.get('password')
        user=authenticate(request,email=uemail,password=upass)
        if user is not None:
            login(request,user)
            messages.success(request,"Loged In successfully")
            return redirect ('index')
        else:
            messages.warning(request,'Invalide Credential')
    
    return render(request,'account_management/user_login.html')




#      function for user sign_up

def user_signUp(request):
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
                    return redirect('/user_signUp')
            except:
                pass

            try:
                if Account.objects.get(user_name=uname):
                    messages.warning(request,'Username already exist')
                    return redirect('/user_signUp')
            except:
                pass
            
            #code for checking the email 
            try:
                if Account.objects.get(email=email):
                    messages.warning(request,'Email already exist !')
                    return redirect ('/user_signUp')
            except:
                pass

            if ' ' in email or '.com' not in email:
                messages.warning(request,"Enter a valid email id 🫤!")
                return redirect('/user_signUp')
            else:
                pass


            #code for checking phone number 
            if len(phone)<10 or len(phone)>12:
                messages.warning(request,"Enter a valid phone number !")
                return redirect('/user_signUp')
            else:
                pass
            if not phone.isdigit():
                messages.warning(request,"Please enter valid phone number !")
                return redirect('/user_signUp')
            else:
                pass

            #code for checking the password 
            if pass1!=pass2:
                messages.warning(request,"Passwords do not match. Please make sure the password and confirm password fields are identical")
                return redirect('/user_signUp')
            else:
                pass
            if len(pass1)<8:
                messages.warning(request,"Password must contains atleast 8 characters")
                return redirect('/user_signUp')
            else:
                pass

            user=Account.objects.create_user(uname,email,phone,pass1)
            messages.success(request,"Registed successfully")
            return redirect('/user_login')

    return render(request,'account_management/user_signUp.html')


