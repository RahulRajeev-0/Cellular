from django.shortcuts import render,HttpResponse,redirect
from account_management.models import Account
from django.contrib.auth import authenticate,login,logout
from django.contrib import messages
from account_management.models import Account



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
                return redirect('admin_panel:admin_index')
            else:
                messages.warning(request, 'Invalid.')
                return redirect ('admin_panel:admin_login')
    return render(request,'admin_templates/admin_login.html') 




# function for user listing 
def user_listing(request):
     users=Account.objects.all()
     context={'users':users}
     return render(request,'admin_templates/user_list.html',context)

def user_block_unblock(request,id):
        user=Account.objects.get(id=id)
        if user.is_active:
            user.is_active=False
            user.save()
        else:
            user.is_active=True
            user.save()
        return redirect ('admin_panel:user_listing')
 


     