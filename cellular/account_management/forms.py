from django import forms
from django.forms import ModelForm
from account_management.models import HomeMainSlide, HomeSubBanner , userAddressBook




#------=============== forms ===================-----------

# address book  form

class userAddressBookForm(ModelForm):
    class Meta:
        model = userAddressBook
        fields = '__all__'
        exclude = ('user','is_default','is_active')
        widgets = {
            # 'user':forms.Select(attrs={'class':'form-control'}),
            'name':forms.TextInput(attrs={'class':'form-control'}),
            'phone':forms.TextInput(attrs={'class':'form-control'}),
            'address_line_1':forms.TextInput(attrs={'class':'form-control'}),
            'address_line_2':forms.TextInput(attrs={'class':'form-control'}),
            'country':forms.TextInput(attrs={'class':'form-control'}),
            'state':forms.TextInput(attrs={'class':'form-control'}),
            'city':forms.TextInput(attrs={'class':'form-control'}),
            'pincode':forms.TextInput(attrs={'class':'form-control'}),
            'is_default':forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'is_active':forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }



class HomeMainSliderForm(ModelForm):
    class Meta:
        model = HomeMainSlide
        fields = '__all__'

        widgets = {
            'heading':forms.TextInput(attrs={'class':'form-control'}),
            'subheading':forms.TextInput(attrs={'class':'form-control'}),
            

        }


class HomeSubBannerForm(ModelForm):
    class Meta:
        model = HomeSubBanner
        fields = '__all__'

        widgets = {
            'heading':forms.TextInput(attrs={'class':'form-control'}),
            'sub_heading':forms.TextInput(attrs={'class':'form-control'}),
            

        }
        
