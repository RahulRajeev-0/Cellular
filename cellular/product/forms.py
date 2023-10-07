from django import forms
from django.forms import ModelForm
from .models import Brand, Product, RamVarient, ColorVarient

class BrandForm(ModelForm):
    class Meta:
        model=Brand
        fields='__all__'

        widgets={
            'brand_name':forms.TextInput(attrs={'class':'form-control'}),
            'slug':forms.TextInput(attrs={'class':'form-control'}),
            #'is_active':forms.BooleanField()
            # 'brand_image':forms.ImageField()

        }

class ProductForm(ModelForm):
    class Meta:
        model=Product
        fields='__all__'

        widgets={
            'product_name':forms.TextInput(attrs={'class':'form-control'}),
             'slug':forms.TextInput(attrs={'class':'form-control'}),
             'brand':forms.CheckboxSelectMultiple,
             

         }
        

class RamForm(ModelForm):
    class Meta:
        model =  RamVarient
        fields = "__all__"

        widgets = {
            'ram_no':forms.TextInput(attrs={'class':'form-control'}),
        }

class ColorForm(ModelForm):
    class Meta:
        model = ColorVarient
        fields = '__all__'

        widgets = { 
            'color_name':forms.TextInput(attrs={'class':'form-control'}),
        }