from django.shortcuts import render,HttpResponse , redirect
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from product.models import Product ,Product_varients , RamVarient ,ColorVarient , ProductImage
from cart.models import Cart,CartItem , WishList
from cart.views import _cart_id
from django.core.paginator import EmptyPage , PageNotAnInteger , Paginator

# Create your views here.


def shoping_page(request):
    products = Product.objects.all()
    product_variants = Product_varients.objects.all().filter(is_active = True).order_by('uid')  # Get all product variants
    paginator = Paginator(product_variants , 6)
    page = request.GET.get('page')
    if request.user.is_authenticated:
        wishlist_items = WishList.objects.filter(user=request.user).exists()
    else:
        wishlist_items = None
    if not wishlist_items:
        wishlist_items = 0
    else:
        wishlist_items = WishList.objects.filter(user=request.user).values_list('product__uid', flat=True)
    paged_products = paginator.get_page(page)
    
        
    context = {
        'products': products, 
        'product_variants': paged_products,
        'wishlist_items': wishlist_items,
        }
    
    return render(request, 'products/shoping.html', context)


def product_details(request, vuid ):
    product_variant_instance = get_object_or_404(Product_varients, uid = vuid)
    product_varients = Product_varients.objects.filter(product=product_variant_instance.product).exclude(uid=vuid)
    print("++++++++++++++++++++\n")
    print(product_varients)
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
        'product_varients':product_varients,
            })
    




# search suggestion 
def get_names(request):
    search = request.GET.get('search')
    if search:
        objs = Product_varients.objects.filter(product_heading__istartswith=search)
        payload = [{'name': obj.product_heading} for obj in objs]
    else:
        payload = []

    return JsonResponse({
        'status': True,
        'payload': payload
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




def filter_by_price(request):
    if request.method == "POST":
        value = request.POST.get('amount')
        if value == "-15000":
            product_variants = Product_varients.objects.filter(price__lt=15000.0)
        elif value == "-30000":
            product_variants = Product_varients.objects.filter(price__lt=30000.0)
        elif value == "-50000":
            product_variants = Product_varients.objects.filter(price__lt=50000.0)
        elif value == "-70000":
            product_variants = Product_varients.objects.filter(price__lt=70000.0)
        elif value == "-90000":
            product_variants = Product_varients.objects.filter(price__lt=90000.0)
        else:
            product_variants = Product_varients.objects.filter(price__gte=90000.0)
        
        context = {'product_variants': product_variants}
        return render(request, 'products/shoping.html', context)