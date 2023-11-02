from django.shortcuts import render
from django.core.paginator import EmptyPage , PageNotAnInteger , Paginator
# ---------------------------------- models -----------------------------------
from offers.models import ProductOffer , CategoryOffer
from product.models import Product_varients, Product
from cart.models import WishList



# Create your views here.
def offers(request):
    product_offer_slide = ProductOffer.objects.all()
    category_offer_slide = CategoryOffer.objects.all()
    context = {
        'product_offer_slide':product_offer_slide,
        'category_offer_slide':category_offer_slide,
        }
    return render (request, "offers/offer_page.html", context)




# ------------------------- SHOWING THE SHOP PAGE WITH ONLY THE PRODUCT OFFERS -------------

def shop_product_offer(request,id):
    offer = ProductOffer.objects.get(id=id)
    product_variants = offer.product.filter(is_active=True)
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
        'product_variants': paged_products,
        'wishlist_items': wishlist_items,
        }
    return render (request, 'products/shoping.html',context)


def shop_category_offer(request,id):
    offer = CategoryOffer.objects.get(id=id)
    cate = offer.category.filter(is_active=True)
    
    product_variants = Product_varients.objects.filter(product__product_category__in=cate, is_active=True)

    print("+++++++++++++++++++++++++++++++++++/n")
    print(product_variants)
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
        'product_variants': paged_products,
        'wishlist_items': wishlist_items,
        }
    return render (request, 'products/shoping.html', context)