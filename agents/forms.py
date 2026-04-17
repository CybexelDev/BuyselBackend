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
        model = PendingAgentRegistration
        fields = [
            'full_name',
            'email',
            'phone_number',
            'password',
            'city',
            'pin_code',
            'agent_type',
            'premium_plan',
            'elite_plan',
            'address'
        ]

        widgets = {
            'full_name': forms.TextInput(attrs={'placeholder': 'Full Name'}),
            'email': forms.EmailInput(attrs={'placeholder': 'Email'}),
            'phone_number': forms.TextInput(attrs={'placeholder': 'Phone Number'}),
            'city': forms.TextInput(attrs={'placeholder': 'City'}),
            'pin_code': forms.NumberInput(attrs={'placeholder': 'Pin Code'}),
            'agent_type': forms.Select(choices=AGENT_TYPE_CHOICES),
            'address': forms.Textarea(attrs={'placeholder': 'Full Address', 'rows': 3}),
        }

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if PendingAgentRegistration.objects.filter(email=email).exists():
            raise forms.ValidationError("You have already submitted a registration request with this email.")
        return email


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


class MultipleFileInput(forms.ClearableFileInput):
    """Custom widget that supports multiple file upload"""
    allow_multiple_selected = True

class AgentPropertyForm(forms.ModelForm):

    images = forms.FileField(
        widget=MultipleFileInput(),
        required=False
    )

    amenities_input = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={
            'placeholder': 'Comma separated: pool,gym,garden'
        })
    )

    selling_points_input = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={
            'placeholder': 'Comma separated: Near park,Good view'
        })
    )

    landmarks_input = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={
            'placeholder': '[{"name":"school","distance":"1km"}]'
        })
    )

    class Meta:
        model = AgentProperty
        fields = [
            'label', 'land_area', 'sq_ft', 'description',
            'category', 'purpose', 'price', 'perprice',
            'location', 'city', 'pincode', 'district',
            'land_mark', 'owner', 'taluk', 'village', 'state',
            'paid', 'notes', 'image', 'screenshot'
        ]

        widgets = {
            'description': forms.Textarea(attrs={'rows': 3}),
            'notes': forms.Textarea(attrs={'rows': 2}),
            'paid': forms.CheckboxInput(),
        }

    def save(self, commit=True, agent=None):
        import json

        # 🔥 SAFE IMPORTS (IMPORTANT FIX)
        from agents import models
        from developer.models import Amenities, SubcategoryField

        images = self.files.getlist('images') if hasattr(self, 'files') else []

        amenities = self.cleaned_data.get('amenities_input', '')
        selling_points = self.cleaned_data.get('selling_points_input', '')
        landmarks_str = self.cleaned_data.get('landmarks_input', '')

        # assign agent
        if agent:
            self.instance.agent = agent
            self.instance.phone = agent.phone_number
            self.instance.whatsapp = agent.whatsapp_number

        property_obj = super().save(commit=commit)

        # ================= AMENITIES =================
        if amenities:
            amenity_list = [a.strip() for a in amenities.split(",") if a.strip()]
            amenity_objs = Amenities.objects.filter(name__in=amenity_list)
            property_obj.amenities.set(amenity_objs)

        # ================= IMAGES =================
        for img in images:
            models.AgentPropertyImage.objects.create(
                property=property_obj,
                image=img
            )

        # ================= SELLING POINTS =================
        if selling_points:
            property_obj.selling_points.all().delete()
            for sp in [s.strip() for s in selling_points.split(",") if s.strip()]:
                property_obj.selling_points.create(point=sp)

        # ================= LANDMARKS =================
        if landmarks_str:
            try:
                landmarks_list = json.loads(landmarks_str)
                property_obj.landmarks.all().delete()

                for lm in landmarks_list:
                    if isinstance(lm, dict):
                        property_obj.landmarks.create(
                            name=lm.get("name"),
                            distance=lm.get("distance")
                        )
            except json.JSONDecodeError:
                pass

        return property_obj



class AgentReviewForm(forms.ModelForm):

    class Meta:
        model = AgentReview
        fields = ["rating", "review"]  # ✅ ONLY valid fields

        widgets = {
            "rating": forms.NumberInput(attrs={
                "class": "form-control",
                "min": 1,
                "max": 5,
                "step": 0.5,
                "placeholder": "Rating (1-5)"
            }),
            "review": forms.Textarea(attrs={
                "class": "form-control",
                "rows": 4,
                "placeholder": "Write your review..."
            }),
        }

    # ✅ Validation
    def clean_rating(self):
        rating = self.cleaned_data.get("rating")

        if rating < 1 or rating > 5:
            raise forms.ValidationError("Rating must be between 1 and 5")

        return rating