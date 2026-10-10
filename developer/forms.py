from django import forms
from .models import (
    PendingAgentRegistration,
    AgentPlan,
)
from agents.models import (
    AgentProperty,
    AgentPropertyImage,
    AgentPropertyFieldValue,
    AgentPropertySellingPoint,
    AgentPropertyLandmark
)
from .models import BannerAd, SliderAd
from .models import Blog

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

class PendingAgentRegistrationForm(forms.ModelForm):

    # --------------------------------
    # PASSWORD
    # --------------------------------

    password = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                "class": INPUT_STYLE,
                "placeholder": "Enter password",
                "autocomplete": "new-password",
            }
        )
    )


    # --------------------------------
    # BASIC PLAN
    # --------------------------------

    basic_plan = forms.ModelChoiceField(
        queryset=AgentPlan.objects.all().order_by("name"),
        required=False,
        empty_label="Select Basic Plan",
        widget=forms.Select(
            attrs={
                "class": SELECT_STYLE,
                "id": "id_basic_plan",
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
            "basic_plan",
            "premium_plan",
            "elite_plan",
            "years_of_experience",
            "deals_closed",
            "status",
        ]


        widgets = {

            # --------------------------------
            # FULL NAME
            # --------------------------------

            "full_name": forms.TextInput(
                attrs={
                    "class": INPUT_STYLE,
                    "placeholder": "Enter full name",
                }
            ),


            # --------------------------------
            # EMAIL
            # --------------------------------

            "email": forms.EmailInput(
                attrs={
                    "class": INPUT_STYLE,
                    "placeholder": "Enter email address",
                    "autocomplete": "off",
                }
            ),


            # --------------------------------
            # PHONE
            # --------------------------------

            "phone_number": forms.TextInput(
                attrs={
                    "class": INPUT_STYLE,
                    "placeholder": "Enter phone number",
                }
            ),


            # --------------------------------
            # CITY
            # --------------------------------

            "city": forms.TextInput(
                attrs={
                    "class": INPUT_STYLE,
                    "placeholder": "Enter city",
                }
            ),


            # --------------------------------
            # PIN CODE
            # --------------------------------

            "pin_code": forms.TextInput(
                attrs={
                    "class": INPUT_STYLE,
                    "placeholder": "Enter pin code",
                }
            ),


            # --------------------------------
            # ADDRESS
            # --------------------------------

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
                    "rows": 5,
                }
            ),


            # --------------------------------
            # AGENT TYPE
            # --------------------------------

            "agent_type": forms.Select(
                attrs={
                    "class": SELECT_STYLE,
                    "id": "id_agent_type",
                }
            ),


            # --------------------------------
            # PREMIUM PLAN
            # --------------------------------

            "premium_plan": forms.Select(
                attrs={
                    "class": SELECT_STYLE,
                    "id": "id_premium_plan",
                }
            ),


            # --------------------------------
            # ELITE PLAN
            # --------------------------------

            "elite_plan": forms.Select(
                attrs={
                    "class": SELECT_STYLE,
                    "id": "id_elite_plan",
                }
            ),


            # --------------------------------
            # EXPERIENCE
            # --------------------------------

            "years_of_experience": forms.NumberInput(
                attrs={
                    "class": INPUT_STYLE,
                    "placeholder": "Years of experience",
                }
            ),


            # --------------------------------
            # DEALS CLOSED
            # --------------------------------

            "deals_closed": forms.NumberInput(
                attrs={
                    "class": INPUT_STYLE,
                    "placeholder": "Number of deals",
                }
            ),


            # --------------------------------
            # STATUS
            # --------------------------------

            "status": forms.Select(
                attrs={
                    "class": SELECT_STYLE,
                }
            ),
        }


    # =====================================
    # VALIDATION
    # =====================================

    def clean(self):

        cleaned_data = super().clean()

        agent_type = cleaned_data.get("agent_type")

        basic = cleaned_data.get("basic_plan")
        premium = cleaned_data.get("premium_plan")
        elite = cleaned_data.get("elite_plan")


        # --------------------------------
        # BASIC
        # --------------------------------

        if agent_type == "basic":

            if not basic:

                self.add_error(
                    "basic_plan",
                    "Please select a Basic Plan."
                )

            # Basic should not have other plans

            cleaned_data["premium_plan"] = None
            cleaned_data["elite_plan"] = None


        # --------------------------------
        # PREMIUM
        # --------------------------------

        elif agent_type == "premium":

            if not premium:

                self.add_error(
                    "premium_plan",
                    "Please select a Premium Plan."
                )

            # Premium does not use Basic or Elite

            cleaned_data["basic_plan"] = None
            cleaned_data["elite_plan"] = None


        # --------------------------------
        # ELITE
        # --------------------------------

        elif agent_type == "elite":

            if not elite:

                self.add_error(
                    "elite_plan",
                    "Please select an Elite Plan."
                )

            # Elite does not use Basic or Premium

            cleaned_data["basic_plan"] = None
            cleaned_data["premium_plan"] = None


        return cleaned_data

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

from django import forms
from .models import Blog


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

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # =====================================================
        # COMMON FIELD CLASSES
        # =====================================================

        self.fields["category"].widget.attrs.update({
            "class": "blog-input"
        })

        self.fields["blog_head"].widget.attrs.update({
            "class": "blog-input",
            "placeholder": "Enter blog title"
        })

        self.fields["date"].widget.attrs.update({
            "class": "blog-input",
            "type": "date"
        })

        self.fields["card_paragraph"].widget.attrs.update({
            "class": "blog-input",
            "placeholder": "Enter card paragraph"
        })

        self.fields["image"].widget.attrs.update({
            "class": "blog-input",
            "accept": "image/jpeg,image/png,image/webp"
        })

    # =========================================================
    # BLOG TITLE VALIDATION
    # =========================================================

    def clean_blog_head(self):

        title = self.cleaned_data.get("blog_head", "").strip()

        if not title:
            raise forms.ValidationError(
                "Blog title is required."
            )

        if len(title) < 5:
            raise forms.ValidationError(
                "Blog title must contain at least 5 characters."
            )

        return title

    # =========================================================
    # CARD PARAGRAPH VALIDATION
    # =========================================================

    def clean_card_paragraph(self):

        paragraph = self.cleaned_data.get(
            "card_paragraph",
            ""
        ).strip()

        if not paragraph:
            raise forms.ValidationError(
                "Card paragraph is required."
            )

        if len(paragraph) < 5:
            raise forms.ValidationError(
                "Card paragraph must contain at least 5 characters."
            )

        return paragraph

    # =========================================================
    # CATEGORY VALIDATION
    # =========================================================

    def clean_category(self):

        category = self.cleaned_data.get("category")

        if not category:
            raise forms.ValidationError(
                "Please select a category."
            )

        return category

    # =========================================================
    # DATE VALIDATION
    # =========================================================

    def clean_date(self):

        date = self.cleaned_data.get("date")

        if not date:
            raise forms.ValidationError(
                "Publish date is required."
            )

        return date

    def clean_image(self):

        image = self.cleaned_data.get("image")
        if not image:
            if not self.instance or not self.instance.pk:
                raise forms.ValidationError(
                    "Featured image is required."
                )
            return self.instance.image
        if not hasattr(image, "size"):

            return image

        allowed_types = [
            "image/jpeg",
            "image/png",
            "image/webp",
        ]

        if image.content_type not in allowed_types:

            raise forms.ValidationError(
                "Only JPG, PNG and WEBP images are allowed."
            )

        return image


class BannerAdForm(forms.ModelForm):
    class Meta:
        model = BannerAd
        fields = ["image", "is_active"]


class SliderAdForm(forms.ModelForm):
    class Meta:
        model = SliderAd
        fields = ["image", "is_active"]



#new code added by mehreena
class AgentPropertyForm(forms.ModelForm):

    class Meta:
        model = AgentProperty

        fields = [
            "category",
            "subcategory",
            "purpose",

            "label",
            "land_area",
            "sq_ft",

            "price",
            "perprice",
            "deposit",

            "description",

            "owner",
            "phone",
            "whatsapp",

            "city",
            "district",
            "state",
            "taluk",
            "village",
            "pincode",

            "location",
            "notes",
        ]

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
            ),

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

        