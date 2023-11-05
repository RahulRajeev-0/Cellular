from django.shortcuts import render , HttpResponse , redirect ,reverse ,get_object_or_404
import datetime 
from django.contrib import messages
import uuid
import razorpay
from django.utils import timezone
from datetime import datetime, timedelta
from django.db.models import Sum
from django.http import JsonResponse
# ------------------- settings -------------
from django.conf import settings

# --------------------------- models  ---------------------------------
from cart.models import Cart , CartItem
from orders.models import Order , Payment , OrderProduct , Coupon
from account_management.models import userAddressBook
from product.models import Product_varients
from wallet.models import Wallet , WalletTransaction
# -------------------------- forms ---------------------------------















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
        total += (cart_item.product.product_price() * cart_item.quantity)
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
        discount = 0
        coupon_code = request.POST.get('coupon')
        if coupon_code:
            try:
                coupon_obj = Coupon.objects.get(coupon_code=coupon_code)
                grand_total = (total - coupon_obj.discount_price) + tax
                discount = coupon_obj.discount_price
                if grand_total < 0:
                    grand_total = 0
            except:
                discount = 0

        #generating unique number 
        unique_id = uuid.uuid4().hex[:10]  # Generates a random 10-character hexadecimal string
        current_date = datetime.now().strftime("%Y%m%d")
        order_number = f"{current_date}-{unique_id}"

        unique_id_payment = uuid.uuid4().hex[:10]  # Generates a random 10-character hexadecimal string
        current_date = datetime.now().strftime("%Y%m%d")
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
            discount = discount,
            tax=tax,
            ip=ip,
            )
        order_object.save()


    # checking if the user used wallet or not if yes then making the discount 
        if 'use_wallet' in request.POST:
            wallet = Wallet.objects.get(user=request.user)
            wallet_balance = wallet.balance
            wallet_discount = min(wallet_balance, grand_total)
            grand_total -= wallet_discount
            wallet_balance -= wallet_discount
            order_object.order_total = grand_total
            order_object.wallet_discount = wallet_discount
            wallet.balance = wallet_balance
            order_object.save()
            wallet.save()

            transaction = WalletTransaction.objects.create(
                wallet= wallet,
                transaction_type = 'CREDIT',
                transaction_detail = str(order_object.order_number) + "  APPLIED",
                amount = order_object.wallet_discount + order_object.order_total - order_object.discount,
            )
            transaction.save()


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


# def ajax_coupon(request):
#     if request.method == "POST":
#         coupon_code = request.POST.get('couponCode')
#         grand_total = float(request.POST.get('grandTotal'))
#         sub_total = float(request.POST.get('subTotal'))
#         tax = float(request.POST.get('tax'))
#         print("????????????????")
#         print(coupon_code)
#         if coupon_code:
#             try:
#                 coupon = Coupon.objects.get(coupon_code=coupon_code, is_expired=False)
#                 if sub_total >= coupon.minimium_amount:
#                     new_grand_total = (sub_total + tax) - coupon.discount_price 
#                     if new_grand_total < 0:
#                         new_grand_total = 0
#                     response_data = {
#                     'success': True,
#                     'message': 'Coupon applied successfully!',
#                     'newGrandTotal':new_grand_total,
#                 }
#                     return JsonResponse(response_data)
#                 else:
#                     new_grand_total = (sub_total + tax)
#                     response_data = {
#                         'success': False,
#                         'message': '"Oops! Coupon not applied. Please check the code and try again."!',
#                         'newGrandTotal':new_grand_total,
#                     }
#                     return JsonResponse(response_data)
#             except:
#                 print("+++++++++")
#                 new_grand_total = (sub_total + tax)
#                 response_data = {
#                 'success': False,
#                 'newGrandTotal':new_grand_total,
#                 'message': 'Invalid coupon code. Please try again with a valid code.',
#                 'error':'Invalid request',
#             }
#                 return JsonResponse(response_data, status=400)
#         else:
#             new_grand_total = (sub_total + tax)
#             response_data = {
#                 'success': False,
#                 'message': 'Invalid request',
#                  'newGrandTotal':new_grand_total,
#             }
#             return JsonResponse(response_data, status=400)

def ajax_coupon(request):
    if request.method == "POST":
        coupon_code = request.POST.get('couponCode')
        sub_total = float(request.POST.get('subTotal'))
        grand_total = float(request.POST.get('grandTotal')) 
        tax = float(request.POST.get('tax'))
        
        # Initialize new_grand_total with default values
        new_grand_total = sub_total + tax
        message = "Not applied"
        success = False
        
        if coupon_code:
            try:
                coupon = Coupon.objects.get(coupon_code=coupon_code, is_expired=False)
                if grand_total >= coupon.minimium_amount:
                    new_grand_total = (sub_total + tax) - coupon.discount_price 
                    message = "Coupon applied successfully!"
                    success = True
                    if new_grand_total < 0:
                        new_grand_total = 0
                else:
                    message = "Oops! Coupon not applied. Does not meet the minimum amount ."
                    success = False
            except Coupon.DoesNotExist:
                message = "Invalid coupon code. Please try again with a valid code."
                success = False
            if " " in coupon_code:
                message = "Code doesn't contains space"
                success = False
        
        response_data = {
            'success': success,
            'message': message,
            'newGrandTotal': new_grand_total,
        }
        return JsonResponse(response_data)
    



        







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
        price = cart_item.product.product_price()
        ordered_product = OrderProduct.objects.create(
            order=order_object,
            user=current_user,
            product=product,
            quantity=quantity,
            product_price=price,
            ordered=True,
            
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
    discount = order_object.discount
    total =order_object.order_total
    context = {
        'order_products':order_products,
        'date':date,
        'order_no':order_no,
        'pay_method':pay_method,
        'address':address,
        'tax':tax,
        'total':total,
        'discount':discount,
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
        price = cart_item.product.product_price()
        ordered_product = OrderProduct.objects.create(
            order=order_object,
            user=current_user,
            product=product,
            quantity=quantity,
            product_price=price,
            ordered=True,
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
    orders = Order.objects.filter(user=request.user, is_ordered=True).order_by('-created_at')
    
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
    # add money to wallet 
    if order.payment.payment_method == "Razorpay" or order.payment.payment_method == "Razor Pay" or order.wallet_discount != 0:
         user = order.user
    # adding the order total amount back to the users wallet 
         wallet = Wallet.objects.get(user=user)
         if order.payment.payment_method == "COD":
            wallet.balance += order.wallet_discount
            amount = order.wallet_discount
         else:
            wallet.balance += order.order_total + order.wallet_discount - order.discount
            amount = order.order_total + order.wallet_discount - order.discount
         wallet.save()
    # creating transaction details for the returned amount back to the wallet 
         transaction = WalletTransaction.objects.create(
        wallet= wallet,
        transaction_type = 'CREDIT',
        transaction_detail = str(order.order_number) + "  CANCELLED",
        amount = amount,
          )
         transaction.save()

    order_products = OrderProduct.objects.filter(order=order)
    for order_product in order_products:
        product = Product_varients.objects.get(uid=order_product.product.uid)
        product.stock_qty += order_product.quantity 
        product.save()
    return redirect("orders:order_details_user", id=order.order_number)







def user_order_return(request,id):
    order = Order.objects.get(order_number=id)
    order.status = "Return"
    order.save()
    return redirect("orders:order_listing_user", id=order.order_number)












def get_weekly_sales():
    end_date = timezone.now()
    start_date = end_date - timezone.timedelta(days=7)

    return OrderProduct.objects.filter(
        order__created_at__range=(start_date, end_date)
    ).values('product__product_heading').annotate(weekly_sales=Sum('quantity'))




def get_monthly_sales():
    end_date = timezone.now()
    start_date = end_date - timezone.timedelta(days=30)

    return OrderProduct.objects.filter(
        order__created_at__range=(start_date, end_date)
    ).values('product__product_heading').annotate(monthly_sales=Sum('quantity'))




def get_yearly_sales():
        end_date = timezone.now()
        start_date = end_date - timezone.timedelta(days=365)

        return OrderProduct.objects.filter(
            order__created_at__range=(start_date, end_date)
        ).values('product__product_heading').annotate(yearly_sales=Sum('quantity')) 


def sales_report(request):
    weekly_sales_data = list(get_weekly_sales().values('product__product_heading','weekly_sales'))  # Convert QuerySet to a list of dictionaries
    monthly_sales_data = list(get_monthly_sales().values('product__product_heading','monthly_sales'))
    yearly_sales_data = list(get_yearly_sales().values('product__product_heading','yearly_sales'))
    sales_data = {
        'weekly_sales': weekly_sales_data,
        'monthly_sales': monthly_sales_data,
        'yearly_sales': yearly_sales_data,
    }
    
    
    return JsonResponse(sales_data, safe=False)


