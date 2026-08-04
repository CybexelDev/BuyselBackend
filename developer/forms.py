from django import forms

class SuperuserLoginForm(forms.Form):
    username = forms.CharField(
        max_length=150,
        widget=forms.TextInput(attrs={
            'placeholder': 'Enter username',
            'style': 'text-align: center;'
        })
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'placeholder': 'Enter password',
            'style': 'text-align: center;'
        })
    )


from django import forms
from .models import PendingAgentRegistration


INPUT_STYLE = (
    "w-full h-14 "
    "pl-14 pr-5 "
    "rounded-2xl "
    "border border-gray-200 "
    "bg-gray-50 "
    "text-gray-800 "
    "text-base "
    "outline-none "
    "transition duration-200 "
    "focus:bg-white "
    "focus:ring-2 "
    "focus:ring-[#8bc83f] "
    "focus:border-[#8bc83f]"
)


SELECT_STYLE = (
    "w-full h-14 "
    "px-5 "
    "rounded-2xl "
    "border border-gray-200 "
    "bg-gray-50 "
    "text-gray-800 "
    "text-base "
    "outline-none "
    "transition duration-200 "
    "focus:bg-white "
    "focus:ring-2 "
    "focus:ring-[#8bc83f] "
    "focus:border-[#8bc83f]"
)

# SELECT_STYLE = (
#     "w-full h-14 "
#     "px-5 pr-12 "
#     "rounded-2xl "
#     "border border-gray-300 "
#     "bg-white "
#     "text-gray-800 "
#     "text-base "
#     "font-medium "
#     "shadow-sm "
#     "appearance-none "
#     "cursor-pointer "
#     "outline-none "
#     "transition-all duration-200 "
#     "hover:border-[#8bc83f] "
#     "focus:bg-white "
#     "focus:border-[#8bc83f] "
#     "focus:ring-4 "
#     "focus:ring-[#8bc83f]/20"
# )


class PendingAgentRegistrationForm(forms.ModelForm):

    password = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                "class": INPUT_STYLE,
                "placeholder": "Enter password",
                "autocomplete": "new-password"
            }
        )
    )


    class Meta:

        model = PendingAgentRegistration


        fields = [
            "full_name",
            "email",
            "phone_number",
            "password",
            "city",
            "pin_code",
            "address",
            "agent_type",
            "premium_plan",
            "elite_plan",
            "years_of_experience",
            "deals_closed",
            "status",
        ]


        widgets = {


            "full_name": forms.TextInput(
                attrs={
                    "class": INPUT_STYLE,
                    "placeholder": "Enter full name"
                }
            ),


            "email": forms.EmailInput(
                attrs={
                    "class": INPUT_STYLE,
                    "placeholder": "Enter email address",
                    "autocomplete": "off"
                }
            ),


            "phone_number": forms.TextInput(
                attrs={
                    "class": INPUT_STYLE,
                    "placeholder": "Enter phone number"
                }
            ),


            "city": forms.TextInput(
                attrs={
                    "class": INPUT_STYLE,
                    "placeholder": "Enter city"
                }
            ),


            "pin_code": forms.TextInput(
                attrs={
                    "class": INPUT_STYLE,
                    "placeholder": "Enter pin code"
                }
            ),


            "address": forms.Textarea(
                attrs={
                    "class":
                        "w-full min-h-[140px] "
                        "px-5 py-4 "
                        "rounded-2xl "
                        "border border-gray-200 "
                        "bg-gray-50 "
                        "text-gray-800 "
                        "outline-none "
                        "transition "
                        "focus:bg-white "
                        "focus:ring-2 "
                        "focus:ring-[#8bc83f] "
                        "focus:border-[#8bc83f]",
                    "placeholder": "Enter complete address",
                    "rows": 5
                }
            ),


            "agent_type": forms.Select(
                attrs={
                    "class": SELECT_STYLE,
                    "id": "id_agent_type"
                }
            ),


            "premium_plan": forms.Select(
                attrs={
                    "class": SELECT_STYLE,
                    "id": "id_premium_plan"
                }
            ),


            "elite_plan": forms.Select(
                attrs={
                    "class": SELECT_STYLE,
                    "id": "id_elite_plan"
                }
            ),


            "years_of_experience": forms.NumberInput(
                attrs={
                    "class": INPUT_STYLE,
                    "placeholder": "Years of experience"
                }
            ),


            "deals_closed": forms.NumberInput(
                attrs={
                    "class": INPUT_STYLE,
                    "placeholder": "Number of deals"
                }
            ),


            "status": forms.Select(
                attrs={
                    "class": SELECT_STYLE
                }
            ),

        }



    def clean(self):

        cleaned_data = super().clean()

        agent_type = cleaned_data.get("agent_type")
        premium = cleaned_data.get("premium_plan")
        elite = cleaned_data.get("elite_plan")


        if agent_type == "basic":

            cleaned_data["premium_plan"] = None
            cleaned_data["elite_plan"] = None


        elif agent_type == "premium":

            if not premium:

                self.add_error(
                    "premium_plan",
                    "Please select a Premium Plan."
                )


            cleaned_data["elite_plan"] = None


        elif agent_type == "elite":

            if not elite:

                self.add_error(
                    "elite_plan",
                    "Please select an Elite Plan."
                )


            cleaned_data["premium_plan"] = None


        return cleaned_data



from django import forms
from .models import Blog


INPUT_STYLE = (
    "w-full h-14 px-5 rounded-2xl "
    "border border-gray-200 bg-gray-50 "
    "text-gray-800 outline-none "
    "transition duration-200 "
    "focus:bg-white "
    "focus:ring-2 "
    "focus:ring-[#8bc83f] "
    "focus:border-[#8bc83f]"
)

TEXTAREA_STYLE = (
    "w-full min-h-[140px] px-5 py-4 "
    "rounded-2xl border border-gray-200 "
    "bg-gray-50 text-gray-800 "
    "outline-none transition duration-200 "
    "focus:bg-white "
    "focus:ring-2 "
    "focus:ring-[#8bc83f] "
    "focus:border-[#8bc83f]"
)

SELECT_STYLE = (
    "w-full h-14 px-5 rounded-2xl "
    "border border-gray-200 bg-gray-50 "
    "text-gray-800 outline-none "
    "transition duration-200 "
    "focus:bg-white "
    "focus:ring-2 "
    "focus:ring-[#8bc83f] "
    "focus:border-[#8bc83f]"
)


class BlogForm(forms.ModelForm):

    class Meta:

        model = Blog

        fields = [
            "category",
            "blog_head",
            "date",
            "card_paragraph",
            "image",
        ]


        widgets = {

            "category": forms.Select(
                attrs={
                    "class": SELECT_STYLE
                }
            ),


            "blog_head": forms.TextInput(
                attrs={
                    "class": INPUT_STYLE,
                    "placeholder": "Enter Blog Title"
                }
            ),


            "date": forms.DateInput(
                attrs={
                    "class": INPUT_STYLE,
                    "type": "date"
                }
            ),


            "card_paragraph": forms.Textarea(
                attrs={
                    "class": TEXTAREA_STYLE,
                    "placeholder": "Enter Blog Description",
                    "rows":5
                }
            ),


            "image": forms.ClearableFileInput(
                attrs={
                    "class": INPUT_STYLE,
                    "accept":"image/*"
                }
            ),

        }


from django import forms
from .models import BannerAd, SliderAd


class BannerAdForm(forms.ModelForm):
    class Meta:
        model = BannerAd
        fields = ["image", "is_active"]


class SliderAdForm(forms.ModelForm):
    class Meta:
        model = SliderAd
        fields = ["image", "is_active"]


from django import forms

from agents.models import (
    AgentProperty,
    AgentPropertyImage,
    AgentPropertyFieldValue,
    AgentPropertySellingPoint,
    AgentPropertyLandmark
)


class AgentPropertyForm(forms.ModelForm):

    class Meta:
        model = AgentProperty

        exclude = (
            "id",
            "agent",
            "property_hash_id",
            "subscription",
            "paid",
            "created_at",
            "is_featured",
        )

        widgets = {

            "description": forms.Textarea(
                attrs={
                    "rows": 4
                }
            ),

            "location": forms.Textarea(
                attrs={
                    "rows": 2
                }
            ),

            "notes": forms.Textarea(
                attrs={
                    "rows": 2
                }
            )

        }
        


class AgentPropertyImageForm(forms.ModelForm):

    class Meta:

        model = AgentPropertyImage

        fields = (
            "image",
        )


class AgentPropertySellingPointForm(forms.ModelForm):

    class Meta:

        model = AgentPropertySellingPoint

        fields = (
            "point",
        )


class AgentPropertyLandmarkForm(forms.ModelForm):

    class Meta:

        model = AgentPropertyLandmark

        fields = (
            "name",
            "distance",
        )


class AgentPropertyFieldValueForm(forms.ModelForm):

    class Meta:

        model = AgentPropertyFieldValue

        fields = (
            "field",
            "value",
        )

        