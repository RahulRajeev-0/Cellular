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


# function to add the cart items using adjax 

def add_to_cart_ajax(request):
    if request.method == "POST":
        if request.user.is_authenticated:
            prod_id = request.POST.get('product_id')
            product_check = Product_varients.objects.get(uid=prod_id)
            if (product_check):
                if (CartItem.objects.filter(user=request.user , product=product_check)):
                    return JsonResponse({'status':"product already in cart "})
                else:
                    prod_qty = int(request.POST.get('product_qty'))

                    if product_check.stock_qty >= prod_qty:
                        CartItem.objects.create(user=request.user , product= product_check , quantity=prod_qty)
                        return JsonResponse({"status":"Product add sessuccfully "})
                    else:
                        return JsonResponse({'status':"Only "+str(product_check.stock_qty)+" this number of quantity available" })
            else:
                return JsonResponse({"status":'NO such product found '})
            
        else:
            return JsonResponse({'status':"Login to continue ! "})









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
            total += (cart_item.product.price * cart_item.quantity)
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
    product = Product_varients.objects.get(uid=id)
    wish_list_exist = WishList.objects.filter(user=request.user, product=product).exists()
    if wish_list_exist:
        messages.info(request,"Already in the wishlist")
        return redirect('cart:wish_list')
    else:
        wishlist_item = WishList.objects.create(user=request.user, product=product)
        wishlist_item.save()
        return redirect('cart:wish_list')



def remove_item_wish_list(request, id):
    product = Product_varients.objects.get(uid = id)
    wish_list = WishList.objects.get(user=request.user, product=product)
    wish_list.delete()
    return redirect('cart:wish_list')

