from django import forms
# forms.py

from django import forms
from .models import *



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

    # ✅ NEW (form-only fields)
    instagram = forms.CharField(required=False, widget=forms.TextInput(attrs={'class': 'form-control'}))
    facebook = forms.CharField(required=False, widget=forms.TextInput(attrs={'class': 'form-control'}))

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
            'agent_type',
        ]

        widgets = {
            'phone_number': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.TextInput(attrs={'class': 'form-control'}),
            'address': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'pin_code': forms.TextInput(attrs={'class': 'form-control'}),
            'profile_image': forms.ClearableFileInput(attrs={'class': 'form-control'}),
            'professional_title': forms.TextInput(attrs={'class': 'form-control'}),
            'professional_bio': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'agent_type': forms.Select(attrs={'class': 'form-control'}),
        }

    def clean_operating_cities(self):
        cities = self.cleaned_data.get('operating_cities')
        if cities:
            return [city.strip() for city in cities.split(',')]
        return []

    def save(self, commit=True):
        instance = super().save(commit=False)

        # ✅ Save website JSON
        instagram = self.cleaned_data.get('instagram')
        facebook = self.cleaned_data.get('facebook')

        instance.website = {
            "instagram": instagram or "",
            "facebook": facebook or ""
        }

        if commit:
            instance.save()
            self.save_m2m()

        return instance