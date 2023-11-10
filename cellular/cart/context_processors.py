from cart.models import Cart , CartItem
from cart.views import _cart_id

def counter(request):
    cart_count = 0 
    try :
        cart = Cart.objects.filter(cart_id = _cart_id(request))
        if request.user.is_authenticated :
            cart_items = CartItem.objects.all().filter(user = request.user)
        else:

            cart_items = CartItem.objects.all().filter(cart = cart[:1])
        for cart_item in cart_items :
            cart_count += cart_item.quantity
    except Cart.DoesNotExist:
        cart_item = 0 

    return dict(cart_count = cart_count)



from .models import WishList

def wishlist_count(request):
    if request.user.is_authenticated:
        wishlist_count = WishList.objects.filter(user=request.user).count()
    else:
        wishlist_count = 0
    return {'wishlist_count': wishlist_count}
