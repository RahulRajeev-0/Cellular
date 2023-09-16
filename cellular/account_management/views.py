from django.shortcuts import render
from django.shortcuts import HttpResponse

# Create your views here.
def index(request):
    return render(request,'account_management/index.html')

def user_login(request):
    return render(request,'account_management/user_login.html')

def user_signUp(request):
    return render(request,'account_management/user_signUp.html')
