from django.shortcuts import render,HttpResponse


# Create your views here.
def shoping_page(request):
    return render(request,'products/shoping.html')

def product_details(request):
    return render(request,'products/product_details.html')