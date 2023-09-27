from django.shortcuts import render,HttpResponse
from product.models import Product


# Create your views here.
def shoping_page(request):
    context={'products':Product.objects.all()}
    return render(request,'products/shoping.html',context)

def product_details(request,slug):
    product=Product.objects.get(slug=slug)
    return render(request,'products/product_details.html',context={'product':product    })
  
    