from django import forms
from django.core.validators import RegexValidator
from .models import *
from developer.models import *
from agents.models import *
from django.core.exceptions import ValidationError


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
    AGENT_TYPES = [
        ('basic', 'Basic Agent'),
        ('premium', 'Premium Agent'),
        ('elite', 'Elite Agent'),
    ]

    username = forms.CharField(
        max_length=50,
        validators=[
            RegexValidator(
                regex=r'^[A-Za-z\s]+$',
                message='Name must contain only letters.'
            )
        ]
    )

    password = forms.CharField(
        widget=forms.PasswordInput(attrs={'placeholder': 'Enter password'}),
        min_length=6
    )

    email = forms.CharField(
        max_length=50,
        validators=[
            RegexValidator(
                regex=r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$',
                message='Enter a valid email address.'
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

    pin_code = forms.CharField(
        max_length=6,
        validators=[
            RegexValidator(
                regex=r'^\d{6}$',
                message='Enter a valid 6-digit PIN code.'
            )
        ]
    )

    professional_bio = forms.CharField(
        required=False,
        widget=forms.Textarea(attrs={'rows': 3, 'placeholder': 'Enter professional bio'})
    )

    operating_cities = forms.CharField(
        required=False,
        max_length=255
    )

    agent_type = forms.ChoiceField(
        choices=AGENT_TYPES,
        widget=forms.Select(attrs={'class': 'form-control'}),
        label="Agent Membership"
    )

    premium_plan = forms.ModelChoiceField(
        queryset=PremiumPlan.objects.all(),
        required=False,
        empty_label="Select Premium Plan"
    )

    elite_plan = forms.ModelChoiceField(
        queryset=ElitePlan.objects.all(),
        required=False,
        empty_label="Select Elite Plan"
    )

    class Meta:
        model = AgentUserProfile
        fields = [
            'username',
            'password',
            'email',
            'phone_number',
            'address',
            'pin_code',
            'profile_image',
            'is_agent',
            'agent_type',
            'paid',
            'professional_bio',
            'specializations',
            'operating_cities',
            'social_media',
            'premium_plan',
            'elite_plan',
        ]
        widgets = {
            'specializations': forms.TextInput(attrs={'placeholder': 'Example: ["residential","commercial"]'}),
            'social_media': forms.TextInput(attrs={'placeholder': 'Example: {"instagram":"agent","facebook":"agentfb"}'}),
        }

    def clean_username(self):
        username = self.cleaned_data.get('username', '').strip()
        username = re.sub(r'\s+', ' ', username)
        return username

    def clean_profile_image(self):
        image = self.cleaned_data.get('profile_image')
        if image:
            if hasattr(image, 'content_type'):
                if image.content_type not in ['image/jpeg', 'image/png', 'image/gif', 'image/webp']:
                    raise ValidationError("Only JPEG, PNG, GIF, or WEBP formats are allowed.")
            if image.size > 5 * 1024 * 1024:
                raise ValidationError("Image size must be under 5MB.")
        return image

    def clean(self):
        cleaned_data = super().clean()
        agent_type = cleaned_data.get("agent_type")
        premium_plan = cleaned_data.get("premium_plan")
        elite_plan = cleaned_data.get("elite_plan")

        if agent_type == "premium":
            if not premium_plan:
                self.add_error("premium_plan", "Please select a premium plan.")
            cleaned_data["elite_plan"] = None

        elif agent_type == "elite":
            if not elite_plan:
                self.add_error("elite_plan", "Please select an elite plan.")
            cleaned_data["premium_plan"] = None

        else:
            cleaned_data["premium_plan"] = None
            cleaned_data["elite_plan"] = None

        return cleaned_data

    def save(self, commit=True):
        agent = super().save(commit=False)
        password = self.cleaned_data.get("password")
        if password:
            agent.set_password(password)

        if commit:
            agent.save()
            self.save_m2m()

        return agent



import re
from django import forms
from django.core.validators import RegexValidator


class InboxMessages(forms.ModelForm):
    name = forms.CharField(
        max_length=50,
        strip=True,
        validators=[
            RegexValidator(
                regex=r'^[A-Za-z\s]+$',
                message='Name must contain only letters.'
            )
        ]
    )

    pin_code = forms.CharField(
        max_length=6,
        validators=[
            RegexValidator(
                regex=r'^\d{6}$',
                message='Enter a valid 6-digit PIN code.'
            )
        ]
    )

    contact = forms.CharField(
        max_length=10,
        validators=[
            RegexValidator(
                regex=r'^[6-9]\d{9}$',
                message='Enter a valid 10-digit Indian mobile number.'
            )
        ]
    )

    messages_text = forms.CharField(
        max_length=500,
        widget=forms.Textarea(attrs={
            "rows": 4,
            "placeholder": "Enter your message"
        }),
        validators=[
            RegexValidator(
                regex=r"^[A-Za-z0-9\s,.\'-]+$",
                message='Messages must contain only letters, numbers, or basic punctuation.'
            )
        ]
    )

    class Meta:
        model = Inbox
        fields = ['name', 'contact', 'pin_code', 'messages_text']

    def clean_name(self):
        name = self.cleaned_data.get("name", "").strip()
        return re.sub(r'\s+', ' ', name)

    def clean_pin_code(self):
        pin_code = self.cleaned_data.get("pin_code", "").strip()
        return pin_code

    def clean_contact(self):
        contact = self.cleaned_data.get("contact", "").strip()
        return contact

    def clean_messages_text(self):
        text = self.cleaned_data.get("messages_text", "").strip()
        sanitized = re.sub(r"[^A-Za-z0-9\s,.\'-]", "", text)
        sanitized = re.sub(r'\s+', ' ', sanitized)
        return sanitized