from django import forms
# forms.py

from django import forms
from .models import *




class AgentUserProfileForm(forms.ModelForm):
    SPECIALIZATION_CHOICES = [
        ('residential', 'Residential'),
        ('plot_land', 'Plot/Land'),
        ('industrial', 'Industrial'),
        ('commercial', 'Commercial'),
    ]

    AGENT_TYPE_CHOICES = [
        ('basic', 'Basic Agent'),
        ('premium', 'Premium Agent'),
        ('elite', 'Elite Agent'),
    ]

    specializations = forms.MultipleChoiceField(
        choices=SPECIALIZATION_CHOICES,
        widget=forms.CheckboxSelectMultiple,
        required=False
    )

    social_media = forms.JSONField(
        required=False,
        widget=forms.Textarea(attrs={
            'class': 'form-control',
            'placeholder': 'Enter social media links in JSON format, e.g. {"facebook": "url", "instagram": "url"}',
            'rows': 3
        })
    )

    agent_type = forms.ChoiceField(
        choices=AGENT_TYPE_CHOICES,
        widget=forms.Select(attrs={'class': 'form-control'})
    )

    class Meta:
        model = AgentUserProfile
        fields = [
            'phone_number',
            'address',
            'profile_image',
            'email',
            'pin_code',
            'professional_title',
            'professional_bio',
            'operating_cities',
            'specializations',
            'social_media',
            'agent_type',
        ]
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
            'professional_title': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter your professional title'
            }),
            'professional_bio': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'Write a short professional bio',
                'rows': 3
            }),
            'operating_cities': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter cities you operate in (comma separated)'
            }),
        }  



