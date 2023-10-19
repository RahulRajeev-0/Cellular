from django.shortcuts import render,HttpResponse , redirect
from django.shortcuts import get_object_or_404
from product.models import Product ,Product_varients , RamVarient ,ColorVarient , ProductImage
from cart.models import Cart,CartItem
from cart.views import _cart_id
from django.core.paginator import EmptyPage , PageNotAnInteger , Paginator

# Create your views here.


def shoping_page(request):
    products = Product.objects.all()
    product_variants = Product_varients.objects.all().filter(is_active = True).order_by('uid')  # Get all product variants
    paginator = Paginator(product_variants , 6)
    page = request.GET.get('page')
    paged_products = paginator.get_page(page)
    
    context = {
        'products': products, 
        'product_variants': paged_products,
        }
    
    return render(request, 'products/shoping.html', context)


def product_details(request, vuid ):
    product_variant_instance = get_object_or_404(Product_varients, uid = vuid)
    ram_variants = RamVarient.objects.filter(product_varients = product_variant_instance)
    color_varients = ColorVarient.objects.filter(product_varients = product_variant_instance)
    photos = product_variant_instance.product_images.all()

    try:
        in_cart = CartItem.objects.filter(cart__cart_id = _cart_id(request), product = product_variant_instance).exists()
    except:
        pass
    return render(request, 'products/product_details.html', context = {
        'product_variants': product_variant_instance,
        'ram_variants': ram_variants , 
        'color_varients':color_varients ,
        'photos':photos ,
        'in_cart':in_cart ,
            })
    


def shop_sreach(request):
    if request.method == "POST":
        product = request.POST.get('sreach_product','')
    
        if product:
            products = Product.objects.all()
            product_variants = Product_varients.objects.filter(product_heading__icontains=product)
            context = {'product_variants':product_variants}
            return render(request, 'products/shoping.html', context)
    return redirect ('product:shoping_page')
