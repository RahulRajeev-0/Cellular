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
def cash_on_delivery(request):
    return render (request, 'orders/cash_on_delivery.html')









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
            payment=payment_object,
            order_total=grand_total,
            tax=tax,
            ip=ip,
            )
        order_object.save()
        

        if request.POST['payment'] == "COD" or 'razorpay' :
            payment_object.payment_method = request.POST['payment']
            payment_object.save()
            order = Order.objects.get(user=current_user, is_ordered=False, order_number=order_number)
            context = {
                'order':order,
                'cart_items':cart_items,
                'total':total,
                'tax':tax,
                'grand_total':grand_total,
            }
            
            return render(request, 'orders/cash_on_delivery.html', context)
        else:
            return HttpResponse('This is not valid')
        

    return redirect('cart:checkout')



   

    