from django.shortcuts import render , redirect , HttpResponse
from django.shortcuts import get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
# -------------------- models --------------------------
from product.models import Product_varients
from cart.models import Cart , CartItem

# Create your views here.


# function for getting session for storing it in the cart id 

def _cart_id(request):
    cart = request.session.session_key
    if not cart :
        cart = request.session.create()
    return cart



# add to cart function that adds the products to the cart 
def add_cart(request, product_uid):
    current_user = request.user
    if current_user.is_authenticated :
        product = Product_varients.objects.get(uid=product_uid) # get product 
        
        is_cart_item_exits = CartItem.objects.filter(product = product , user = current_user).exists()
        try :
            cart_item = CartItem.objects.get(product = product , user = current_user)
            if cart_item.product.stock_qty > cart_item.quantity:   # checking the quantiy in stock and cart quantity 
                cart_item.quantity += 1         #cart_item.quantity = cart_item.quantity + 1 
                cart_item.save()
            else:
                messages.warning(request, "Oops! It looks like the quantity you're trying to add is more than what we currently have in stock. Please adjust the quantity and try again. ")
                return redirect ('cart:cart_page')
        except CartItem.DoesNotExist:
            cart_item = CartItem.objects.create(
                product = product ,
                quantity = 1 ,
                user = current_user ,
                )
            cart_item.save()
    
        return redirect ('cart:cart_page')
    
    # if the user is not authenticated 
    else:
        product = Product_varients.objects.get(uid = product_uid) # get product 
        try :
            cart = Cart.objects.get(cart_id = _cart_id(request))  # get the cart using the cart_id present in the session 
        except Cart.DoesNotExist:
            cart = Cart.objects.create(
                cart_id = _cart_id(request)
            )
            cart.save()


        is_cart_item_exits = CartItem.objects.filter(product = product , cart = cart).exists()
        try :
            cart_item = CartItem.objects.get(product = product , cart = cart)
            if cart_item.product.stock_qty > cart_item.quantity:
                cart_item.quantity += 1         #cart_item.quantity = cart_item.quantity + 1 
                cart_item.save()
            else:
                messages.warning(request, "Oops! It looks like the quantity you're trying to add is more than what we currently have in stock. Please adjust the quantity and try again. ")
                return redirect ('cart:cart_page')
            
        except CartItem.DoesNotExist:
            cart_item = CartItem.objects.create(
                product = product ,
                quantity = 1 ,
                cart = cart ,
                )
            cart_item.save()
    
        return redirect ('cart:cart_page')



def remove_cart(request , product_uid):
    
    product = get_object_or_404(Product_varients , uid = product_uid)
    try:
        if request.user.is_authenticated:
            cart_item = CartItem.objects.get(product=product , user = request.user)
        else:
            cart = Cart.objects.get(cart_id = _cart_id(request))
            cart_item = CartItem.objects.get(product=product , cart = cart)
    except:
        pass

    if cart_item.quantity > 1 :
        cart_item.quantity -= 1
        cart_item.save()
    else:
        cart_item.delete()
    return redirect ('cart:cart_page')




def remove_cart_item(request, product_uid):
    product = get_object_or_404(Product_varients, uid = product_uid)
    if request.user.is_authenticated:
        cart_item = CartItem.objects.get(product = product , user = request.user)
        cart_item.delete()
    else:
        cart = Cart.objects.get(cart_id = _cart_id(request))    
        cart_item = CartItem.objects.get(product = product , cart = cart)
        cart_item.delete()
    return redirect ('cart:cart_page')




# function to render the cart page 
def cart_page(request, total = 0 , quantity = 0 , cart_items = None):
    tax = 0
    grand_total = 0
    
    try :
        if request.user.is_authenticated:
            cart_items = CartItem.objects.filter(user = request.user, is_active = True)
        else:
            cart = Cart.objects.get(cart_id=_cart_id(request))
            cart_items = CartItem.objects.filter(cart=cart, is_active = True)
        for cart_item in cart_items:
            total += (cart_item.product.price * cart_item.quantity)
            quantity += cart_item.quantity
        tax = (2 * total)/100
        grand_total = total + tax
    except :
        pass  # ingnore 
    
    context = { 
        'total': total ,
        'quantity': quantity ,
        'cart_items':cart_items ,
        'tax': tax,
        'grand_total':grand_total,

    }
    return render(request, 'cart/cart_page.html', context)



@login_required(login_url='account_management:user_login')
def checkout(request, total = 0 , quantity = 0 , cart_items = None):
    tax = 0
    grand_total = 0
    
    try :
        cart = Cart.objects.get(cart_id=_cart_id(request))
        cart_items = CartItem.objects.filter(cart=cart, is_active = True)
        for cart_item in cart_items:
            total += (cart_item.product.price * cart_item.quantity)
            quantity += cart_item.quantity
        tax = (2 * total)/100
        grand_total = total + tax
    except :
        pass  # ingnore 
    
    context = { 
        'total': total ,
        'quantity': quantity ,
        'cart_items':cart_items ,
        'tax': tax,
        'grand_total':grand_total,

    }
    return render (request, 'cart/checkout.html', context)