from django.shortcuts import render
from django.core.exceptions import ObjectDoesNotExist
from django.http import JsonResponse


# ----------------- MODELS ----------------
from wallet.models import Wallet
from account_management.models import Account


# Create your views here.

def apply_wallet(request):
    if request.method == "POST":
        user = request.user
        grand_total =  float(request.POST.get('grandTotal'))  # Convert to float
        new_grand_total = grand_total
        response_data = {}

        try:
            wallet = Wallet.objects.get(user=user)
        except ObjectDoesNotExist:
            wallet = Wallet.objects.create(user=user)

        wallet_balance = wallet.balance
        wallet_discount = min(wallet_balance, grand_total)
        grand_total -= wallet_discount
        wallet_balance -= wallet_discount
        new_grand_total = grand_total
        

        response_data['success'] = True
        response_data['newGrandTotal'] = new_grand_total
        
        return JsonResponse(response_data)
    else:
        return JsonResponse({'success': False, 'message': 'Invalid request method'})
    

def wallet_page(request):
    user = Account.objects.get(email=request.user)
    try:
        wallet_money = Wallet.objects.get(user=user)
    except:
        wallet_money = 0
    context = {
        'user':user,
        'wallet_money':wallet_money,
    }
    return render(request, "account_management/wallet.html", context)