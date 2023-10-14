from django import forms
from django.forms import ModelForm
from categoryManagement.models import Category


# forms here


class CategoryForm(ModelForm):
    class Meta :
        model = Category
        fields = '__all__'

        widgets = {
            'cate_name':forms.TextInput(attrs={'class':'form-control'}),
            
        }




