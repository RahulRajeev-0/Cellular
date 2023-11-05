from django.shortcuts import render
from wallet.models import Wallet
from django.core.exceptions import ObjectDoesNotExist
from django.http import JsonResponse

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