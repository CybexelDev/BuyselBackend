from django import forms
from django.core.validators import RegexValidator
from .models import *
from developer.models import *
from agents.models import *


class PropertyForm(forms.ModelForm):
    # Property name: only letters, numbers, spaces, and basic punctuation
    property_name = forms.CharField(
        max_length=200,
        validators=[
            RegexValidator(
                regex=r'^[\w\s.,!\'"-]{3,255}$',
                message='Property name must contain only letters, numbers, and punctuation.'
            )
        ]
    )

    # Location: letters, spaces, optional commas or dashes
    locations = forms.CharField(
        max_length=255,
        validators=[
            RegexValidator(
                regex=r'^[A-Za-z\s,-]+$',
                message='Location should only contain letters, spaces, commas, or dashes.'
            )
        ]
    )

    # Price: should be numeric with optional decimals
    price = forms.CharField(
        validators=[
            RegexValidator(
                regex=r'^\d+(\.\d{1,2})?$',
                message='Enter a valid price (e.g., 1000 or 1000.00).'
            )
        ]
    )

    # About the property: allow letters, numbers, punctuation (no scripts)
    about_the_property = forms.CharField(
        widget=forms.Textarea,
        validators=[
            RegexValidator(
                regex=r'^[\w\s.,!\'"-]{10,1000}$',
                message='Description must be at least 10 characters and contain only allowed characters.'
            )
        ]
    )

    class Meta:
        model = Propertylist
        fields = '__all__'

    # Additional image validation
    def clean_image(self):
        image = self.cleaned_data.get('image')
        if image:
            if image.content_type not in ['image/jpeg', 'image/png', 'image/gif']:
                raise forms.ValidationError("Only JPEG, PNG, or GIF formats are allowed.")
            if image.size > 5 * 1024 * 1024:  # 5MB max
                raise forms.ValidationError("Image size must be under 5MB.")
        return image



class AgentRegister(forms.ModelForm):
    name = forms.CharField(
        max_length=50,
        validators=[
            RegexValidator(
                regex=r'^[A-Za-z\s]+$',
                message='Name must contain only letters.'
            )
        ]
    )

    email = forms.CharField(
        max_length=50,
        validators=[
            RegexValidator(
                regex=r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$',
                message='Enter a valid email address (e.g., abc@gmail.com).'
            )
        ]
    )

    address = forms.CharField(
        max_length=255,
        widget=forms.Textarea(attrs={'rows': 4, 'placeholder': 'Enter address'}),
        validators=[
            RegexValidator(
                regex=r'^[A-Za-z0-9\s,.-]+$',
                message='Address can only contain letters, numbers, spaces, commas, dots, and hyphens.'
            )
        ]
    )

    phone_number = forms.CharField(
        max_length=10,
        validators=[
            RegexValidator(
                regex=r'^[6-9]\d{9}$',
                message='Enter a valid 10-digit Indian mobile number.'
            )
        ]
    )

    Dealings = forms.CharField(
        max_length=50,
        validators=[
            RegexValidator(
                regex=r'^[A-Za-z\s]+$',
                message='Dealings must contain only letters.'
            )
        ]
    )

    class Meta:
        model = AgentForm
        fields = '__all__'

    # Additional image validation
    def clean_image(self):
        image = self.cleaned_data.get('image')
        if image:
            if image.content_type not in ['image/jpeg', 'image/png', 'image/gif']:
                raise forms.ValidationError("Only JPEG, PNG, or GIF formats are allowed.")
            if image.size > 5 * 1024 * 1024:  # 5MB max
                raise forms.ValidationError("Image size must be under 5MB.")
        return image


import re
from django import forms
from django.core.validators import RegexValidator


class InboxMessages(forms.ModelForm):
    name = forms.CharField(
        max_length=50,
        strip=True,
        validators=[
            RegexValidator(regex=r'^[A-Za-z\s]+$', message='Name must contain only letters.')
        ]
    )

    pin_code = forms.CharField(
        max_length=6,
        validators=[
            RegexValidator(regex=r'^\d{6}$', message='Enter a valid 6-digit PIN code.')
        ]
    )

    contact = forms.CharField(
        max_length=10,
        validators=[
            RegexValidator(regex=r'^[6-9]\d{9}$', message='Enter a valid 10-digit Indian mobile number.')
        ]
    )

    messages_text = forms.CharField(
        max_length=500,
        widget=forms.Textarea,
        validators=[
            RegexValidator(
                regex=r'^[A-Za-z0-9\s,.\'-]+$',
                message='Messages must contain only letters, numbers, or basic punctuation.'
            )
        ]
    )

    def clean_messages_text(self):
        text = self.cleaned_data.get('messages_text')
        sanitized = re.sub(r'[^A-Za-z0-9\s,.\'-]', '', text)
        return sanitized.strip()

    class Meta:
        model = Inbox
        fields = ['name', 'contact', 'pin_code', 'messages_text']
