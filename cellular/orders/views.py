from django.shortcuts import render , HttpResponse , redirect
import datetime 
from django.contrib import messages
import uuid


# --------------------------- models  ---------------------------------
from cart.models import Cart , CartItem
from orders.models import Order , Payment
from account_management.models import userAddressBook
# -------------------------- forms -----------------------------------






# Create your views here.




# def place_order(request , total = 0 , quantity = 0):
#     current_user = request.user

#     # if the cart count is less than zero then redirect back  to shop 
#     cart_items = CartItem.objects.filter(user=current_user)
#     cart_count = cart_items.count()
#     if cart_count <= 0:
#         return redirect('product:shoping_page')
    
#     grand_total = 0
#     tax = 0 
#     for cart_item in cart_items:
#         total += (cart_item.product.price * cart_item.quantity)
#         quantity += cart_item.quantity 

#     tax = ( 2 * total)/100
#     grand_total = total + tax

#     try :
#         address = userAddressBook.objects.get(user=request.user , is_default=True)
#     except Exception as e:
        
#         print(e)
#         messages.warning(request, 'please select or add an address')
#         return redirect ('cart:checkout')


#     if request.method == "POST":
#         form = OrderForm(request.POST)
#         form.shipping_address = address
#         if form.is_valid():
#             # store all the billing information inside the order table 
#             data = Order()
#             # data.shipping_address = address
#             data.order_total = grand_total
#             data.tax = tax
#             data.ip = request.META.get('REMOTE_ADDR')
#             data.save()
#             # Generate order number 
#             yr = int(datetime.data.today().shrftime('%Y'))
#             dt = int(datetime.data.today().shrftime('%d'))
#             mt = int(datetime.data.today().shrftime('%m'))
#             d = datetime.date(yr, mt , dt)
#             current_date = d.strftime("%Y%m%d")
#             order_number = current_date + str(data.id)
#             data.order_number = order_number
#             data.save()
#             return redirect("cart:checkout")
#         else:
#             print("-----------")
#             print(form.errors)
#     else:
#         return redirect('cart:checkout')





def place_order(request):
    current_user = request.user

    # if the cart count is less than zero then redirect back to shop 
    cart_items = CartItem.objects.filter(user=current_user)
    cart_count = cart_items.count()
    if cart_count <= 0:
        return redirect('product:shoping_page')
    
    total = 0
    quantity = 0
    for cart_item in cart_items:
        total += (cart_item.product.price * cart_item.quantity)
        quantity += cart_item.quantity 

    tax = (2 * total) / 100
    grand_total = total + tax

    try:
        address = userAddressBook.objects.get(user=request.user, is_default=True)
    except userAddressBook.DoesNotExist:
        messages.warning(request, 'Please select or add an address')
        return redirect('cart:checkout')

    if request.method == "POST":
        ip = request.META.get('REMOTE_ADDR')

        #generating unique number 
        unique_id = uuid.uuid4().hex[:10]  # Generates a random 10-character hexadecimal string
        current_date = datetime.datetime.now().strftime("%Y%m%d")
        order_number = f"{current_date}-{unique_id}"

        #payment model
        payment_object = Payment.objects.create(
            user=current_user,
            payment_order_id=order_number,
            amount_paid=grand_total,
            payment_status='PENDING',
            )

        #order model
        order_object = Order.objects.create(
            user=current_user,
            order_number=order_number,
            shipping_address=address,
            order_total=grand_total,
            tax=tax,
            ip=ip,
            )
        order_object.save()
        

        if request.POST['payment'] == "COD" or 'razorpay' :
            payment_object.payment_method = request.POST['payment']
            payment_object.save()
            return redirect('cart:checkout')
        else:
            return HttpResponse('This is not valid')
        

    return redirect('cart:checkout')



   

    