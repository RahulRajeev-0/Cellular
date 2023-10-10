from django.shortcuts import render,HttpResponse
from django.shortcuts import get_object_or_404
from product.models import Product ,Product_varients , RamVarient ,ColorVarient , ProductImage


# Create your views here.
# def shoping_page(request):
#     context={'products':Product.objects.all()}
#     return render(request,'products/shoping.html',context)

def shoping_page(request):
    products = Product.objects.all()
    product_variants = Product_varients.objects.all()  # Get all product variants
    context = {'products': products, 'product_variants': product_variants}
    return render(request, 'products/shoping.html', context)


def product_details(request, vuid , puid):
    product_variant_instance = get_object_or_404(Product_varients, uid = vuid)
    ram_variants = RamVarient.objects.filter(product_varients = product_variant_instance)
    color_varients = ColorVarient.objects.filter(product_varients = product_variant_instance)
    photos = product_variant_instance.product_images.all()
    return render(request, 'products/product_details.html', context = {'product_variants': product_variant_instance, 'ram_variants': ram_variants , 'color_varients':color_varients , 'photos':photos })
    