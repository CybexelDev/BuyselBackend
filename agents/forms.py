from django import forms
# forms.py

from django import forms
from .models import *





AGENT_TYPE_CHOICES = [
    ('basic', 'Basic Agent'),
    ('premium', 'Premium Agent'),
    ('elite', 'Elite Agent'),
]

class PendingAgentRegistrationForm(forms.ModelForm):
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={'placeholder': 'Enter password'}),
        required=True
    )

    class Meta:
        model = PendingAgentRegistration
        fields = [
            'full_name',
            'email',
            'phone_number',
            'password',
            'city',
            'pin_code',
            'agent_type',
            'plan_name',
            'address'
        ]
        widgets = {
            'full_name': forms.TextInput(attrs={'placeholder': 'Full Name'}),
            'email': forms.EmailInput(attrs={'placeholder': 'Email'}),
            'phone_number': forms.TextInput(attrs={'placeholder': 'Phone Number'}),
            'city': forms.TextInput(attrs={'placeholder': 'City'}),
            'pin_code': forms.NumberInput(attrs={'placeholder': 'Pin Code'}),
            'agent_type': forms.Select(choices=AGENT_TYPE_CHOICES),
            'plan_name': forms.TextInput(attrs={'placeholder': 'Plan Name (if applicable)'}),
            'address': forms.Textarea(attrs={'placeholder': 'Full Address', 'rows': 3}),
        }

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if PendingAgentRegistration.objects.filter(email=email).exists():
            raise forms.ValidationError("You have already submitted a registration request with this email.")







class AgentUserProfileForm(forms.ModelForm):

    specializations = forms.ModelMultipleChoiceField(
        queryset=Category.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=False
    )

    operating_cities = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter cities (comma separated)'
        })
    )

    class Meta:
        model = AgentUserProfile
        fields = [
            'phone_number',
            'email',
            'address',
            'pin_code',
            'profile_image',
            'professional_title',
            'professional_bio',
            'operating_cities',
            'specializations',
            'instagram',
            'facebook',
            'website',   # ✅ added
            'agent_type',
        ]

    def clean_operating_cities(self):
        cities = self.cleaned_data.get('operating_cities')
        if cities:
            return [city.strip() for city in cities.split(',')]
        return []




# users/forms.py
from django import forms
from .models import AgentProperty, AgentPropertyImage

class MultipleFileInput(forms.ClearableFileInput):
    """Custom widget that supports multiple file upload"""
    allow_multiple_selected = True


class AgentPropertyForm(forms.ModelForm):
    # Multiple images upload
    images = forms.FileField(
        widget=MultipleFileInput(),
        required=False
    )

    # Amenities as a comma-separated string
    amenities = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={'placeholder': 'Comma separated, e.g., pool,gym,garden'})
    )

    # Selling points as a comma-separated string
    selling_points = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={'placeholder': 'Comma separated, e.g., Near park,Good view'})
    )

    # Landmarks as JSON string (list of dicts)
    landmarks = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={'placeholder': 'JSON format, e.g., [{"name":"near school","distance":"0.5 km"}]'})
    )

    class Meta:
        model = AgentProperty
        fields = [
            'label', 'land_area', 'sq_ft', 'description',
            'category', 'purpose', 'price', 'perprice',
            'location', 'city', 'pincode', 'district',
            'land_mark', 'owner', 'taluk', 'village', 'state',
            'paid', 'notes', 'image', 'screenshot', 'amenities', 'images',
            'selling_points', 'landmarks'
        ]
        widgets = {
            'description': forms.Textarea(attrs={'rows': 3}),
            'notes': forms.Textarea(attrs={'rows': 2}),
            'paid': forms.CheckboxInput(),
        }

    def save(self, commit=True, agent=None):
        images = self.cleaned_data.pop('images', [])
        amenities = self.cleaned_data.pop('amenities', '')
        selling_points = self.cleaned_data.pop('selling_points', '')
        landmarks_str = self.cleaned_data.pop('landmarks', '')

        # Save amenities as comma-separated string or many-to-many if you use separate model
        if amenities:
            self.instance.amenities = ",".join([a.strip() for a in amenities.split(",")])

        if agent:
            self.instance.agent = agent
            self.instance.phone = agent.phone_number
            self.instance.whatsapp = agent.whatsapp_number

        property_obj = super().save(commit=commit)

        # Save images
        for img in images:
            AgentPropertyImage.objects.create(property=property_obj, image=img)

        # Save selling points (comma-separated)
        if selling_points:
            for sp in [s.strip() for s in selling_points.split(",") if s.strip()]:
                property_obj.selling_points.create(point=sp)

        # Save landmarks (JSON string)
        if landmarks_str:
            import json
            try:
                landmarks_list = json.loads(landmarks_str)
                for lm in landmarks_list:
                    if isinstance(lm, dict):
                        property_obj.landmarks.create(**lm)
            except json.JSONDecodeError:
                pass  # invalid JSON, ignore or raise error

        return property_obj