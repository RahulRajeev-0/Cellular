from django.shortcuts import render,HttpResponse,redirect
from account_management.models import Account
from django.contrib.auth import authenticate,login,logout
from django.contrib import messages



# Create your views here.
def admin_index (request):
    return render(request,'admin_templates/admin_index.html') 

def admin_login(request):
    if request.method=='POST':
            ademail=request.POST.get("email")
            passw=request.POST.get('password')
           
            user=authenticate(email=ademail,password=passw)
           
            if user is not None and user.is_superuser:
                login(request,user)
                return redirect('admin_index')
            else:
                messages.warning(request, 'Invalid.')
                return redirect ('admin_login')
    return render(request,'admin_templates/admin_login.html') 
      