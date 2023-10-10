from django.shortcuts import render

# Create your views here.

def cart_page(request):
    return render(request, 'cart/cart_page.html')
