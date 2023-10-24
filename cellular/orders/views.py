from django.shortcuts import render , HttpResponse , redirect ,reverse ,get_object_or_404
import datetime 
from django.contrib import messages
import uuid
import razorpay

# ------------------- settings -------------
from django.conf import settings

# --------------------------- models  ---------------------------------
from cart.models import Cart , CartItem
from orders.models import Order , Payment , OrderProduct
from account_management.models import userAddressBook
from product.models import Product_varients
# -------------------------- forms -----------------------------------
















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

        unique_id_payment = uuid.uuid4().hex[:10]  # Generates a random 10-character hexadecimal string
        current_date = datetime.datetime.now().strftime("%Y%m%d")
        order_number = f"{current_date}-{unique_id_payment}"
        payment_id=unique_id_payment

        #payment model
        payment_object = Payment.objects.create(
            user=current_user,
            payment_order_id=order_number,
            amount_paid=grand_total,
            payment_status='PENDING',
            payment_id=payment_id,
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
        
        request.session['pay_id']=payment_id
        if request.POST['payment'] == "COD" or 'Razorpay' :
            payment_object.payment_method = request.POST['payment']
            payment_object.save()
            print("----------------\n",payment_object.payment_method)
            order = Order.objects.get(user=current_user, is_ordered=False, order_number=order_number)

            # -------razorpay code -------- 
            amount = int(grand_total)
            client = razorpay.Client(auth=(settings.KEY , settings.SECRET))
            payment =client.order.create({
                'amount':amount * 100,
                'currency':'INR',
                'payment_capture':1 
                })
            print("--------------++++++++++++---------------")
            print(payment)
            payment_object.rayzor_pay_order_id=payment['id']
            payment_object.save()
            
            # creating success url
            success_url = request.build_absolute_uri(reverse('orders:success'))
            context = {
                'order':order,
                'cart_items':cart_items,
                'total':total,
                'tax':tax,
                'grand_total':grand_total,
                'payment':payment,
                'success_url':success_url,
            }
            
            return render(request, 'orders/product_review_payment.html', context)
        else:
            return HttpResponse('This is not valid')
        

    return redirect('cart:checkout')










# ------------------------------------ function for cash on delivery ------------------------------------------

def cash_on_delivery(request):
    current_user = request.user
    cart_items = CartItem.objects.select_related('cart').filter(user = current_user)
    pay_id = request.session['pay_id']
    
    #payment table 
    payment_object = Payment.objects.get(payment_id=pay_id)
    payment_object.payment_status = "SUCCESS"
    payment_object.save()


    # order details
    order_object = Order.objects.get(order_number=payment_object.payment_order_id)
    order_object.order_status = "Accepted"
    order_object.is_ordered = True
    order_object.save()

    for cart_item in cart_items:
        quantity = cart_item.quantity
        product = cart_item.product
        price = cart_item.product.price
        ordered_product = OrderProduct.objects.create(
            order=order_object,
            user=current_user,
            product=product,
            quantity=quantity,
            product_price=price,
            )
        ordered_product.save()
        product_vareint = Product_varients.objects.get(uid=cart_item.product.uid)
        product_vareint.stock_qty -= cart_item.quantity
        product_vareint.save()
    cart_items.delete()
    order_products = OrderProduct.objects.filter(order=order_object)
    date = order_object.updated_at
    order_no = order_object.order_number
    pay_method = order_object.payment.payment_method
    address = order_object.shipping_address
    tax = order_object.tax
    total =order_object.order_total
    context = {
        'order_products':order_products,
        'date':date,
        'order_no':order_no,
        'pay_method':pay_method,
        'address':address,
        'tax':tax,
        'total':total,
    }
    
    return render(request, 'orders/success.html', context)



def success (request):
    order_id = request.GET.get('order_id')
    

    current_user = request.user
    pay_id = request.session['pay_id']
    cart_items = CartItem.objects.select_related('cart').filter(user = current_user)
    payment_object = Payment.objects.get(payment_order_id=order_id)
    payment_object.payment_status = "SUCCESS"
    # payment_object.rayzor_pay_payment_id = request.GET.get('payment_id')
    # payment_object.rayzor_pay_payment_signature = request.Get.get('payment_sign')
    payment_object.save()

    #order details
    order_object = Order.objects.get(order_number=payment_object.payment_order_id)
    order_object.order_status = "Accepted"
    order_object.is_ordered = True
    order_object.save()
    details = cart_items
    for cart_item in cart_items:
        quantity = cart_item.quantity
        product = cart_item.product
        price = cart_item.product.price
        ordered_product = OrderProduct.objects.create(
            order=order_object,
            user=current_user,
            product=product,
            quantity=quantity,
            product_price=price,
            )
        ordered_product.save()
        product_vareint = Product_varients.objects.get(uid=cart_item.product.uid)
        product_vareint.stock_qty -= cart_item.quantity
        product_vareint.save()
    cart_items.delete()
    order_products = OrderProduct.objects.filter(order=order_object)
    date = order_object.updated_at
    order_no = order_object.order_number
    pay_method = order_object.payment.payment_method
    address = order_object.shipping_address
    tax = order_object.tax
    total =order_object.order_total
    context = {
        'order_products':order_products,
        'date':date,
        'order_no':order_no,
        'pay_method':pay_method,
        'address':address,
        'tax':tax,
        'total':total,
    }
    
    return render(request,'orders/success.html', context)
    
    



# -------------------------------  user order listing  -------------------------------

def order_listing_user(request):
    orders = Order.objects.filter(user=request.user, is_ordered=True)
    
    context = {
        'orders':orders,
    }
    return render(request, 'orders/order_listing.html', context)


def order_details_user(request,id):
    order = Order.objects.get(order_number=id)
    total = order.order_total
    tax = order.tax
    products = OrderProduct.objects.filter(order=order)
    context = {
        'order':order,
        'total':total,
        'tax':tax,
        'products':products,

    }
    return render (request, 'orders/order_details.html',context)
   




# order cancel by user 
def user_order_cancel(request,id):
    order = Order.objects.get(order_number=id)
    order.status = "Cancel"
    order.save()
    return redirect("orders:order_details_user")

def user_order_return(request,id):
    order = Order.objects.get(order_number=id)
    order.status = "Return"
    order.save()
    return redirect("orders:order_listing_user")