from django import forms
from orders.models import Coupon

class DateInput(forms.DateInput):
    input_type = 'date'

class CouponForm(forms.ModelForm):

    def __init__(self,*args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'

        self.fields['is_expired'].widget.attrs['class'] = 'sd'
        self.fields['expiration_date'].widget = DateInput()
        self.fields['expiration_date'].widget.attrs['class'] = 'form-control'

    class Meta:
        model = Coupon
        fields = '__all__'

        widgets = {
            # 'coupon_code':forms.TextInput(attrs={'class':'form-control'}),
            # 'discount_price':forms.TextInput(attrs={'class':'form-control'}),
            # 'expiration_date':forms.TextInput(attrs={'class':'form-control'}),
            # 'minimium_amount':forms.TextInput(attrs={'class':'form-control'}),
            # 'expiration_date': DateInput(),
        }

