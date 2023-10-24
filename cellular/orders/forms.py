from django import forms
from orders.models import Coupon

class CouponForm(forms.ModelForm):
    
    class Meta:
        model = Coupon
        fields = '__all__'

        widgets = {
            'coupon_code':forms.TextInput(attrs={'class':'form-control'}),
            'discount_price':forms.TextInput(attrs={'class':'form-control'}),
            'expiration_date':forms.TextInput(attrs={'class':'form-control'}),
            'minimium_amount':forms.TextInput(attrs={'class':'form-control'}),
        }

