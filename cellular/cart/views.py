from django.shortcuts import render , redirect , HttpResponse 
from django.http.response import JsonResponse
from django.shortcuts import get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.forms import ValidationError
from django.shortcuts import get_object_or_404


#-----------------forms----------------
from account_management.forms import userAddressBookForm
from account_management.models import userAddressBook

# -------------------- models --------------------------
from product.models import Product_varients
from cart.models import Cart , CartItem , WishList
from orders.models import Coupon

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
        # product_id = request.POST.get('product_id')
        # product_check = Product_varients.objects.get(uid=product_id)
        # is_cart_item_exits = CartItem.objects.filter(product = product , user = current_user).exists()
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





def newcart_update(request):
    new_quantity = 0
    total = 0
    tax = 0
    grand_total = 0
    quantity=0
    counter=0
    if request.method == "POST":
        prod_id = request.POST.get("product_id")
        cart_item_id = int(request.POST.get('cart_id'))
        qty = int(request.POST.get('qty'))
        counter = int(request.POST.get('counter'))
        product = get_object_or_404(Product_varients, uid=prod_id)
        
        if request.user.is_authenticated:
            try:
                cart_item = CartItem.objects.get(product=product)
                cart_items = CartItem.objects.filter(user=request.user)
            except:
                return JsonResponse({'status': 'error', 'message': 'Cart item not found'})
            
            if cart_item.quantity < product.stock_qty:
                cart_item.quantity += 1
                cart_item.save()
                sub_total = cart_item.quantity * product.product_price()
                
                new_quantity = cart_item.quantity
            else:
                messages.warning(request, "Out of Stock")
                return JsonResponse({'status': 'error', 'message': "out of stock"})    

            for item in cart_items:
                total += (item.product.product_price() * item.quantity)
                quantity += item.quantity
            tax = (2 * total)/100
            grand_total = total + tax 
       
            if new_quantity == 0 :
                message = "out of stock"
                return JsonResponse({'status': 'error', 'message': message})
            else:
                return JsonResponse({
            'status': "success",
            'new_quantity': new_quantity,
            "total": total,
            "tax": tax,
            'counter':counter,
            "grand_total": grand_total,
            "sub_total":sub_total,
            })
        else:
            # getting the session for getting the cart items 
            try:
                cart = Cart.objects.get(cart_id = _cart_id(request))  # get the cart using the cart_id present in the session 
            except Cart.DoesNotExist:
                cart = Cart.objects.create(
                    cart_id=_cart_id(request)
                    )  
                cart.save()  
            
            # using the getted cart or created cart  trying get the cart item
            
            cart_item = CartItem.objects.get(cart=cart, product=product)
            cart_items = CartItem.objects.filter(cart=cart)
            if cart_item.quantity < product.stock_qty:
                cart_item.quantity += 1
                cart_item.save()
                sub_total = cart_item.quantity * product.product_price()
                new_quantity = cart_item.quantity
            else:
                message = "Out of Stock"
                return JsonResponse({"status":"error", "message":message})
            for item in cart_items:
                total += (item.product.product_price() * cart_item.quantity)
                quantity = item.quantity
            tax = (2* total)/100
            grand_total = tax + total

            if new_quantity == 0:
                message = "out of stock"
                return JsonResponse({'status': 'error', 'message': message})
            else:
                return JsonResponse({
                    'status': "success",
                    'new_quantity': new_quantity,
                    "total": total,
                    "tax": tax,
                    'counter':counter,
                    "grand_total": grand_total,
                    "sub_total":sub_total,
                })

# function to add the cart items using adjax 










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


def ajax_remove_cart(request):
    # initailizing the values 
    new_quantity = 0
    total = 0
    tax = 0
    grand_total = 0
    quantity=0
    counter=0
    
    
    if request.method == "POST":

        # getting the values from the fornt end 
        prod_id = request.POST.get("product_id")
        cart_item_id = int(request.POST.get('cart_id'))
        qty = int(request.POST.get('qty'))
        counter = int(request.POST.get('counter'))
        product = get_object_or_404(Product_varients, uid=prod_id)

        # if the user is authenticaed or logged in 
        if request.user.is_authenticated :
            try:
                cart_item = CartItem.objects.get(product=product)
                cart_items = CartItem.objects.filter(user=request.user)
            except:
                return JsonResponse({'status': 'error', 'message': 'Cart item not found'})
            
            if cart_item.quantity > 1 :
                cart_item.quantity -= 1
                cart_item.save()
                sub_total = cart_item.quantity * product.product_price()
                new_quantity = cart_item.quantity
            else:
                cart_item.delete()
                message = "the cart iem has bee deleted"
                return JsonResponse({'status': 'error', 'message': message})
            
            for item in cart_items:
                total += (cart_item.product.product_price() * cart_item.quantity)
                quantity = cart_item.quantity
            tax = (2* total)/100
            grand_total = tax + total
            return JsonResponse({
                    'status': "success",
                    'new_quantity': new_quantity,
                    "total": total,
                    "tax": tax,
                    'counter':counter,
                    "grand_total": grand_total,
                    "sub_total":sub_total,
                })
        else:
            try :
                cart = Cart.objects.get(cart_id=_cart_id(request))
            except Cart.DoesNotExist:
                cart = Cart.objects.create(
                    cart_id=_cart_id(request)
                    )  
                cart.save()  
            cart_items = CartItem.objects.filter(cart=cart)
            cart_item = CartItem.objects.get(product=product)

            if cart_item.quantity > 0 :
                cart_item.quantity -= 1
                cart_item.save()
                sub_total = cart_item.quantity * product.product_price()
                new_quantity = cart_item.quantity
            else:
                cart_item.delete()
                message = "the cart iem has bee deleted"
                return JsonResponse({'status': 'error', 'message': message})
            for item in cart_items:
                total += (cart_item.product.product_price() * cart_item.quantity)
                quantity = cart_item.quantity
            tax = (2* total)/100
            grand_total = tax + total
            return JsonResponse({
                    'status': "success",
                    'new_quantity': new_quantity,
                    "total": total,
                    "tax": tax,
                    'counter':counter,
                    "grand_total": grand_total,
                    "sub_total":sub_total,
                })
            

            

    




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
            total += (cart_item.product.product_price() * cart_item.quantity)
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
    user_address_book_exists = userAddressBook.objects.filter(user=request.user).exists()
    user_addresses = None
    user_address_count = 0
    if user_address_book_exists:
        user_addresses = userAddressBook.objects.filter(user=request.user)
        
    if request.method == "POST":
        form = userAddressBookForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('cart:checkout')
        else:
            print(form.errors)
    else:
        form = userAddressBookForm

    try :
        # cart = Cart.objects.get(user=ses)
        cart_items = CartItem.objects.filter(user = request.user, is_active = True)
        for cart_item in cart_items:
            total += (cart_item.product.product_price() * cart_item.quantity)
            if cart_item.product.stock_qty > 0:
                quantity += cart_item.quantity
            else:
                messages.warning(request, f'{cart_item.product} is out of Stock ! ')
                return redirect('cart:cart_page')
        tax = (2 * total)/100
        grand_total = total + tax
    except :
        pass  # ingnore

    

    context = { 
        'total': total ,
        'quantity': quantity ,
        'cart_items': cart_items, 
        'tax': tax,
        'grand_total':grand_total,
        'form':form,
        'user_address_book_exists': user_address_book_exists,  # Include the user_address_book_exists variable in the context
        'user_addresses':user_addresses,
    }
    return render (request, 'cart/checkout.html', context)



# def add_address(request):
#     if request.method == "POST":
#         form = userAddressBookForm(request.POST)
#         if form.is_valid():
#             form.save()
#             return redirect('cart:checkout')
#         else:
#             print(form.errors)
#     else:
#         form = userAddressBookForm
#     return render(request, 'cart/add_address.html',{'form':form})




@login_required(login_url='account_management:user_login')
def add_address(request):
    if request.method == "POST":
        form = userAddressBookForm(request.POST)
        if form.is_valid():
            user_address_book_exists = userAddressBook.objects.filter(user=request.user).exists()
            if user_address_book_exists:
                existing_addresses_count = userAddressBook.objects.filter(user=request.user).count()
                if existing_addresses_count < 2:
                    address_book = form.save(commit=False)
                    address_book.user_id = request.user.id
                    address_book.save() 
                    return redirect('cart:checkout')
                else:
                    messages.warning(request,"Only 2 Address can be added")
                    return redirect('cart:checkout')
            else:
                address_book = form.save(commit=False)
                address_book.user_id = request.user.id
                address_book.save() 
                return redirect('cart:checkout')
        else:
            print(form.errors)
    else:
        
        form = userAddressBookForm()  # Instantiate the form

    return render(request, 'cart/add_address.html', {'form': form})






@login_required(login_url='account_management:user_login')
def address_default(request, id):
    address = userAddressBook.objects.get(id=id)
    address.is_default = not address.is_default  # Toggle the is_default field
    address.save()  # Save the updated object to the database
    return redirect('cart:checkout')




@login_required(login_url='account_management:user_login')
def edit_address(request,id):
    user_address_book = get_object_or_404(userAddressBook, id=id)
    if request.method == "POST":
        form = userAddressBookForm(request.POST, instance = user_address_book)
        if form.is_valid():
            form.save()
            return redirect('cart:checkout')
        else:
            print(form.error)
    else:
        form = userAddressBookForm(instance=user_address_book)
    return render(request, 'cart/edit_address.html',{'form':form})





@login_required(login_url='account_management:user_login')
def wish_list(request):
    items = WishList.objects.filter(user=request.user)
    context ={
        'items':items
    }

    return render(request,'cart/wishlist.html', context)




def add_to_wish_list(request, id):
    if request.user.is_authenticated:
        product = Product_varients.objects.get(uid=id)
        wish_list_exist = WishList.objects.filter(user=request.user, product=product).exists()
        if wish_list_exist:
            messages.info(request,"Already in the wishlist")
            return redirect('cart:wish_list')
        else:
            wishlist_item = WishList.objects.create(user=request.user, product=product)
            wishlist_item.save()
            return redirect('cart:wish_list')
    else:
        return redirect ('product:shoping_page')



def remove_item_wish_list(request, id):
    product = Product_varients.objects.get(uid = id)
    wish_list = WishList.objects.get(user=request.user, product=product)
    wish_list.delete()
    return redirect('cart:wish_list')



