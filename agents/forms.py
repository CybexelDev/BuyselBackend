from django import forms
# forms.py

from django import forms
from .models import *





class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['phone_number', 'address', 'profile_image','email','pin_code']
        widgets = {
            'phone_number': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter your phone number'
            }),
            'address': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'Enter your address',
                'rows': 3
            }),
             'email': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter your email id'
            }),
            'pin_code': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Add your pincode'
            }),
            'profile_image': forms.ClearableFileInput(attrs={
                'class': 'form-control'
            }),
           

        }

     

