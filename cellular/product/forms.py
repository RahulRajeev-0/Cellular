from django import forms
from django.forms import ModelForm
from .models import Brand,Product

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
             #'price':forms.IntegerField(attrs={'class':'form-control'}),
             #'product_description':forms.TextInput(),
             'color_varient':forms.CheckboxSelectMultiple,
             'ram_varient':forms.CheckboxSelectMultiple,

         }