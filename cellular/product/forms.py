from django import forms
from django.forms import ModelForm
from .models import Brand, Product, RamVarient, ColorVarient , Product_varients , ProductImage

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
             'brand':forms.Select(attrs={'class':'form-control'}),
             

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

class Product_varientsForm(ModelForm):
    class Meta:
        model = Product_varients
        fields = '__all__'

        widgets = {
            'product':forms.Select(attrs={'class':'form-control'}),
            'product_heading': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
            'model_id':forms.TextInput(attrs={'class':'form-control'}),
            'ram':forms.Select(attrs={'class':'form-control'}),
            'color':forms.Select(attrs={'class':'form-control'}),
            'product_detailed_description':forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
            'price':forms.TextInput(attrs={'class':'form-control'}),
            'stock_qty':forms.TextInput(attrs={'class':'form-control'}),
            'is_active': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            # 'thumbnail': forms.ImageField(attrs={'class': 'form-control-file', 'style': 'margin-top: 10px;'})

        }

class ProductVarientImageForm(ModelForm):
    class Meta:
        model = ProductImage
        fields = "__all__"

    widgets = {
        'product':forms.Select(attrs={'class':'form-control'}),
    }