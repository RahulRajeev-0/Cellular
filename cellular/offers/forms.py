from django.forms import ModelForm
from django import forms

# imported models in here 
from offers.models import ProductOffer



# Product offer form 


class DateInput(forms.DateInput):
    input_type = 'date'


class CreateProductOfferForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'
            
        self.fields['is_active'].widget.attrs['class'] = ''  
        self.fields['product'].widget.attrs['class'] = 'select'  
    class Meta:
        model = ProductOffer
        fields = '__all__'
        exclude = ['product_offer_slug',]
        widgets = {
            'expire_date': DateInput(),
        }
        
