from django import forms
from django.forms import ModelForm
from account_management.models import HomeMainSlide




#------=============== forms ===================-----------





class HomeMainSliderForm(ModelForm):
    class Meta:
        model= HomeMainSlide
        fields='__all__'

        widgets={
            'heading':forms.TextInput(attrs={'class':'form-control'}),
            'subheading':forms.TextInput(attrs={'class':'form-control'}),
            

        }

