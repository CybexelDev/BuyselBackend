from rest_framework import serializers
from .models import *
from django.contrib.auth.hashers import check_password
from django.core.mail import send_mail
from django.contrib.auth.hashers import make_password
from agents.models import *
import shortuuid
from agents.utils import check_agent_property_limit
from agents.models import (
    AgentProperty,
    AgentPropertyImage,
    AgentPropertyFieldValue,
    SubcategoryField,
    AgentPropertySellingPoint,
    AgentPropertyLandmark,
    Category,
    Subcategory,
    Purpose
)
import re
from django.db.models import Avg, Count
import hashids
from django.core.exceptions import ValidationError as DjangoValidationError

class PropertySerializer(serializers.ModelSerializer):

    # ✅ All images together
    image = serializers.SerializerMethodField()

    # ✅ Show NAME instead of ID
    category = serializers.CharField(source="category.name", read_only=True)
    purpose = serializers.CharField(source="purpose.name", read_only=True)

    class Meta:
        model = Property

        fields = [
            "id",
            "image",
            "category",   # name
            "purpose",    # name
            "city",       # already CharField
            "label",
            "location",
            "district",
            "perprice",
            "price",
            "owner",
            "whatsapp",
            "phone",
        ]

    # -------------------
    # ALL IMAGES
    # -------------------
    def get_image(self, obj):

        images = []

        # main image
        if obj.image:
            images.append(obj.image.url)

        # gallery images
        if hasattr(obj, "images"):
            images.extend(
                [img.image.url for img in obj.images.all() if img.image]
            )

        return images

    from rest_framework import serializers
    from .models import Premium

    class PremiumLoginSerializer(serializers.Serializer):

        username = serializers.CharField()
        password = serializers.CharField(write_only=True)

        def validate(self, data):

            username = data.get("username")
            password = data.get("password")

            try:

                premium = Premium.objects.get(username=username)

            except Premium.DoesNotExist:

                raise serializers.ValidationError("Invalid Username")

            # simple password check
            if premium.password != password:
                raise serializers.ValidationError("Invalid Password")

            # expiry check
            if premium.is_expired():
                raise serializers.ValidationError(
                    "Account Expired"
                )

            data["premium"] = premium

            return data


class PremiumLoginSerializer(serializers.Serializer):

    username = serializers.CharField()
    password = serializers.CharField(write_only=True)

    def validate(self,data):

        username = data.get("username")
        password = data.get("password")

        try:

            premium = Premium.objects.get(username=username)

        except Premium.DoesNotExist:

            raise serializers.ValidationError("Invalid Username")

        # simple password check
        if premium.password != password:

            raise serializers.ValidationError("Invalid Password")

        # expiry check
        if premium.is_expired():

            raise serializers.ValidationError(
                "Account Expired"
            )

        data["premium"] = premium

        return data

class RequestSerializer(serializers.ModelSerializer):

    class Meta:
        model = Request

        fields = [
            "id",
            "name",
            "email",
            "phone",
            "message",
            "created_at"
        ]

        read_only_fields = ["id", "created_at"]

    def validate(self, data):

        name = data.get("name")
        email = data.get("email")
        phone = data.get("phone")
        message = data.get("message")

        if not name or len(name.strip()) < 2:
            raise serializers.ValidationError({
                "name": "Name must be at least 2 characters"
            })

        email_regex = r"^[\w\.-]+@[\w\.-]+\.\w+$"

        if not email or not re.match(email_regex, email):
            raise serializers.ValidationError({
                "email": "Enter a valid email address"
            })

        if not phone or not re.match(r"^[6-9]\d{9}$", phone):
            raise serializers.ValidationError({
                "phone": "Enter a valid 10-digit phone number"
            })

        if message and len(message.strip()) < 5:
            raise serializers.ValidationError({
                "message": "Message must be at least 5 characters"
            })

        return data

class BudgetSerializer(serializers.ModelSerializer):

    class Meta :
        model = Budget

        fields = [
            "id",
            "value",
        ]

        read_only_fields= ["id"]


class CategorySerializer(serializers.ModelSerializer):
    class Meta :
        model = Category

        fields = [
            "id",
            "name"
        ]
        read_only_fields = ["id"]


class PremiumPasswordChangeSerializer(serializers.Serializer):

    username = serializers.CharField()
    old_password = serializers.CharField(write_only=True)
    new_password = serializers.CharField(write_only=True)
    confirm_password = serializers.CharField(write_only=True)

    def validate(self, data):

        username = data.get("username")
        old_password = data.get("old_password")
        new_password = data.get("new_password")
        confirm_password = data.get("confirm_password")

        try:
            premium = Premium.objects.get(
                username=username
            )

        except Premium.DoesNotExist:

            raise serializers.ValidationError(
                "Invalid Username"
            )

        if not check_password(
            old_password,
            premium.password
        ):

            raise serializers.ValidationError(
                "Old Password Incorrect"
            )

        if new_password != confirm_password:

            raise serializers.ValidationError(
                "Password Does Not Match"
            )

        data["premium"] = premium

        return data


class AgentFormSerializer(serializers.ModelSerializer):

    image = serializers.SerializerMethodField()

    class Meta:
        model = AgentForm
        fields = "__all__"

    def get_image(self, obj):

        if obj.image:
            try:
                return obj.image.url  
            except:
                return None

        return None

from rest_framework import serializers
from django.contrib.auth.hashers import make_password
from users.models import UserCreate


class RegisterSerializer(serializers.ModelSerializer):

    confirm_password = serializers.CharField(write_only=True)

    class Meta:
        model = UserCreate
        fields = [
            "name",
            "email",
            "mobile",
            "password",
            "confirm_password"
        ]

        extra_kwargs = {
            "password": {"write_only": True}
        }

    def validate(self, attrs):

        password = attrs.get("password")
        confirm_password = attrs.get("confirm_password")
        email = attrs.get("email")

        # 1. Password match check
        if password != confirm_password:
            raise serializers.ValidationError({
                "confirm_password": "Passwords do not match"
            })

        # 2. Email uniqueness check (case-insensitive)
        if UserCreate.objects.filter(email__iexact=email).exists():
            raise serializers.ValidationError({
                "email": "Email already registered"
            })

        # 3. Password strength (optional but good)
        if len(password) < 6:
            raise serializers.ValidationError({
                "password": "Password must be at least 6 characters long"
            })

        return attrs

    def create(self, validated_data):

        validated_data.pop("confirm_password")

        validated_data["password"] = make_password(
            validated_data["password"]
        )

        return UserCreate.objects.create(**validated_data)


class VerifyOTPSerializer(serializers.Serializer):
    email = serializers.EmailField()
    otp = serializers.CharField(max_length=6)
    def validate_otp(self, value):
        if not value.isdigit():
            raise serializers.ValidationError("OTP must contain only numbers.")
        return value

class ForgotPasswordSerializer(serializers.Serializer):

    email = serializers.EmailField()


class VerifyForgotOTPSerializer(serializers.Serializer):

    email = serializers.EmailField()

    otp = serializers.CharField(max_length=6)
    
    def validate_otp(self, value):
        if not value.isdigit():
            raise serializers.ValidationError("OTP must contain only numbers.")
        return value


class ChangePasswordSerializer(serializers.Serializer):

    new_password = serializers.CharField(
        min_length=6,
        write_only=True
    )

    confirm_password = serializers.CharField(
        min_length=6,
        write_only=True
    )

    def validate(self, data):

        if data["new_password"] != data["confirm_password"]:

            raise serializers.ValidationError({

                "confirm_password":
                "Passwords do not match"

            })

        return data

class UserLoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField()








class AgentNotificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Notification
        fields = "__all__"




from cloudinary.utils import cloudinary_url
from rest_framework import serializers
from cloudinary.utils import cloudinary_url
from .models import UserProfile


class UserProfileSerializer(
    serializers.ModelSerializer
):

    email = serializers.CharField(
        source="user.email",
        read_only=True
    )

    mobile = serializers.CharField(
        source="user.mobile",
        required=False
    )

    name = serializers.CharField(
        source="user.name",
        read_only=True
    )

    city = serializers.CharField(
        required=False,
        allow_blank=True,
        allow_null=True
    )

    is_verified = serializers.BooleanField(
        source="user.is_verified",
        read_only=True
    )

    created_at = serializers.DateTimeField(
        format="%d-%m-%Y",
        read_only=True
    )

    image = serializers.SerializerMethodField()


    class Meta:
        model = UserProfile

        fields = [
            "custom_user_id",
            "email",
            "name",
            "username",
            "full_name",
            "mobile",
            "alternate_mobile",
            "city",
            "image",
            "auth_provider",
            "is_active",
            "is_verified",
            "created_at",
        ]


        read_only_fields = [
            "custom_user_id",
            "email",
            "name",
            "username",
            "auth_provider",
            "is_active",
            "created_at",
            "is_verified",
        ]


    def to_representation(
        self,
        instance
    ):
        data = super().to_representation(
            instance
        )

        data["city"] = (
            instance.city or ""
        )

        return data


    def get_image(
        self,
        obj
    ):
        if obj.image:
            try:
                url,_ = cloudinary_url(
                    obj.image.public_id,
                    secure=True
                )
                return url
            except:
                return None

        return None

    
class AmenitiesSerializer(serializers.ModelSerializer):

    icon = serializers.SerializerMethodField()

    class Meta:
        model = Amenities
        fields = ["id", "name", "icon"]

    def get_icon(self, obj):
        if obj.icon:
            return obj.icon.url
        return None




class InboxSerializer(serializers.ModelSerializer):
    class Meta:
        model = Inbox
        fields = "__all__"
        read_only_fields = ["created_at", "is_read", "is_removed"]

class AgentReviewSerializer(serializers.ModelSerializer):

    user_name = serializers.SerializerMethodField()
    user_image = serializers.SerializerMethodField()
    total_likes = serializers.SerializerMethodField()
    created_at = serializers.SerializerMethodField()
    is_owner = serializers.SerializerMethodField()

    class Meta:
        model = AgentReview
        fields = [
            "id",
            "user_name",
            "user_image",
            "rating",
            "review",
            "total_likes",
            "created_at",
            "is_owner"
        ]

    def get_is_owner(self, obj):
        request = self.context.get("request")

        if not request:
            return False

        user = getattr(request, "user", None)

        # MUST be authenticated user from JWT
        if not user or not user.is_authenticated:
            return False

        # safe comparison
        return obj.user_id == user.id

    def get_user_name(self, obj):
        return obj.user.name if obj.user else "Anonymous"

    def get_user_image(self, obj):

        if obj.user and hasattr(obj.user, "profile"):
            profile = obj.user.profile
            if profile.image:
                return profile.image.url

        name = obj.user.name if obj.user else "Anonymous"

        return (
            "https://ui-avatars.com/api/"
            f"?name={name}"
            "&background=random"
            "&color=fff"
        )

    def get_total_likes(self, obj):
        return obj.likes.count()

    def get_created_at(self, obj):
        return obj.created_at.strftime("%d-%m-%Y")
    
class AgentListFrontendSerializer(serializers.ModelSerializer):
    profile_image = serializers.SerializerMethodField()
    avg_rating = serializers.SerializerMethodField()
    total_reviews = serializers.SerializerMethodField()

    class Meta:
        model = AgentUserProfile
        fields = [
            "id",
            "username",
            "profile_image",
            "city",
            "agent_type",
            "avg_rating",
            "total_reviews",
        ]

    def get_profile_image(self, obj):
        return obj.get_profile_image()

    def get_avg_rating(self, obj):
        # safe fallback for reverse relation
        reviews = getattr(obj, "reviews", None) or obj.review_set
        return reviews.aggregate(avg=Avg("rating"))["avg"] or 0

    def get_total_reviews(self, obj):
        reviews = getattr(obj, "reviews", None) or obj.review_set
        return reviews.count()

class AgentSerializer(serializers.ModelSerializer):
    agent_code = serializers.CharField(read_only=True)
    plan_name = serializers.SerializerMethodField()
    profile_image = serializers.SerializerMethodField()

    class Meta:
        model = AgentUserProfile
        fields = "__all__"
        extra_kwargs = {
            'password': {'write_only': True}
        }

    def get_profile_image(self, obj):
        return obj.get_profile_image()

    def get_plan_name(self, obj):
        if obj.plan:
            return obj.plan.name
        if obj.elite_plan:
            return obj.elite_plan.name
        return None
    
    
class AgentRegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    plan = serializers.CharField(required=False)

    class Meta:
        model = AgentUserProfile
        fields = [
            "username",
            "password",
            "phone_number",
            "address",
            "city",
            "profile_image",
            "pin_code",
            "email",
            "agent_type",
            "plan",
            "professional_bio",
            "specializations",
            "operating_cities",
            "instagram",
            "facebook",
            "website",
            "whatsapp_number"
        ]

    def validate(self, data):
        plan_name = data.get("plan")
        agent_type = data.get("agent_type")

        # Plan required for premium & elite
        if agent_type in ["premium", "elite"] and not plan_name:
            raise serializers.ValidationError({
                "plan": "Plan is required for Premium and Elite agents"
            })

        # Assign Premium Plan
        if plan_name and agent_type == "premium":
            try:
                plan_obj = PremiumPlan.objects.get(name__iexact=plan_name)
                data["plan"] = plan_obj
            except PremiumPlan.DoesNotExist:
                raise serializers.ValidationError({
                    "plan": "Premium plan not found"
                })

        # Assign Elite Plan
        if plan_name and agent_type == "elite":
            try:
                plan_obj = ElitePlan.objects.get(name__iexact=plan_name)
                data["elite_plan"] = plan_obj
                data.pop("plan", None)
            except ElitePlan.DoesNotExist:
                raise serializers.ValidationError({
                    "plan": "Elite plan not found"
                })

        return data

    def create(self, validated_data):
        request = self.context.get('request')

        password = validated_data.pop("password")

        # Remove ManyToMany from validated_data
        validated_data.pop("specializations", None)

        specializations = request.data.getlist("specializations")
        operating_cities = request.data.get("operating_cities")

        # Create agent
        agent = AgentUserProfile(**validated_data)
        agent.set_password(password)
        agent.is_agent = True
        agent.save()

        # Activate plan AFTER save
        if agent.plan:
            agent.activate_premium_plan(agent.plan)

        if hasattr(agent, "elite_plan") and agent.elite_plan:
            agent.activate_elite_plan(agent.elite_plan)

        # Operating Cities
        if operating_cities:
            agent.operating_cities = [
                city.strip() for city in operating_cities.split(',')
            ]
            agent.save()

        # Set ManyToMany Specializations
        if specializations:
            category_objects = []
            for name in specializations:
                category, _ = Category.objects.get_or_create(name=name)
                category_objects.append(category)

            agent.specializations.set(category_objects)

        return agent

class AgentLoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)

    def validate(self, data):
        email = data.get("email")
        password = data.get("password")

        try:
            user = AgentUserProfile.objects.get(email=email)
        except AgentUserProfile.DoesNotExist:
            raise serializers.ValidationError({"error": "Invalid email"})

        if not user.check_password(password):
            raise serializers.ValidationError({"error": "Invalid password"})

        data["user"] = user
        return data

from django.core.exceptions import ValidationError as DjangoValidationError

from rest_framework import serializers

from .models import (
    PendingAgentRegistration,
    PremiumPlan,
    ElitePlan,
    AgentUserProfile,
)


# class PendingAgentRegistrationSerializer(
#     serializers.ModelSerializer
# ):

#     class Meta:

#         model = PendingAgentRegistration

#         fields = [
#             "full_name",
#             "email",
#             "phone_number",
#             "password",
#             "city",
#             "pin_code",
#             "address",
#             "agent_type",
#             "premium_plan",
#             "elite_plan",
#             "years_of_experience",
#             "deals_closed",
#         ]

#         extra_kwargs = {
#             "password": {
#                 "write_only": True,
#                 "min_length": 8,
#             }
#         }

#     # =================================================
#     # FULL NAME
#     # =================================================

#     def validate_full_name(self, value):

#         value = value.strip()

#         if not value:
#             raise serializers.ValidationError(
#                 "Full name is required."
#             )

#         if len(value) < 2:

#             raise serializers.ValidationError(
#                 "Full name must contain at least 2 characters."
#             )

#         if len(value) > 150:

#             raise serializers.ValidationError(
#                 "Full name cannot exceed 150 characters."
#             )

#         import re

#         # if not re.fullmatch(
#         #     r"[A-Za-z][A-Za-z .'-]*",
#         #     value
#         # ):

#         #     raise serializers.ValidationError(
#         #         "Full name contains invalid characters."
#         #     )

#         return value

#     # =================================================
#     # EMAIL
#     # =================================================

#     def validate_email(self, value):

#         value = value.strip().lower()

#         if not value:

#             raise serializers.ValidationError(
#                 "Email is required."
#             )

#         if PendingAgentRegistration.objects.filter(
#             email__iexact=value,
#             status="pending"
#         ).exists():

#             raise serializers.ValidationError(
#                 "You have already submitted a request."
#             )

#         if AgentUserProfile.objects.filter(
#             email__iexact=value
#         ).exists():

#             raise serializers.ValidationError(
#                 "Account already exists. Please login."
#             )

#         return value

#     # =================================================
#     # PHONE
#     # =================================================

#     def validate_phone_number(self, value):

#         value = value.strip()

#         import re

#         if not re.fullmatch(
#             r"^[6-9]\d{9}$",
#             value
#         ):

#             raise serializers.ValidationError(
#                 "Enter a valid 10-digit Indian mobile number."
#             )

#         return value

#     # =================================================
#     # PASSWORD
#     # =================================================

#     def validate_password(self, value):

#         if not value:

#             raise serializers.ValidationError(
#                 "Password is required."
#             )

#         if len(value) < 8:

#             raise serializers.ValidationError(
#                 "Password must contain at least 8 characters."
#             )

#         if len(value) > 128:

#             raise serializers.ValidationError(
#                 "Password cannot exceed 128 characters."
#             )

#         if not any(
#             char.isupper()
#             for char in value
#         ):

#             raise serializers.ValidationError(
#                 "Password must contain at least one uppercase letter."
#             )

#         if not any(
#             char.islower()
#             for char in value
#         ):

#             raise serializers.ValidationError(
#                 "Password must contain at least one lowercase letter."
#             )

#         if not any(
#             char.isdigit()
#             for char in value
#         ):

#             raise serializers.ValidationError(
#                 "Password must contain at least one number."
#             )

#         if not any(
#             char in "!@#$%^&*()-_=+[]{}|;:,.<>?/`~"
#             for char in value
#         ):

#             raise serializers.ValidationError(
#                 "Password must contain at least one special character."
#             )

#         return value

#     # =================================================
#     # CITY
#     # =================================================

#     def validate_city(self, value):

#         value = value.strip()

#         if not value:

#             raise serializers.ValidationError(
#                 "City is required."
#             )

#         return value

#     # =================================================
#     # PIN CODE
#     # =================================================

#     def validate_pin_code(self, value):

#         value = str(value).strip()

#         import re

#         if not re.fullmatch(
#             r"^\d{6}$",
#             value
#         ):

#             raise serializers.ValidationError(
#                 "PIN code must contain exactly 6 digits."
#             )

#         if value.startswith("0"):

#             raise serializers.ValidationError(
#                 "PIN code cannot start with zero."
#             )

#         return value

#     # =================================================
#     # ADDRESS
#     # =================================================

#     def validate_address(self, value):

#         value = value.strip()

#         if not value:

#             raise serializers.ValidationError(
#                 "Address is required."
#             )

#         if len(value) < 5:

#             raise serializers.ValidationError(
#                 "Address must contain at least 5 characters."
#             )

#         return value

#     # =================================================
#     # AGENT TYPE
#     # =================================================

#     def validate_agent_type(self, value):

#         allowed_types = {
#             "basic",
#             "premium",
#             "elite"
#         }

#         if value not in allowed_types:

#             raise serializers.ValidationError(
#                 "Invalid agent type."
#             )

#         return value

#     # =================================================
#     # YEARS OF EXPERIENCE
#     # =================================================

#     def validate_years_of_experience(self, value):

#         if value is None:

#             return value

#         if value < 0:

#             raise serializers.ValidationError(
#                 "Years of experience cannot be negative."
#             )

#         if value > 100:

#             raise serializers.ValidationError(
#                 "Years of experience cannot exceed 100."
#             )

#         return value

#     # =================================================
#     # DEALS CLOSED
#     # =================================================

#     def validate_deals_closed(self, value):

#         if value is None:

#             return 0

#         if value < 0:

#             raise serializers.ValidationError(
#                 "Deals closed cannot be negative."
#             )

#         if value > 1000000:

#             raise serializers.ValidationError(
#                 "Deals closed value is too large."
#             )

#         return value

#     # =================================================
#     # PREMIUM PLAN
#     # =================================================

#     def validate_premium_plan(self, value):

#         if value is None:

#             return value

#         if not PremiumPlan.objects.filter(
#             pk=value.pk
#         ).exists():

#             raise serializers.ValidationError(
#                 "Selected premium plan does not exist."
#             )

#         return value

#     # =================================================
#     # ELITE PLAN
#     # =================================================

#     def validate_elite_plan(self, value):

#         if value is None:

#             return value

#         if not ElitePlan.objects.filter(
#             pk=value.pk
#         ).exists():

#             raise serializers.ValidationError(
#                 "Selected elite plan does not exist."
#             )

#         return value

#     # =================================================
#     # CROSS FIELD VALIDATION
#     # =================================================

#     def validate(self, attrs):

#         agent_type = attrs.get(
#             "agent_type"
#         )

#         premium_plan = attrs.get(
#             "premium_plan"
#         )

#         elite_plan = attrs.get(
#             "elite_plan"
#         )

#         if agent_type == "basic":

#             if premium_plan:

#                 raise serializers.ValidationError({
#                     "premium_plan":
#                     "Basic agent cannot have a premium plan."
#                 })

#             if elite_plan:

#                 raise serializers.ValidationError({
#                     "elite_plan":
#                     "Basic agent cannot have an elite plan."
#                 })

#         elif agent_type == "premium":

#             if not premium_plan:

#                 raise serializers.ValidationError({
#                     "premium_plan":
#                     "Premium plan is required for premium agent."
#                 })

#             if elite_plan:

#                 raise serializers.ValidationError({
#                     "elite_plan":
#                     "Premium agent cannot have an elite plan."
#                 })

#         elif agent_type == "elite":

#             if not elite_plan:

#                 raise serializers.ValidationError({
#                     "elite_plan":
#                     "Elite plan is required for elite agent."
#                 })

#             if premium_plan:

#                 raise serializers.ValidationError({
#                     "premium_plan":
#                     "Elite agent cannot have a premium plan."
#                 })

#         return attrs

#     # =================================================
#     # CREATE
#     # =================================================

#     def create(self, validated_data):

#         # submitted_by is intentionally NOT taken
#         # from request.data.
#         #
#         # It is supplied by:
#         #
#         # serializer.save(
#         #     submitted_by=request.user
#         # )

#         submitted_by = validated_data.pop(
#             "submitted_by",
#             None
#         )

#         registration = PendingAgentRegistration.objects.create(
#             submitted_by=submitted_by,
#             **validated_data
#         )

#         return registration

class PendingAgentRegistrationSerializer(
    serializers.ModelSerializer
):

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

            # ==========================================
            # BASIC PLAN
            # ==========================================
            "basic_plan",

            # ==========================================
            # PREMIUM / ELITE
            # ==========================================
            "premium_plan",
            "elite_plan",

            "years_of_experience",
            "deals_closed",
        ]

        extra_kwargs = {
            "password": {
                "write_only": True,
                "min_length": 8,
            },

            "basic_plan": {
                "required": False,
                "allow_null": True,
            },

            "premium_plan": {
                "required": False,
                "allow_null": True,
            },

            "elite_plan": {
                "required": False,
                "allow_null": True,
            },
        }

    # =================================================
    # FULL NAME
    # =================================================

    def validate_full_name(self, value):

        value = value.strip()

        if not value:

            raise serializers.ValidationError(
                "Full name is required."
            )

        if len(value) < 2:

            raise serializers.ValidationError(
                "Full name must contain at least 2 characters."
            )

        if len(value) > 150:

            raise serializers.ValidationError(
                "Full name cannot exceed 150 characters."
            )

        return value

    # =================================================
    # EMAIL
    # =================================================

    def validate_email(self, value):

        value = value.strip().lower()

        if not value:

            raise serializers.ValidationError(
                "Email is required."
            )

        if PendingAgentRegistration.objects.filter(
            email__iexact=value,
            status="pending"
        ).exists():

            raise serializers.ValidationError(
                "You have already submitted a request."
            )

        if AgentUserProfile.objects.filter(
            email__iexact=value
        ).exists():

            raise serializers.ValidationError(
                "Account already exists. Please login."
            )

        return value

    # =================================================
    # PHONE
    # =================================================

    def validate_phone_number(self, value):

        value = value.strip()

        import re

        if not re.fullmatch(
            r"^[6-9]\d{9}$",
            value
        ):

            raise serializers.ValidationError(
                "Enter a valid 10-digit Indian mobile number."
            )

        return value

    # =================================================
    # PASSWORD
    # =================================================

    def validate_password(self, value):

        if not value:

            raise serializers.ValidationError(
                "Password is required."
            )

        if len(value) < 8:

            raise serializers.ValidationError(
                "Password must contain at least 8 characters."
            )

        if len(value) > 128:

            raise serializers.ValidationError(
                "Password cannot exceed 128 characters."
            )

        if not any(
            char.isupper()
            for char in value
        ):

            raise serializers.ValidationError(
                "Password must contain at least one uppercase letter."
            )

        if not any(
            char.islower()
            for char in value
        ):

            raise serializers.ValidationError(
                "Password must contain at least one lowercase letter."
            )

        if not any(
            char.isdigit()
            for char in value
        ):

            raise serializers.ValidationError(
                "Password must contain at least one number."
            )

        if not any(
            char in "!@#$%^&*()-_=+[]{}|;:,.<>?/`~"
            for char in value
        ):

            raise serializers.ValidationError(
                "Password must contain at least one special character."
            )

        return value

    # =================================================
    # CITY
    # =================================================

    def validate_city(self, value):

        value = value.strip()

        if not value:

            raise serializers.ValidationError(
                "City is required."
            )

        return value

    # =================================================
    # PIN CODE
    # =================================================

    def validate_pin_code(self, value):

        value = str(value).strip()

        import re

        if not re.fullmatch(
            r"^\d{6}$",
            value
        ):

            raise serializers.ValidationError(
                "PIN code must contain exactly 6 digits."
            )

        if value.startswith("0"):

            raise serializers.ValidationError(
                "PIN code cannot start with zero."
            )

        return value

    # =================================================
    # ADDRESS
    # =================================================

    def validate_address(self, value):

        value = value.strip()

        if not value:

            raise serializers.ValidationError(
                "Address is required."
            )

        if len(value) < 5:

            raise serializers.ValidationError(
                "Address must contain at least 5 characters."
            )

        return value

    # =================================================
    # AGENT TYPE
    # =================================================

    def validate_agent_type(self, value):

        value = value.strip().lower()

        allowed_types = {
            "basic",
            "premium",
            "elite"
        }

        if value not in allowed_types:

            raise serializers.ValidationError(
                "Invalid agent type."
            )

        return value

    # =================================================
    # BASIC PLAN
    # =================================================

    def validate_basic_plan(self, value):

        if value is None:
            return value

        if not AgentPlan.objects.filter(
            pk=value.pk
        ).exists():

            raise serializers.ValidationError(
                "Selected basic plan does not exist."
            )

        return value

    # =================================================
    # PREMIUM PLAN
    # =================================================

    def validate_premium_plan(self, value):

        if value is None:
            return value

        if not PremiumPlan.objects.filter(
            pk=value.pk
        ).exists():

            raise serializers.ValidationError(
                "Selected premium plan does not exist."
            )

        return value

    # =================================================
    # ELITE PLAN
    # =================================================

    def validate_elite_plan(self, value):

        if value is None:
            return value

        if not ElitePlan.objects.filter(
            pk=value.pk
        ).exists():

            raise serializers.ValidationError(
                "Selected elite plan does not exist."
            )

        return value

    # =================================================
    # YEARS OF EXPERIENCE
    # =================================================

    def validate_years_of_experience(self, value):

        if value is None:
            return value

        if value < 0:

            raise serializers.ValidationError(
                "Years of experience cannot be negative."
            )

        if value > 100:

            raise serializers.ValidationError(
                "Years of experience cannot exceed 100."
            )

        return value

    # =================================================
    # DEALS CLOSED
    # =================================================

    def validate_deals_closed(self, value):

        if value is None:
            return 0

        if value < 0:

            raise serializers.ValidationError(
                "Deals closed cannot be negative."
            )

        if value > 1000000:

            raise serializers.ValidationError(
                "Deals closed value is too large."
            )

        return value

    # =================================================
    # CROSS FIELD VALIDATION
    # =================================================

    def validate(self, attrs):

        agent_type = attrs.get(
            "agent_type"
        )

        basic_plan = attrs.get(
            "basic_plan"
        )

        premium_plan = attrs.get(
            "premium_plan"
        )

        elite_plan = attrs.get(
            "elite_plan"
        )

        # =================================================
        # BASIC
        # =================================================

        if agent_type == "basic":

            # Basic now MUST have a basic plan

            if not basic_plan:

                raise serializers.ValidationError({
                    "basic_plan":
                    "Basic plan is required for basic agent."
                })

            if premium_plan:

                raise serializers.ValidationError({
                    "premium_plan":
                    "Basic agent cannot have a premium plan."
                })

            if elite_plan:

                raise serializers.ValidationError({
                    "elite_plan":
                    "Basic agent cannot have an elite plan."
                })

        # =================================================
        # PREMIUM
        # =================================================

        elif agent_type == "premium":

            if not premium_plan:

                raise serializers.ValidationError({
                    "premium_plan":
                    "Premium plan is required for premium agent."
                })

            if basic_plan:

                raise serializers.ValidationError({
                    "basic_plan":
                    "Premium agent cannot have a basic plan."
                })

            if elite_plan:

                raise serializers.ValidationError({
                    "elite_plan":
                    "Premium agent cannot have an elite plan."
                })

        # =================================================
        # ELITE
        # =================================================

        elif agent_type == "elite":

            if not elite_plan:

                raise serializers.ValidationError({
                    "elite_plan":
                    "Elite plan is required for elite agent."
                })

            if basic_plan:

                raise serializers.ValidationError({
                    "basic_plan":
                    "Elite agent cannot have a basic plan."
                })

            if premium_plan:

                raise serializers.ValidationError({
                    "premium_plan":
                    "Elite agent cannot have a premium plan."
                })

        return attrs

    # =================================================
    # CREATE
    # =================================================

    def create(self, validated_data):

        # submitted_by is intentionally NOT accepted
        # from frontend.

        submitted_by = validated_data.pop(
            "submitted_by",
            None
        )

        registration = PendingAgentRegistration.objects.create(
            submitted_by=submitted_by,
            **validated_data
        )

        return registration

# class PendingAgentRegistrationSerializer(serializers.ModelSerializer):

#     # -----------------------------------------------------
#     # API INPUT FIELD
#     # -----------------------------------------------------
#     # Frontend sends:
#     #
#     # "plan_id": 5
#     #
#     # We resolve it manually based on agent_type.
#     # -----------------------------------------------------

#     plan_id = serializers.CharField(
#         required=False,
#         allow_null=True,
#         allow_blank=True,
#         write_only=True
#     )

#     class Meta:

#         model = PendingAgentRegistration

#         fields = [
#             "full_name",
#             "email",
#             "phone_number",
#             "password",
#             "city",
#             "pin_code",
#             "address",
#             "agent_type",

#             # Frontend field
#             "plan_id",

#             # Database fields
#             "premium_plan",
#             "elite_plan",

#             "years_of_experience",
#             "deals_closed",
#         ]

#         extra_kwargs = {

#             "password": {
#                 "write_only": True,
#                 "min_length": 8,
#             },

#             "premium_plan": {
#                 "required": False,
#                 "allow_null": True,
#                 "read_only": True,
#             },

#             "elite_plan": {
#                 "required": False,
#                 "allow_null": True,
#                 "read_only": True,
#             },

#             "years_of_experience": {
#                 "required": False,
#                 "allow_null": True,
#             },

#             "deals_closed": {
#                 "required": False,
#             },
#         }

#     # =====================================================
#     # FULL NAME
#     # =====================================================

#     def validate_full_name(self, value):

#         value = str(value).strip()

#         if not value:
#             raise serializers.ValidationError(
#                 "Full name is required."
#             )

#         if len(value) < 2:
#             raise serializers.ValidationError(
#                 "Full name must contain at least 2 characters."
#             )

#         if len(value) > 150:
#             raise serializers.ValidationError(
#                 "Full name cannot exceed 150 characters."
#             )

#         import re

#         # if not re.fullmatch(
#         #     r"[A-Za-z][A-Za-z .'-]*",
#         #     value
#         # ):
#         #     raise serializers.ValidationError(
#         #         "Full name contains invalid characters."
#         #     )

#         return value

#     # =====================================================
#     # EMAIL
#     # =====================================================

#     def validate_email(self, value):

#         value = str(value).strip().lower()

#         if not value:
#             raise serializers.ValidationError(
#                 "Email is required."
#             )

#         # Already pending
#         if PendingAgentRegistration.objects.filter(
#             email__iexact=value,
#             status="pending"
#         ).exists():

#             raise serializers.ValidationError(
#                 "You have already submitted a request."
#             )

#         # Already registered agent
#         if AgentUserProfile.objects.filter(
#             email__iexact=value
#         ).exists():

#             raise serializers.ValidationError(
#                 "Account already exists. Please login."
#             )

#         return value

#     # =====================================================
#     # PHONE
#     # =====================================================

#     def validate_phone_number(self, value):

#         value = str(value).strip()

#         if not value:
#             raise serializers.ValidationError(
#                 "Mobile number is required."
#             )

#         import re

#         if not re.fullmatch(
#             r"^[6-9]\d{9}$",
#             value
#         ):
#             raise serializers.ValidationError(
#                 "Mobile number must contain exactly 10 digits."
#             )

#         return value

#     # =====================================================
#     # PASSWORD
#     # =====================================================

#     def validate_password(self, value):

#         if not value:
#             raise serializers.ValidationError(
#                 "Password is required."
#             )

#         if len(value) < 8:
#             raise serializers.ValidationError(
#                 "Password must contain at least 8 characters."
#             )

#         if len(value) > 128:
#             raise serializers.ValidationError(
#                 "Password cannot exceed 128 characters."
#             )

#         if not any(
#             char.isupper()
#             for char in value
#         ):
#             raise serializers.ValidationError(
#                 "Password must contain at least one uppercase letter."
#             )

#         if not any(
#             char.islower()
#             for char in value
#         ):
#             raise serializers.ValidationError(
#                 "Password must contain at least one lowercase letter."
#             )

#         if not any(
#             char.isdigit()
#             for char in value
#         ):
#             raise serializers.ValidationError(
#                 "Password must contain at least one number."
#             )

#         if not any(
#             char in "!@#$%^&*()-_=+[]{}|;:,.<>?/`~"
#             for char in value
#         ):
#             raise serializers.ValidationError(
#                 "Password must contain at least one special character."
#             )

#         return value

#     # =====================================================
#     # CITY
#     # =====================================================

#     def validate_city(self, value):

#         value = str(value).strip()

#         if not value:
#             raise serializers.ValidationError(
#                 "City is required."
#             )

#         if len(value) < 2:
#             raise serializers.ValidationError(
#                 "City must contain at least 2 characters."
#             )

#         if len(value) > 100:
#             raise serializers.ValidationError(
#                 "City cannot exceed 100 characters."
#             )

#         import re

#         if not re.fullmatch(
#             r"[A-Za-z][A-Za-z .'-]*",
#             value
#         ):
#             raise serializers.ValidationError(
#                 "City contains invalid characters."
#             )

#         return value

#     # =====================================================
#     # PIN CODE
#     # =====================================================

#     def validate_pin_code(self, value):

#         value = str(value).strip()

#         if not value:
#             raise serializers.ValidationError(
#                 "Pincode is required."
#             )

#         import re

#         if not re.fullmatch(
#             r"^\d{6}$",
#             value
#         ):
#             raise serializers.ValidationError(
#                 "Pincode must contain exactly 6 digits."
#             )

#         if value.startswith("0"):
#             raise serializers.ValidationError(
#                 "Pincode cannot start with zero."
#             )

#         return value

#     # =====================================================
#     # ADDRESS
#     # =====================================================

#     def validate_address(self, value):

#         value = str(value).strip()

#         if not value:
#             raise serializers.ValidationError(
#                 "Address is required."
#             )

#         if len(value) < 5:
#             raise serializers.ValidationError(
#                 "Address must contain at least 5 characters."
#             )

#         if len(value) > 1000:
#             raise serializers.ValidationError(
#                 "Address cannot exceed 1000 characters."
#             )

#         return value

#     # =====================================================
#     # AGENT TYPE
#     # =====================================================

#     def validate_agent_type(self, value):

#         value = str(value).strip().lower()

#         allowed_types = {
#             "basic",
#             "premium",
#             "elite",
#         }

#         if value not in allowed_types:

#             raise serializers.ValidationError(
#                 "Invalid agent type."
#             )

#         return value

#     # =====================================================
#     # YEARS EXPERIENCE
#     # =====================================================

#     def validate_years_of_experience(self, value):

#         if value in [None, ""]:
#             return None

#         try:
#             value = int(value)

#         except (ValueError, TypeError):

#             raise serializers.ValidationError(
#                 "Years of experience must be a valid number."
#             )

#         if value < 0:

#             raise serializers.ValidationError(
#                 "Years of experience cannot be negative."
#             )

#         if value > 100:

#             raise serializers.ValidationError(
#                 "Years of experience cannot exceed 100."
#             )

#         return value

#     # =====================================================
#     # DEALS CLOSED
#     # =====================================================

#     def validate_deals_closed(self, value):

#         if value in [None, ""]:
#             return 0

#         try:
#             value = int(value)

#         except (ValueError, TypeError):

#             raise serializers.ValidationError(
#                 "Deals closed must be a valid number."
#             )

#         if value < 0:

#             raise serializers.ValidationError(
#                 "Deals closed cannot be negative."
#             )

#         if value > 1000000:

#             raise serializers.ValidationError(
#                 "Deals closed value is too large."
#             )

#         return value

#     # =====================================================
#     # PLAN + AGENT TYPE VALIDATION
#     # =====================================================

#     def validate(self, attrs):

#         agent_type = attrs.get("agent_type")
#         plan_id = attrs.get("plan_id")

#         premium_plan = None
#         elite_plan = None

#         # =================================================
#         # BASIC
#         # =================================================

#         if agent_type == "basic":

#             # Basic does not need a plan.
#             #
#             # Even if frontend accidentally sends plan_id,
#             # we ignore it.

#             attrs["premium_plan"] = None
#             attrs["elite_plan"] = None

#             return attrs

#         # =================================================
#         # PREMIUM
#         # =================================================

#         if agent_type == "premium":

#             if plan_id in [None, ""]:

#                 raise serializers.ValidationError({
#                     "plan_id": [
#                         "Premium plan is required."
#                     ]
#                 })

#             premium_plan = PremiumPlan.objects.filter(
#                 id=plan_id
#             ).first()

#             if not premium_plan:

#                 raise serializers.ValidationError({
#                     "plan_id": [
#                         "Invalid premium plan."
#                     ]
#                 })

#             attrs["premium_plan"] = premium_plan
#             attrs["elite_plan"] = None

#             return attrs

#         # =================================================
#         # ELITE
#         # =================================================

#         if agent_type == "elite":

#             if plan_id in [None, ""]:

#                 raise serializers.ValidationError({
#                     "plan_id": [
#                         "Elite plan is required."
#                     ]
#                 })

#             elite_plan = ElitePlan.objects.filter(
#                 id=plan_id
#             ).first()

#             if not elite_plan:

#                 raise serializers.ValidationError({
#                     "plan_id": [
#                         "Invalid elite plan."
#                     ]
#                 })

#             attrs["elite_plan"] = elite_plan
#             attrs["premium_plan"] = None

#             return attrs

#         return attrs

#     # =====================================================
#     # CREATE
#     # =====================================================

#     def create(self, validated_data):

#         # plan_id is only an API field.
#         # It is NOT a database field.

#         validated_data.pop(
#             "plan_id",
#             None
#         )

#         try:

#             return PendingAgentRegistration.objects.create(
#                 **validated_data
#             )

#         except DjangoValidationError as exc:

#             if hasattr(exc, "message_dict"):

#                 raise serializers.ValidationError(
#                     exc.message_dict
#                 )

#             raise serializers.ValidationError({
#                 "error": exc.messages
#             })


# class PendingAgentRegistrationSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = PendingAgentRegistration
#         fields = [
#             "full_name",
#             "email",
#             "phone_number",
#             "password",
#             "city",
#             "pin_code",
#             "agent_type",
#             "plan_name",
#             "address"
#         ]

#     def validate_email(self, value):
#         # check duplicate email
#         if PendingAgentRegistration.objects.filter(email=value).exists():
#             raise serializers.ValidationError(
#                 "Email already exists."
#             )
#         return value

#     def create(self, validated_data):
#         # hash password
#         validated_data['password'] = make_password(validated_data['password'])
#         return PendingAgentRegistration.objects.create(**validated_data)


class AgentProfileSerializer(serializers.ModelSerializer):

    agent_id = serializers.CharField(source='agent_code', read_only=True)
    plan_name = serializers.SerializerMethodField()
    specializations = serializers.PrimaryKeyRelatedField(
        many=True,
        queryset=Category.objects.all(),
        required=False
    )

    class Meta:
        model = AgentUserProfile

        fields = [
            'agent_id',
            'email',
            'username',
            'phone_number',
            'whatsapp_number',
            'address',
            'city',
            'pin_code',

            # ✅ IMPORTANT: MAKE THIS WRITABLE NOW
            'profile_image',

            'professional_title',
            'professional_bio',
            'years_of_experience',
            'properties_listed',
            'deals_closed',
            'specializations',
            'operating_cities',
            'instagram',
            'facebook',
            'website',
            'agent_type',
            'plan_name',
            'paid',
            'plan_start_date',
            'plan_expiry_date',
            'created_at'
        ]

        read_only_fields = [
            'agent_id',
            'email',
            'created_at',
            'plan_name'
        ]

    # -----------------------------------
    # OUTPUT IMAGE FIX (IMPORTANT)
    # -----------------------------------
    def get_profile_image(self, obj):
        if obj.profile_image:
            return obj.profile_image.url
        return obj.avatar_url

    # -----------------------------------
    # SPECIALIZATIONS
    # -----------------------------------
    def to_representation(self, instance):
        data = super().to_representation(instance)
        data['specializations'] = [
            cat.name for cat in instance.specializations.all()
        ]

        # 🔥 FIX IMAGE OUTPUT HERE ALSO
        data['profile_image'] = self.get_profile_image(instance)

        return data

    # -----------------------------------
    # PLAN NAME
    # -----------------------------------
    def get_plan_name(self, obj):
        if obj.plan:
            return obj.plan.name
        if obj.elite_plan:
            return obj.elite_plan.name
        return None

    # -----------------------------------
    # UPDATE LOGIC (KEEP IMAGE SAFE)
    # -----------------------------------
    def update(self, instance, validated_data):

        specializations = validated_data.pop('specializations', None)

        # ⚡ handle image explicitly (VERY IMPORTANT)
        if 'profile_image' in validated_data:
            instance.profile_image = validated_data.get('profile_image')

            # optional: clear fallback avatar if real image exists
            instance.avatar_url = None

        for attr, value in validated_data.items():
            if attr != 'profile_image':
                setattr(instance, attr, value)

        instance.save()

        if specializations is not None:
            instance.specializations.set(specializations)

        return instance

class UserplanSerializer(serializers.ModelSerializer):
    class Meta:
        model = Userplan
        fields = '__all__'

class AgentPlanSerializer(serializers.ModelSerializer):
    class Meta:
        model = AgentPlan
        fields = '__all__'


class PremiumPlanSerializer(serializers.ModelSerializer):
    class Meta:
        model = PremiumPlan
        fields = '__all__'


class ElitePlanSerializer(serializers.ModelSerializer):
    class Meta:
        model = ElitePlan
        fields = '__all__'


class CurrentPlanSerializer(serializers.Serializer):
    status = serializers.CharField()
    plan_name = serializers.CharField()
    subtitle = serializers.CharField()
    expires_on = serializers.DateField()

    property_limit = serializers.IntegerField()
    used_properties = serializers.IntegerField()

    features = serializers.ListField(child=serializers.CharField())

    is_active = serializers.BooleanField()

class AgentContactSerializer(serializers.ModelSerializer):
    class Meta:
        model = AgentContact
        fields = [
            'id',
            'first_name',
            'last_name',
            'contact_number',
            'email',
            'message',
            'created_at'
        ]
        read_only_fields = ['id', 'created_at']

class ChangePasswordSerializer(serializers.Serializer):
    current_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True)
    confirm_password = serializers.CharField(required=True)

    def validate(self, data):
        if data['new_password'] != data['confirm_password']:
            raise serializers.ValidationError("New password and confirm password do not match")
        return data


class AgentPropertySerializer(serializers.ModelSerializer):

    # ✅ UUID PRIMARY KEY
    id = serializers.UUIDField(
        read_only=True
    )

    images = serializers.SerializerMethodField()
    image = serializers.SerializerMethodField()
    amenities = serializers.SerializerMethodField()
    selling_points = serializers.SerializerMethodField()
    landmarks = serializers.SerializerMethodField()
    features = serializers.SerializerMethodField()

    # =========================================
    # INPUT FIELDS
    # =========================================

    category = serializers.PrimaryKeyRelatedField(
        queryset=Category.objects.all()
    )

    subcategory = serializers.CharField(
        required=False,
        allow_null=True,
        allow_blank=True
    )

    purpose = serializers.CharField(
        required=False,
        allow_null=True,
        allow_blank=True
    )

    class Meta:
        model = AgentProperty

        exclude = [
            "property_hash_id"
        ]

        read_only_fields = [
            "agent",
            "id"
        ]

    # =====================================================
    # FK HANDLER
    # =====================================================

    def handle_foreign_keys(self, validated_data):

        # =========================================
        # SUBCATEGORY
        # =========================================

        subcategory_name = self.initial_data.get(
            "subcategory"
        )

        if subcategory_name:

            subcategory = Subcategory.objects.filter(
                name__iexact=str(subcategory_name).strip()
            ).first()

            if not subcategory:
                raise serializers.ValidationError({
                    "subcategory": "Invalid subcategory"
                })

            validated_data["subcategory"] = subcategory

        # =========================================
        # PURPOSE
        # =========================================

        purpose_name = self.initial_data.get(
            "purpose"
        )

        if purpose_name:

            purpose = Purpose.objects.filter(
                name__iexact=str(purpose_name).strip()
            ).first()

            if not purpose:
                raise serializers.ValidationError({
                    "purpose": "Invalid purpose"
                })

            validated_data["purpose"] = purpose

        return validated_data

    # =====================================================
    # VALIDATION
    # =====================================================

    def validate(self, attrs):
        # =========================================
        # REQUIRED FIELD VALIDATION
        # =========================================

        required_fields = [

            "category",
            "subcategory",
            "purpose",
            "description",
            "sq_ft",
            "whatsapp",
            "phone",
            "state",
            "district",
            "pincode",
            "phone"

        ]

        for field in required_fields:

            value = attrs.get(
                field,
                getattr(self.instance, field, None)
                if self.instance else None
            )

            if value in [None, "", [], {}]:

                raise serializers.ValidationError({

                    field: f"{field} field cannot be empty."

                })

        # =========================================
        # IMAGE VALIDATION
        # =========================================

        request = self.context.get("request")

        if request:

            images = request.FILES.getlist("images")

            # =====================================
            # CREATE
            # =====================================

            if not self.instance:

                if not images:

                    raise serializers.ValidationError({

                        "images": (
                            "Minimum 3 property images are required."
                        )

                    })

                if len(images) < 3:

                    raise serializers.ValidationError({

                        "images": (
                            "Minimum 3 property images are required."
                        )

                    })

                if len(images) > 10:

                    raise serializers.ValidationError({

                        "images": (
                            "Maximum 10 property images are allowed."
                        )

                    })

            # =====================================
            # UPDATE
            # =====================================

            else:

                old_images = request.data.getlist(
                    "images"
                )

                new_images = request.FILES.getlist(
                    "images"
                )

                total_images_after_update = (
                    len(old_images) +
                    len(new_images)
                )

                if total_images_after_update < 3:

                    raise serializers.ValidationError({

                        "images": (
                            "Minimum 3 property images are required."
                        )

                    })

                if total_images_after_update > 10:

                    raise serializers.ValidationError({

                        "images": (
                            "Maximum 10 property images are allowed."
                        )

                    })

        # =========================================
        # SELLING POINTS VALIDATION
        # =========================================

        selling_points_list = self.context.get(
            "selling_points_list",
            []
        )

        # if not selling_points_list:

        #     raise serializers.ValidationError({

        #         "selling_points": (
        #             "Selling points cannot be empty."
        #         )

        #     })
        cleaned_selling_points = [

            str(sp).strip()

            for sp in selling_points_list

            if str(sp).strip()
        ]

        if not cleaned_selling_points:

            raise serializers.ValidationError({

                "selling_points": (
                    "Selling points cannot be empty."
                )

            })

        # =========================================
        # LANDMARKS VALIDATION
        # =========================================

        # landmarks_list = self.context.get(
        #     "landmarks_list",
        #     []
        # )

        # if not landmarks_list:

        #     raise serializers.ValidationError({

        #         "landmarks": (
        #             "Landmarks cannot be empty."
        #         )

        #     })
        landmarks_list = self.context.get(
            "landmarks_list",
            []
        )

        # Empty list check
        if not landmarks_list:

            raise serializers.ValidationError({

                "landmarks": (
                    "Landmarks cannot be empty."
                )

            })

        # Validate each landmark
        cleaned_landmarks = []

        for lm in landmarks_list:

            # Must be dict
            if not isinstance(lm, dict):

                continue

            name = str(
                lm.get("name", "")
            ).strip()

            distance = str(
                lm.get("distance", "")
            ).strip()

            # Skip empty landmark
            if not name or not distance:

                continue

            cleaned_landmarks.append({

                "name": name,
                "distance": distance
            })

        # Final validation
        if not cleaned_landmarks:

            raise serializers.ValidationError({

                "landmarks": (
                    "Valid landmarks are required."
                )

            })

        # Save cleaned data back
        self.context["landmarks_list"] = cleaned_landmarks

        # =========================================
        # FEATURES VALIDATION
        # =========================================

        field_values = self.context.get(
            "field_values",
            []
        )

        # =========================================
        # FEATURES VALIDATION
        # =========================================

        field_values = self.context.get(
            "field_values",
            []
        )

        if not field_values:

            raise serializers.ValidationError({

                "features": (
                    "Features cannot be empty."
                )

            })

        # =========================================
        # AMENITIES VALIDATION
        # =========================================

        amenities_list = self.context.get(
            "amenities_list",
            []
        )

        if not amenities_list:

            raise serializers.ValidationError({

                "amenities": (
                    "Amenities cannot be empty."
                )

            })

        purpose_obj = None

        # =========================================
        # GET PURPOSE
        # =========================================

        if "purpose" in attrs:

            purpose_value = attrs.get("purpose")

            if isinstance(purpose_value, str):

                purpose_obj = Purpose.objects.filter(
                    name__iexact=purpose_value.strip()
                ).first()

            else:
                purpose_obj = purpose_value

        elif self.instance:
            purpose_obj = self.instance.purpose

        if not purpose_obj:
            return attrs

        # =========================================
        # PURPOSE NAME
        # =========================================

        purpose_name = str(
            purpose_obj.name
        ).lower().strip()

        # =========================================
        # VALUES
        # =========================================

        price = attrs.get(
            "price",
            getattr(self.instance, "price", None)
        )

        perprice = attrs.get(
            "perprice",
            getattr(self.instance, "perprice", None)
        )

        deposit = attrs.get(
            "deposit",
            getattr(self.instance, "deposit", None)
        )

        # =========================================
        # SALE
        # =========================================

        # if purpose_name == "sale":

        #     if not price:
        #         raise serializers.ValidationError({
        #             "price": "Price is required for sale"
        #         })

        #     if not perprice:
        #         raise serializers.ValidationError({
        #             "perprice": "Per price is required for sale"
        #         })

        #     attrs["deposit"] = None

        if purpose_name == "sale":

            if not price:

                raise serializers.ValidationError({
                    "price": "Price is required for sale"
                })

            if not perprice:

                raise serializers.ValidationError({
                    "perprice": "Per price is required for sale"
                })

            # =====================================
            # PER PRICE FORMAT VALIDATION
            # =====================================

            perprice = str(perprice).strip()

            # pattern = r'^\d+(\.\d+)?\s*/\s*([a-zA-Z]+)$'
            pattern = r'^.+?\s*/\s*([a-zA-Z]+)$'

            matched = re.match(
                pattern,
                perprice
            )

            if not matched:

                raise serializers.ValidationError({

                    "perprice": (
                        "Per price must be like '5000 / Acre'"
                    )

                })

            allowed_units = [

                "Acre",
                "Cent"
            ]

            unit = matched.group(1)

            if unit not in allowed_units:

                raise serializers.ValidationError({

                    "perprice": (
                        "Only Acre and Cent are allowed."
                    )

                })

            attrs["deposit"] = None

        # =========================================
        # RENT
        # =========================================

        elif purpose_name == "rent":

            if not price:
                raise serializers.ValidationError({
                    "price": "Rent amount is required"
                })

            if not deposit:
                raise serializers.ValidationError({
                    "deposit": "Deposit is required for rent"
                })

            attrs["perprice"] = None

        # =========================================
        # LEASE
        # =========================================

        elif purpose_name == "lease":

            if not price:
                raise serializers.ValidationError({
                    "price": "Price is required for lease"
                })

            attrs["deposit"] = None
            attrs["perprice"] = None

        return attrs

    # =====================================================
    # CREATE
    # =====================================================

    def create(self, validated_data):

        request = self.context["request"]

        agent = request.user

        validated_data = self.handle_foreign_keys(
            validated_data
        )

        # AUTO PHONE ONLY IF EMPTY
        if not validated_data.get("phone"):
            validated_data["phone"] = agent.phone_number

        if not validated_data.get("whatsapp"):
            validated_data["whatsapp"] = agent.whatsapp_number

        instance = AgentProperty.objects.create(
            agent=agent,
            **validated_data
        )

        self.handle_related_fields(instance)

        return instance

    # =====================================================
    # UPDATE
    # =====================================================

    def update(self, instance, validated_data):

        request = self.context.get("request")

        validated_data = self.handle_foreign_keys(
            validated_data
        )

        for attr, value in validated_data.items():

            setattr(instance, attr, value)

        if request and request.FILES.get("image"):

            instance.image = request.FILES.get(
                "image"
            )

        instance.save()
        if request:

            old_images = request.data.getlist(
                "images"
            )
            new_images = request.FILES.getlist(
                "images"
            )

            for img_obj in instance.images.all():

                try:

                    image_url = request.build_absolute_uri(
                        img_obj.image.url
                    )

                except Exception:
                    continue

                # keep existing image
                if image_url in old_images:
                    continue

                # skip uploaded file object
                if any(
                    hasattr(i, "name")
                    for i in old_images
                ):
                    continue

                # delete removed image
                img_obj.delete()

            if new_images:

                AgentPropertyImage.objects.bulk_create([

                    AgentPropertyImage(
                        property=instance,
                        image=img
                    )

                    for img in new_images
                ])

        self.handle_related_fields(
            instance
        )

        return instance

    # def update(self, instance, validated_data):

    #     validated_data = self.handle_foreign_keys(
    #         validated_data
    #     )

    #     instance = super().update(
    #         instance,
    #         validated_data
    #     )

    #     self.handle_related_fields(instance)

    #     return instance

    # =====================================================
    # RELATED FIELDS
    # =====================================================

    def handle_related_fields(self, instance):

        amenities_list = self.context.get(
            "amenities_list",
            []
        )

        selling_points_list = self.context.get(
            "selling_points_list",
            []
        )

        landmarks_list = self.context.get(
            "landmarks_list",
            []
        )

        field_values = self.context.get(
            "field_values",
            []
        )

        # =========================================
        # AMENITIES
        # =========================================

        if amenities_list:

            instance.amenities.set(
                amenities_list
            )

        # =========================================
        # SELLING POINTS
        # =========================================

        if selling_points_list:

            instance.selling_points.all().delete()

            AgentPropertySellingPoint.objects.bulk_create([

                AgentPropertySellingPoint(
                    property=instance,
                    point=sp
                )

                for sp in selling_points_list
            ])

        # =========================================
        # LANDMARKS
        # =========================================

        if landmarks_list:

            instance.landmarks.all().delete()

            AgentPropertyLandmark.objects.bulk_create([

                AgentPropertyLandmark(
                    property=instance,
                    name=lm.get("name"),
                    distance=lm.get("distance")
                )

                for lm in landmarks_list
                if isinstance(lm, dict)
            ])

        # =========================================
        # FEATURES
        # =========================================
        # old_subcategory = instance.subcategory

        # instance = super().update(instance, validated_data)

        # new_subcategory = instance.subcategory

        # if old_subcategory != new_subcategory:

        AgentPropertyFieldValue.objects.filter(
            property=instance
        ).delete()

        if field_values:

            for fv in field_values:

                if not isinstance(fv, dict):
                    raise serializers.ValidationError(
                        "Invalid field_values format"
                    )

                field_name = fv.get("name")
                option_name = fv.get("option")
                value = fv.get("value")

                if not field_name:
                    raise serializers.ValidationError(
                        "Feature name missing"
                    )

                field = SubcategoryField.objects.filter(
                    subcategory=instance.subcategory,
                    field_name__iexact=field_name.strip()
                ).first()

                if not field:
                    raise serializers.ValidationError(
                        f"Invalid feature: {field_name}"
                    )

                # =========================================
                # OPTION FIELD
                # =========================================

                if option_name:

                    option = FieldOption.objects.filter(
                        name__iexact=option_name.strip(),
                        field=field
                    ).first()

                    if not option:
                        raise serializers.ValidationError(
                            f"Invalid option: {option_name}"
                        )

                    try:
                        value = int(value)

                    except:
                        raise serializers.ValidationError(
                            f"{option_name} must be a number"
                        )

                    AgentPropertyFieldValue.objects.filter(
                        property=instance,
                        field=field,
                        value__icontains=f'"option": "{option.name}"'
                    ).delete()

                    AgentPropertyFieldValue.objects.create(
                        property=instance,
                        field=field,
                        value=json.dumps({
                            "option": option.name,
                            "count": value
                        })
                    )

                # =========================================
                # NORMAL FIELD
                # =========================================

                else:

                    AgentPropertyFieldValue.objects.filter(
                        property=instance,
                        field=field
                    ).delete()

                    AgentPropertyFieldValue.objects.create(
                        property=instance,
                        field=field,
                        value=str(value)
                    )

    # =====================================================
    # CLEAN OUTPUT
    # =====================================================

    def to_representation(self, instance):

        data = super().to_representation(
            instance
        )

        # ✅ FORCE UUID STRING OUTPUT
        data["id"] = str(instance.id)

        # =========================================
        # PURPOSE NAME
        # =========================================

        data["purpose"] = (
            instance.purpose.name
            if instance.purpose else None
        )

        # =========================================
        # SUBCATEGORY NAME
        # =========================================

        data["subcategory"] = (
            instance.subcategory.name
            if instance.subcategory else None
        )

        purpose = (
            instance.purpose.name.lower().strip()
            if instance.purpose else ""
        )

        # =========================================
        # RENT
        # =========================================

        if purpose == "rent":

            data.pop("perprice", None)

        # =========================================
        # SALE
        # =========================================

        elif purpose == "sale":

            data.pop("deposit", None)

        # =========================================
        # LEASE
        # =========================================

        elif purpose == "lease":

            data.pop("deposit", None)
            data.pop("perprice", None)

        return data
    
    def get_amenities(self, obj):

        return [
            {
                "id": a.id,
                "name": a.name
            }
            for a in obj.amenities.all()
        ]
    
    def get_selling_points(self, obj):

        return [

            sp.point

            for sp in obj.selling_points.all()
        ]
    
    def get_landmarks(self, obj):

        return [

            {
                "name": lm.name,
                "distance": lm.distance
            }

            for lm in obj.landmarks.all()
        ]

    # def get_selling_points(self, obj):

    #     if isinstance(
    #         obj.selling_points,
    #         list
    #     ):
    #         return obj.selling_points

    #     return []

    # def get_landmarks(self, obj):

    #     if isinstance(
    #         obj.land_mark,
    #         list
    #     ):
    #         return obj.land_mark

    #     return []

    # =====================================================
    # FEATURES
    # =====================================================

    # def get_features(self, obj):

    #     result = {}

    #     for fv in obj.field_values.select_related(
    #         "field"
    #     ):

    #         field = fv.field

    #         icon = (
    #             field.icon.url
    #             if field.icon else None
    #         )

    #         try:

    #             data = json.loads(fv.value)

    #             option = data.get("option")

    #             count = data.get("count", 0)

    #             if option:

    #                 result[option] = {
    #                     "value": count,
    #                     "icon": icon
    #                 }

    #                 continue

    #         except Exception:
    #             pass

    #         if field.field_name.lower() == "flat furnishings":
    #             continue

    #         if field.field_type == "countable":

    #             try:
    #                 value = int(fv.value)

    #             except:
    #                 value = 0

    #         else:
    #             value = fv.value

    #         result[field.field_name] = {
    #             "value": value,
    #             "icon": icon
    #         }

    #     return [
    #         {
    #             "name": k,
    #             "value": v["value"],
    #             "icon": v["icon"]
    #         }
    #         for k, v in result.items()
    #     ]
    def get_features(self, obj):

        result = {}

        request = self.context.get("request")

        for fv in obj.field_values.select_related("field"):

            field = fv.field

            try:

                data = json.loads(fv.value)

                option = data.get("option")
                count = data.get("count", 0)

                if option:

                    option_obj = FieldOption.objects.filter(
                        field=field,
                        name__iexact=option
                    ).first()

                    option_icon = None

                    if option_obj and option_obj.icon:

                        try:

                            option_icon = (
                                request.build_absolute_uri(
                                    option_obj.icon.url
                                )
                                if request
                                else option_obj.icon.url
                            )

                        except Exception:

                            option_icon = option_obj.icon.url

                    result[option] = {
                        "value": count,
                        "icon": option_icon
                    }

                    continue

            except Exception:
                pass

            if field.field_name.lower() == "flat furnishings":
                continue

            if field.icon:

                try:

                    icon = (
                        request.build_absolute_uri(
                            field.icon.url
                        )
                        if request
                        else field.icon.url
                    )

                except Exception:

                    icon = field.icon.url

            else:

                icon = None

            if field.field_type == "countable":

                try:
                    value = int(fv.value)

                except Exception:
                    value = 0

            else:
                value = fv.value

            result[field.field_name] = {
                "value": value,
                "icon": icon
            }

        return [
            {
                "name": key,
                "value": value["value"],
                "icon": value["icon"]
            }
            for key, value in result.items()
        ]

    # =====================================================
    # OTHER FIELDS
    # =====================================================

    def get_images(self, obj):

        request = self.context.get("request")

        images = obj.images.all()

        if not images:
            return []

        if request:

            return [

                request.build_absolute_uri(
                    i.image.url
                )

                for i in images
                if i.image
            ]

        return [

            i.image.url

            for i in images
            if i.image
        ]
    
    def get_image(self, obj):

        if not obj.image:
            return None

        request = self.context.get(
            "request"
        )

        return (

            request.build_absolute_uri(
                obj.image.url
            )

            if request
            else obj.image.url
        )


class AgentPropertyEnquirySerializer(serializers.ModelSerializer):

    class Meta:
        model = AgentPropertyEnquiry
        fields = [
            "id",
            "name",
            "email",
            "phone",
            "message",
            "created_at",
        ]
        read_only_fields = ["id", "created_at"]



class AdvertisementPackageSerializer(serializers.ModelSerializer):
    class Meta:
        model = AdvertisementPackage
        fields = "__all__"


class ReelPackageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ReelPackage
        fields = "__all__"


class TestimonialSerializer(serializers.ModelSerializer):
    class Meta:
        model = Testimonial
        fields = "__all__"
        read_only_fields = ["user"]



class PropertyCardSerializer(serializers.ModelSerializer):

    id = serializers.UUIDField(source="pk", read_only=True)
    # owner = serializers.CharField(source="owner.name")
    owner = serializers.CharField()
    images = serializers.SerializerMethodField()
    is_wishlisted = serializers.SerializerMethodField()

    class Meta:
        model = Property
        fields = [
            "id",
            "label",
            "city",
            "perprice",
            "price",
            "sq_ft",
            "land_area",
            "owner",
            "whatsapp",
            "phone",
            "location",
            "images",
            "is_wishlisted"
        ]

    def get_images(self, obj):
        return [
            img.image.url
            for img in obj.images.all()[:2]
            if img.image
        ]

    def get_is_wishlisted(self, obj):
        wishlist_ids = self.context.get("wishlist_ids", set())

        # ✅ SAFE UUID COMPARISON
        return str(obj.pk) in wishlist_ids



class WishlistSerializer(serializers.ModelSerializer):

    id = serializers.SerializerMethodField()
    label = serializers.SerializerMethodField()
    city = serializers.SerializerMethodField()
    perprice = serializers.SerializerMethodField()
    price = serializers.SerializerMethodField()
    sq_ft = serializers.SerializerMethodField()
    land_area = serializers.SerializerMethodField()
    owner = serializers.SerializerMethodField()
    whatsapp = serializers.SerializerMethodField()
    phone = serializers.SerializerMethodField()
    location = serializers.SerializerMethodField()
    images = serializers.SerializerMethodField()
    is_wishlisted = serializers.SerializerMethodField()

    class Meta:
        model = Wishlist
        fields = [
            "id",
            "label",
            "city",
            "perprice",
            "price",
            "sq_ft",
            "land_area",
            "owner",
            "whatsapp",
            "phone",
            "location",
            "images",
            "is_wishlisted"
        ]

    # -----------------------------
    # FETCH OBJECT (AUTO DETECT TYPE)
    # -----------------------------
    # def get_obj(self, obj):
    #     return (
    #         Property.objects.filter(uuid=obj.property_uuid).first()
    #         or AgentProperty.objects.filter(uuid=obj.property_uuid).first()
    #     )
        
    def get_obj(self, obj):

        return (

            Property.objects.filter(
                id=obj.property_uuid
            ).first()

            or

            AgentProperty.objects.filter(
                id=obj.property_uuid
            ).first()
        )

    # -----------------------------
    def get_id(self, obj):
        return str(obj.property_uuid)

    def get_label(self, obj):
        prop = self.get_obj(obj)
        return prop.label if prop else None

    def get_city(self, obj):
        prop = self.get_obj(obj)
        return prop.city if prop else None

    def get_perprice(self, obj):
        prop = self.get_obj(obj)
        return getattr(prop, "perprice", None)

    def get_price(self, obj):
        prop = self.get_obj(obj)
        return prop.price if prop else None

    def get_sq_ft(self, obj):
        prop = self.get_obj(obj)
        return getattr(prop, "sq_ft", None)

    def get_land_area(self, obj):
        prop = self.get_obj(obj)
        return prop.land_area if prop else None

    def get_owner(self, obj):
        prop = self.get_obj(obj)
        if not prop:
            return None

        return getattr(getattr(prop, "owner", None) or getattr(prop, "agent", None), "name", None)

    def get_whatsapp(self, obj):
        prop = self.get_obj(obj)
        return getattr(prop, "whatsapp", None)

    def get_phone(self, obj):
        prop = self.get_obj(obj)
        return getattr(prop, "phone", None)

    def get_location(self, obj):
        prop = self.get_obj(obj)
        return prop.location if prop else None

    def get_images(self, obj):
        prop = self.get_obj(obj)

        if not prop:
            return []

        # User property images
        if hasattr(prop, "images"):
            return [img.image.url for img in prop.images.all()[:2] if img.image]

        # Agent property image
        return [prop.image.url] if getattr(prop, "image", None) else []

    def get_is_wishlisted(self, obj):
        return True



from rest_framework import serializers
import json

from .models import (
    Property,
    PropertyFeature,
)


class PropertyDetailSerializer(serializers.ModelSerializer):

    # =====================================================
    # BASIC
    # =====================================================

    id = serializers.UUIDField(
        read_only=True
    )

    # =====================================================
    # CUSTOM FIELDS
    # =====================================================

    images = serializers.SerializerMethodField()

    image = serializers.SerializerMethodField()

    purpose = serializers.SerializerMethodField()

    category = serializers.SerializerMethodField()

    amenities = serializers.SerializerMethodField()

    property_features = serializers.SerializerMethodField()

    price_details = serializers.SerializerMethodField()

    contact_details = serializers.SerializerMethodField()

    owner_profile_image = serializers.SerializerMethodField()

    selling_points = serializers.SerializerMethodField()

    land_mark = serializers.SerializerMethodField()

    location_details = serializers.SerializerMethodField()

    created_at = serializers.DateTimeField(
        format="%Y-%m-%d",
        read_only=True
    )

    # =====================================================
    # META
    # =====================================================

    class Meta:

        model = Property

        fields = [

            "id",

            "property_code",

            "label",

            "image",

            "images",

            "purpose",

            "category",

            "description",

            "city",

            "state",

            "location",

            "land_mark",

            "created_at",

            "property_features",

            "price_details",

            "contact_details",

            "owner_profile_image",

            "amenities",

            "selling_points",

            "location_details",
        ]

    # =====================================================
    # MAIN IMAGE
    # =====================================================

    def get_image(self, obj):

        request = self.context.get("request")

        if not obj.image:
            return None

        try:

            url = obj.image.url

            if request:
                return request.build_absolute_uri(url)

            return url

        except Exception:
            return None

    # =====================================================
    # MULTIPLE IMAGES
    # =====================================================

    def get_images(self, obj):

        request = self.context.get("request")

        urls = []

        # =========================================
        # MAIN IMAGE FIRST
        # =========================================

        if obj.image:

            try:

                main_url = obj.image.url

                if request:
                    main_url = request.build_absolute_uri(
                        main_url
                    )

                urls.append(main_url)

            except Exception:
                pass

        # =========================================
        # PROPERTY IMAGES
        # =========================================

        for img in obj.images.all():

            if img.image:

                try:

                    url = img.image.url

                    if request:
                        url = request.build_absolute_uri(
                            url
                        )

                    if url not in urls:
                        urls.append(url)

                except Exception:
                    pass

        return urls

    # =====================================================
    # PURPOSE
    # =====================================================

    def get_purpose(self, obj):

        return (
            obj.purpose.name
            if obj.purpose else None
        )

    # =====================================================
    # CATEGORY
    # =====================================================

    def get_category(self, obj):

        request = self.context.get("request")

        if not obj.category:
            return None

        image_url = None

        try:

            if obj.category.image:

                image_url = obj.category.image.url

                if request:
                    image_url = request.build_absolute_uri(
                        image_url
                    )

        except Exception:
            image_url = None

        return {

            "id": obj.category.id,

            "name": obj.category.name,

            "image": image_url,
        }

    # =====================================================
    # FEATURES
    # =====================================================

    def get_property_features(self, obj):

        result = {}

        features = obj.property_features.select_related(
            "field"
        )

        for fv in features:

            field = fv.field

            icon = None

            try:

                if field.icon:

                    icon = field.icon.url

                    request = self.context.get(
                        "request"
                    )

                    if request:
                        icon = request.build_absolute_uri(
                            icon
                        )

            except Exception:
                icon = None

            # =========================================
            # JSON OPTION VALUE
            # =========================================

            try:

                data = json.loads(fv.value)

                option = data.get("option")

                count = data.get("count", 0)

                if option:

                    result[option] = {

                        "value": count,

                        "icon": icon
                    }

                    continue

            except Exception:
                pass

            # =========================================
            # NORMAL VALUE
            # =========================================

            if field.field_type == "countable":

                try:
                    value = int(fv.value)

                except Exception:
                    value = 0

            else:
                value = fv.value

            result[field.field_name] = {

                "value": value,

                "icon": icon
            }

        return [

            {
                "name": k,
                "value": v["value"],
                "icon": v["icon"]
            }

            for k, v in result.items()
        ]

    # =====================================================
    # SELLING POINTS
    # =====================================================

    def get_selling_points(self, obj):

        return obj.selling_points or []

    # =====================================================
    # LANDMARKS
    # =====================================================

    def get_land_mark(self, obj):

        return obj.land_mark or []

    # =====================================================
    # PRICE DETAILS
    # =====================================================

    def get_price_details(self, obj):

        data = {

            "price": obj.price,

            "sq_ft": obj.sq_ft,

            "land_area": obj.land_area,

            "perprice": obj.perprice,

            "deposit": obj.deposit,
        }

        purpose = (
            obj.purpose.name.lower().strip()
            if obj.purpose else ""
        )

        # =========================================
        # RENT
        # =========================================

        if purpose == "rent":

            data.pop("perprice", None)

        # =========================================
        # SALE
        # =========================================

        elif purpose == "sale":

            data.pop("deposit", None)

        # =========================================
        # LEASE
        # =========================================

        elif purpose == "lease":

            data.pop("deposit", None)

            data.pop("perprice", None)

        return data

    # =====================================================
    # CONTACT DETAILS
    # =====================================================

    def get_contact_details(self, obj):

        return {

            "owner": (
                obj.owner.name
                if obj.owner else None
            ),

            "whatsapp": obj.whatsapp,

            "phone": obj.phone,

            "owner_profile_image": (
                self.get_owner_profile_image(obj)
            )
        }

    # =====================================================
    # OWNER PROFILE IMAGE
    # =====================================================

    def get_owner_profile_image(self, obj):

        if not obj.owner:
            return None

        owner = obj.owner

        # =========================================
        # PROFILE IMAGE
        # =========================================

        try:

            if (
                hasattr(owner, "profile")
                and owner.profile
            ):

                profile = owner.profile

                if profile.image:

                    image_val = str(
                        profile.image
                    )

                    if (
                        image_val and
                        "Vector_te4oj7"
                        not in image_val
                    ):

                        try:
                            return profile.image.url

                        except Exception:
                            pass

        except Exception:
            pass

        # =========================================
        # FALLBACK AVATAR
        # =========================================

        name = (
            getattr(owner, "name", "")
            or "User"
        ).strip()

        words = name.split()

        if len(words) >= 2:

            initials = (
                words[0][0] +
                words[1][0]
            ).upper()

        else:

            initials = name[:2].upper()

        return (
            "https://ui-avatars.com/api/"
            f"?name={initials}"
            "&background=8bc83f"
            "&color=ffffff"
            "&size=256"
            "&bold=true"
        )

    # =====================================================
    # AMENITIES
    # =====================================================

    def get_amenities(self, obj):

        request = self.context.get("request")

        data = []

        for amenity in obj.amenities.all():

            icon_url = None

            try:

                if amenity.icon:

                    icon_url = amenity.icon.url

                    if request:

                        icon_url = (
                            request.build_absolute_uri(
                                icon_url
                            )
                        )

            except Exception:
                icon_url = None

            data.append({

                "id": amenity.id,

                "name": amenity.name,

                "icon": icon_url
            })

        return data

    # =====================================================
    # LOCATION DETAILS
    # =====================================================

    def get_location_details(self, obj):

        return {

            "village": obj.village,

            "taluk": obj.taluk,

            "district": obj.district,

            "city": obj.city,

            "state": obj.state,

            "pincode": obj.pincode,
        }



# from rest_framework import serializers
# from .models import PropertyEnquiry


# class PropertyEnquirySerializer(serializers.ModelSerializer):

#     class Meta:
#         model = PropertyEnquiry
#         fields = [
#             "id",
#             "name",
#             "phone",
#             "email",
#             "message",
#             "created_at",
#         ]

#         read_only_fields = [
#             "id",
#             "created_at",
#         ]

class PropertyEnquirySerializer(serializers.ModelSerializer):

    class Meta:
        model = PropertyEnquiry
        fields = [
            "id",
            "name",
            "phone",
            "email",
            "message",
            "created_at",
        ]
        read_only_fields = ["id", "created_at"]

# from rest_framework import serializers
# from .models import Property
# from users.models import UserCreate   # ✅ important
# # from utils.hashids import hashids


# class RelatedPropertySerializer(serializers.ModelSerializer):
#     id = serializers.SerializerMethodField()
#     images = serializers.SerializerMethodField()
#     is_wishlisted = serializers.SerializerMethodField()

#     class Meta:
#         model = Property
#         fields = [
#             "id",
#             "label",
#             "city",
#             "perprice",
#             "price",
#             "sq_ft",
#             "land_area",
#             "owner",
#             "whatsapp",
#             "phone",
#             "location",
#             "images",
#             "is_wishlisted",
#         ]

#     # hashed id
#     def get_id(self, obj):
#         return hashids.encode(obj.id)

#     # image list
#     def get_images(self, obj):
#         return [
#             image.image.url
#             for image in obj.images.all()[:2]
#             if image.image
#         ]

#     # WORKS FOR BOTH LOGIN + NO LOGIN
#     def get_is_wishlisted(self, obj):

#         request = self.context.get("request", None)

#         # No request → not wishlisted
#         if not request:
#             return False

#         # User not logged in
#         if not request.user.is_authenticated:
#             return False

#         # Convert AuthUser → UserCreate safely
#         try:
#             user_create = UserCreate.objects.get(user=request.user)
#         except UserCreate.DoesNotExist:
#             return False

#         # Correct FK comparison
#         return obj.wishlist_set.filter(
#             user=user_create
#         ).exists()
    

class RelatedPropertySerializer(serializers.ModelSerializer):
    id=serializers.SerializerMethodField()
    images = serializers.SerializerMethodField()
    is_wishlisted = serializers.SerializerMethodField()

    class Meta:
        model=Property
        fields=[
            "id",
            "label",
            "city",
            "perprice",
            "price",
            "sq_ft",
            "land_area",
            "owner",
            "whatsapp",
            "phone",
            "location",
            "images",
            "is_wishlisted",
        ]

    # hashed id
    def get_id(self,obj):
        return hashids.encode(obj.id)

    #image_list
    def get_images(self, obj):
        return [
            image.image.url
            for image in obj.images.all()[:2]
            if image.image
        ]

    #wishlist
    def get_is_wishlisted(self, obj):
        request = self.context.get("request")

        # check request exists
        if not request:
            return False

        # check user logged in
        if not request.user.is_authenticated:
            return False

        return obj.wishlist_set.filter(
            user=request.user
        ).exists()



class ContactSerializer(serializers.ModelSerializer):
    class Meta:
        model = Contact
        fields = [
            "id",
            "name",
            "email",
            "phone",
            "message",
            "created_at"
        ]

        read_only_fields = ["id","created_at"]

    # mobile number validation
    def validate_phone(self,value):
        if not value.isdigit():
            raise serializers.ValidationError("Phone number must contains only number")
        if len(value) < 10:
            raise serializers.ValidationError("Phone number is too short")
        return value
    

class BlogListSerializer(serializers.ModelSerializer):
    image = serializers.SerializerMethodField()

    class Meta:
        model = Blog
        fields=[
            "id",
            "blog_head",
            "card_paragraph",
            "image",
            "date",
        ]

    def get_image(self,obj):
        request = self.context.get("request")

        if obj.image:
            image_url = obj.image.url
            if request:
                return request.build_absolute_uri(image_url)
            return image_url
        return None
    

from rest_framework import serializers
from .models import Blog


class SingleBlogSerializer(serializers.ModelSerializer):
    card_paragraph = serializers.SerializerMethodField()
    image = serializers.SerializerMethodField()

    class Meta:
        model = Blog
        fields = [
            "id",
            "blog_head",
            "date",
            "card_paragraph",
            "image",
        ]

    def get_card_paragraph(self, obj):
        if not obj.card_paragraph:
            return ""

        # Clean text and make it one normal paragraph
        cleaned_text = " ".join(
            line.strip()
            for line in obj.card_paragraph.splitlines()
            if line.strip()
        )

        return cleaned_text
    
    def get_image(self, obj):
        request = self.context.get("request")

        if not obj.image:
            return None

        url = obj.image.url  # Cloudinary URL

        # make absolute url
        if request:
            return request.build_absolute_uri(url)

        return url
    
# class BlogModalSerializer(serializers.ModelSerializer):
#     image = serializers.SerializerMethodField()

#     class Meta:
#         model = Blog
#         fields = [
#             "modal_head",
#             "date",
#             "modal_paragraph",
#             "image"
#         ]

#     def get_image(self,obj):
#         request = self.context.get("request")

#         if obj.image:
#             image_url = obj.image.url
#             if request:
#                 return request.build_absolute_uri(image_url)
#             return image_url
#         return None
    

# from rest_framework import serializers
# from .models import Blog


# class BlogSerializer(serializers.ModelSerializer):
#     # category = serializers.CharField(source="category.name")
#     image = serializers.SerializerMethodField()

#     class Meta:
#         model = Blog
#         fields = [
#             "blog_head",
#             # "modal_head",
#             "date",
#             "card_paragraph",
#             # "modal_paragraph",
#             "image",
#             # "category",
#         ]

#     def get_image(self, obj):
#         request = self.context.get("request")

#         if not obj.image:
#             return None

#         url = obj.image.url
#         if request:
#             url = request.build_absolute_uri(url)

#         return url



# from rest_framework import serializers
# from .models import UserProfile, UserCreate


# class UserProfileUpdateSerializer(serializers.Serializer):

#     full_name = serializers.CharField(required=False,allow_blank=True)
#     email = serializers.EmailField(required=False)
#     mobile = serializers.CharField(required=False)
#     alternate_mobile = serializers.CharField(required=False)
#     city = serializers.CharField(required=False)

#     def update(self, user, validated_data):

#         profile = user.profile

#         # ❌ BLOCK EMAIL CHANGE
#         if "email" in validated_data:
#             new_email = validated_data["email"]

#             if new_email != user.email:
#                 raise serializers.ValidationError({
#                     "email": "Email cannot be changed once registered."
#                 })

#         # ✅ UPDATE FIELDS ONLY IF PASSED
#         if "full_name" in validated_data:
#             profile.full_name = validated_data["full_name"].strip()

#         if "mobile" in validated_data and validated_data["mobile"].strip():
#             profile.mobile = validated_data["mobile"]
#             user.mobile = validated_data["mobile"]
#             user.save(update_fields=["mobile"])

#         if "alternate_mobile" in validated_data:
#             profile.alternate_mobile = validated_data["alternate_mobile"]

#         if "city" in validated_data:
#             profile.city = validated_data["city"]

#         profile.save()

#         return profile

class UserProfileUpdateSerializer(serializers.Serializer):

    full_name = serializers.CharField(required=False, allow_blank=True)
    email = serializers.EmailField(required=False)
    mobile = serializers.CharField(required=False, allow_blank=True)
    alternate_mobile = serializers.CharField(required=False, allow_blank=True)
    city = serializers.CharField(required=False, allow_blank=True)

    def update(self, user, validated_data):

        profile = user.profile

        # -------------------------
        # EMAIL BLOCK
        # -------------------------
        if "email" in validated_data:
            if validated_data["email"] != user.email:
                raise serializers.ValidationError({
                    "email": "Email cannot be changed once registered."
                })

        # -------------------------
        # FULL NAME (ALLOW EMPTY)
        # -------------------------
        if "full_name" in validated_data:
            value = validated_data.get("full_name")

            if value is None:
                pass
            else:
                value = str(value)

                if value.strip() == "":
                    profile.full_name = ""
                else:
                    profile.full_name = value.strip()

        # -------------------------
        # MOBILE (SAFE HANDLING)
        # -------------------------
        if "mobile" in validated_data:
            value = validated_data.get("mobile")

            if value is not None:
                value = value.strip()

            profile.mobile = value or ""
            user.mobile = value or ""
            user.save(update_fields=["mobile"])

        # -------------------------
        # ALTERNATE MOBILE
        # -------------------------
        if "alternate_mobile" in validated_data:
            value = validated_data.get("alternate_mobile")
            profile.alternate_mobile = value if value is not None else ""

        # -------------------------
        # CITY
        # -------------------------
        if "city" in validated_data:
            value = validated_data.get("city")
            profile.city = value if value is not None else ""

        profile.save()
        return profile


class MyActivitySerializer(serializers.Serializer):

    wishlist_count = serializers.IntegerField()
    enquiries_count = serializers.IntegerField()
    properties_listed_count = serializers.IntegerField()
    viewed_properties_count = serializers.IntegerField()



class SliderAdSerializer(serializers.ModelSerializer):
    image = serializers.SerializerMethodField()

    class Meta:
        model = SliderAd
        fields = ['id', 'image']

    def get_image(self, obj):
        if obj.image:
            return obj.image.url   
        return None
    


class BannerAdSerializer(serializers.ModelSerializer):
    image = serializers.SerializerMethodField()

    class Meta:
        model = BannerAd
        fields = ['id', 'image']

    def get_image(self, obj):
        if obj.image:
            return obj.image.url   
        return None


from rest_framework import serializers
import json

class AgentDetailSerializer(serializers.ModelSerializer):
    # agent_id = serializers.CharField(source='agent_code', read_only=True)
    plan_name = serializers.SerializerMethodField()
    profile_image = serializers.SerializerMethodField()
    reviews = AgentReviewSerializer(many=True, read_only=True)
    specializations = serializers.SlugRelatedField(
        many=True,
        read_only=True,
        slug_field="name"
    )

    # ✅ NEW FIELDS
    operating_cities = serializers.SerializerMethodField()
    served_area = serializers.SerializerMethodField()

    class Meta:
        model = AgentUserProfile
        fields = [
            "id",
            "agent_code",
            "plan_name",
            "profile_image",
            "username",
            "email",
            "phone_number",
            "whatsapp_number",
            "address",
            "city",
            "pin_code",
            "professional_title",
            "professional_bio",
            "years_of_experience",
            "properties_listed",
            "deals_closed",
            "is_agent",
            "is_active",
            "agent_type",
            "paid",
            "plan_start_date",
            "plan_expiry_date",
            "operating_cities",
            "served_area",

            "instagram",
            "facebook",
            "website",
            "created_at",
            "plan",
            "elite_plan",
            "specializations",
            "reviews"
        ]

    # -------------------------------
    # PROFILE IMAGE
    # -------------------------------
    def get_profile_image(self, obj):
        return obj.get_profile_image()

    # -------------------------------
    # PLAN NAME
    # -------------------------------
    def get_plan_name(self, obj):
        if obj.plan:
            return obj.plan.name
        if obj.elite_plan:
            return obj.elite_plan.name
        return None

    # -------------------------------
    # OPERATING CITIES → LIST
    # -------------------------------
    def get_operating_cities(self, obj):
        data = obj.operating_cities

        # If already list (JSONField)
        if isinstance(data, list):
            return data

        # If stored as string → convert
        if isinstance(data, str):
            try:
                return json.loads(data)
            except:
                return [data]  # fallback

        return []

    # -------------------------------
    # SERVED AREA → COUNT
    # -------------------------------
    def get_served_area(self, obj):
        cities = self.get_operating_cities(obj)
        return len(cities)
    

class PremiumElitePropertySerializer(serializers.ModelSerializer):

    images = serializers.SerializerMethodField()
    image = serializers.SerializerMethodField()
    screenshot = serializers.SerializerMethodField()
    amenities = serializers.SerializerMethodField()
    selling_points = serializers.SerializerMethodField()
    landmarks = serializers.SerializerMethodField()
    features = serializers.SerializerMethodField()

    class Meta:
        model = AgentProperty
        fields = "__all__"
        read_only_fields = ["agent", "phone", "whatsapp"]

    # ✅ LIMIT 2 IMAGES
    def get_images(self, obj):
        return [
            img.image.url
            for img in obj.images.all()[:2]
            if img.image
        ]

    # ✅ MAIN IMAGE
    def get_image(self, obj):
        return obj.image.url if obj.image else None

    # ✅ SCREENSHOT FULL URL
    def get_screenshot(self, obj):
        return obj.screenshot.url if obj.screenshot else None

    def get_amenities(self, obj):
        return [{"id": a.id, "name": a.name} for a in obj.amenities.all()]

    def get_selling_points(self, obj):
        return list(obj.selling_points.values_list("point", flat=True))

    def get_landmarks(self, obj):
        return [
            {"name": l.name, "distance": l.distance}
            for l in obj.landmarks.all()
        ]

    def get_features(self, obj):
        return [
            {
                "name": fv.field.field_name,
                "value": fv.value
            }
            for fv in obj.field_values.select_related("field").all()
        ]

    def to_representation(self, instance):
        data = super().to_representation(instance)

        data["category"] = {
            "id": instance.category.id,
            "name": instance.category.name
        }

        data["subcategory"] = (
            {"id": instance.subcategory.id, "name": instance.subcategory.name}
            if instance.subcategory else None
        )

        data["purpose"] = {
            "id": instance.purpose.id,
            "name": instance.purpose.name
        }

        return data


class EnquiryDetailSerializer(serializers.ModelSerializer):
    created_at = serializers.SerializerMethodField()
    property_label = serializers.CharField(source="property.label", read_only=True)
    price = serializers.CharField(source="property.price", read_only=True)
    description = serializers.CharField(source="property.description", read_only=True)

    location_detail = serializers.SerializerMethodField()

    image = serializers.SerializerMethodField()

    class Meta:
        model = PropertyEnquiry
        fields = [
            "id",
            "name",
            "email",
            "phone",
            "created_at",
            "message",
            "property_label",
            "price",
            "description",
            "location_detail",
            "image",
        ]

    
    def get_created_at(self, obj):
        if not obj.created_at:
            return None
        return obj.created_at.strftime("%B %d, %Y %I:%M %p")

   
    def get_location_detail(self, obj):
        if not obj.property:
            return None

        village = obj.property.village or ""
        city = obj.property.city or ""
        state = obj.property.state or ""

        parts = [village, city, state]
        parts = [p.strip() for p in parts if p]

        return ", ".join(parts) if parts else None

    
    def get_image(self, obj):
        if not obj.property:
            return []

        image = []

        # main image
        if obj.property.image:
            image.append(obj.property.image.url)

        # gallery images
        # if hasattr(obj.property, "images"):
        #     images.extend(
        #         [img.image.url for img in obj.property.images.all() if img.image]
        #     )

        return image
    
from rest_framework import serializers
from django.utils import timezone
import pytz

class RecentEnquirySerializer(serializers.ModelSerializer):

    property_name = serializers.CharField(
        source="property.label",
        read_only=True
    )

    owner_name = serializers.SerializerMethodField()

    date = serializers.SerializerMethodField()

    created_at = serializers.DateTimeField(read_only=True)

    class Meta:

        model = PropertyEnquiry

        fields = [
            "id",
            "property_name",
            "owner_name",
            "date",
            "created_at"
        ]
    def get_owner_name(self, obj):

        if obj.property and obj.property.user:

            return getattr(
                obj.property.user,
                "name",
                None
            )

        return None
    def get_date(self, obj):

        if not obj.created_at:
            return None

        india_timezone = pytz.timezone("Asia/Kolkata")

        indian_time = timezone.localtime(
            obj.created_at,
            india_timezone
        )

        return indian_time.strftime(
            "%B %d, %Y %I:%M %p"
        )

class RecentAgentEnquirySerializer(serializers.ModelSerializer):

    property_name = serializers.CharField(
        source="property.label",
        read_only=True
    )

    agent_name = serializers.SerializerMethodField()

    date = serializers.SerializerMethodField()

    created_at = serializers.DateTimeField(read_only=True)

    class Meta:

        model = AgentPropertyEnquiry

        fields = [
            "id",
            "property_name",
            "agent_name",
            "date",
            "created_at"
        ]

    def get_agent_name(self, obj):

        if obj.property and obj.property.agent:

            return getattr(
                obj.property.agent,
                "username",
                None
            )

        return None

    def get_date(self, obj):

        if not obj.created_at:
            return None

        india_timezone = pytz.timezone("Asia/Kolkata")

        indian_time = timezone.localtime(
            obj.created_at,
            india_timezone
        )

        return indian_time.strftime(
            "%B %d, %Y %I:%M %p"
        )

    
from rest_framework import serializers

class CombinedPropertyListSerializer(serializers.Serializer):

    id=serializers.SerializerMethodField()
    property_type=serializers.SerializerMethodField()

    label=serializers.SerializerMethodField()
    city=serializers.SerializerMethodField()
    perprice=serializers.SerializerMethodField()
    price=serializers.SerializerMethodField()
    sq_ft=serializers.SerializerMethodField()
    land_area=serializers.SerializerMethodField()

    owner=serializers.SerializerMethodField()

    whatsapp=serializers.SerializerMethodField()
    phone=serializers.SerializerMethodField()

    location=serializers.SerializerMethodField()

    images=serializers.SerializerMethodField()

    is_wishlisted=serializers.SerializerMethodField()


    def get_id(self,obj):
        return str(obj.id)


    def get_property_type(self,obj):
        if isinstance(obj,Property):
            return "user"
        return "agent"


    def get_label(self,obj):
        return obj.label


    def get_city(self,obj):
        return obj.city


    def get_perprice(self,obj):
        return obj.perprice


    def get_price(self,obj):
        return obj.price


    def get_sq_ft(self,obj):
        return str(obj.sq_ft) if obj.sq_ft else None


    def get_land_area(self,obj):
        return obj.land_area


    # def get_owner(self,obj):

    #     if isinstance(obj,Property):
    #         return (
    #             obj.owner.name
    #             if obj.owner else None
    #         )

    #     return (
    #         obj.owner
    #         or obj.agent.name
    #     )

    def get_owner(self, obj):

        # # USER PROPERTY
        # if isinstance(obj, Property):
        #     return obj.user if obj.user else None

        if isinstance(obj, Property):

            # manual owner name
            if obj.owner:
                return obj.owner

            # fallback to user
            if obj.user:

                # most correct case
                if hasattr(obj.user, "name"):
                    return obj.user.name

                # fallback cases
                if hasattr(obj.user, "full_name"):
                    return obj.user.full_name

                if hasattr(obj.user, "username"):
                    return obj.user.username

                if hasattr(obj.user, "email"):
                    return obj.user.email

            return None

        # AGENT PROPERTY
        if isinstance(obj, AgentProperty):

            # if manual owner string exists
            if obj.owner:
                return obj.owner

            # fallback to agent
            if obj.agent:

                # most correct case
                if hasattr(obj.agent, "user") and obj.agent.user:
                    return obj.agent.user.name

                # fallback cases (safe)
                if hasattr(obj.agent, "full_name"):
                    return obj.agent.full_name

                if hasattr(obj.agent, "username"):
                    return obj.agent.username

            return None


    def get_whatsapp(self,obj):
        return obj.whatsapp


    def get_phone(self,obj):
        return obj.phone


    def get_location(self,obj):
        return obj.location


    # IMPORTANT FIX
    def get_images(self,obj):

        request=self.context.get(
            "request"
        )

        urls=[]


        # USER PROPERTY MULTIPLE IMAGES
        if isinstance(obj,Property):

            if hasattr(obj,"images"):
                for img in obj.images.all()[:2]:
                    if img.image:
                        url=img.image.url

                        if request:
                            url=request.build_absolute_uri(url)

                        urls.append(url)


        # AGENT PROPERTY SINGLE IMAGE
        elif isinstance(obj,AgentProperty):

            if obj.image:
                url=obj.image.url

                if request:
                    url=request.build_absolute_uri(url)

                urls.append(url)


        return urls
    def get_is_wishlisted(self, obj):

        wishlist_ids = self.context.get(
            "wishlist_ids",
            set()
        )

        # compare UUIDs now
        return str(obj.id) in wishlist_ids
    

# class UserPropertySerializer(serializers.ModelSerializer):

#     id=serializers.UUIDField(
#         read_only=True
#     )

#     images=serializers.SerializerMethodField()
#     image=serializers.SerializerMethodField()
#     amenities=serializers.SerializerMethodField()
#     selling_points=serializers.SerializerMethodField()
#     landmarks=serializers.SerializerMethodField()
#     features=serializers.SerializerMethodField()

#     # =====================================================
#     # OWNER TEXT FIELD ONLY
#     # =====================================================

#     owner=serializers.CharField(
#         required=False,
#         allow_null=True,
#         allow_blank=True
#     )

#     category=serializers.PrimaryKeyRelatedField(
#         queryset=Category.objects.all()
#     )

#     subcategory=serializers.CharField(
#         required=False,
#         allow_null=True,
#         allow_blank=True
#     )

#     purpose=serializers.CharField(
#         required=False,
#         allow_null=True,
#         allow_blank=True
#     )

#     class Meta:

#         model=Property

#         fields="__all__"

#         read_only_fields=[
#             "user"
#         ]

#     # =====================================================
#     # CREATE
#     # =====================================================

#     def get_subcategory_obj(self, sub):
#         if not sub:
#             return None

#         return Subcategory.objects.filter(
#             name__iexact=str(sub).strip()
#         ).first()


#     def get_purpose_obj(self, pur):
#         if not pur:
#             return None

#         return Purpose.objects.filter(
#             name__iexact=str(pur).strip()
#         ).first()

#     def create(self,validated_data):

#         request=self.context.get("request")

#         # =================================================
#         # STORE LOGGED USER INTO USER FIELD
#         # =================================================

#         if request and request.user:

#             validated_data["user"]=request.user

#         # =================================================
#         # OWNER TEXT FIELD
#         # =================================================

#         owner_name=self.initial_data.get("owner")

#         if owner_name is not None:

#             validated_data["owner"]=owner_name.strip()

#         # =================================================
#         # SUBCATEGORY
#         # =================================================
#         sub = self.initial_data.get("subcategory")
#         sub_obj = self.get_subcategory_obj(sub)

#         if sub_obj:
#             validated_data["subcategory"] = sub_obj


#         pur = self.initial_data.get("purpose")
#         pur_obj = self.get_purpose_obj(pur)

#         if pur_obj:
#             validated_data["purpose"] = pur_obj

#         # sub=self.initial_data.get("subcategory")

#         # if sub:

#         #     sub_obj=Subcategory.objects.filter(
#         #         name__iexact=sub.strip()
#         #     ).first()

#         #     if sub_obj:
#         #         validated_data["subcategory"]=sub_obj

#         # # =================================================
#         # # PURPOSE
#         # # =================================================

#         # pur=self.initial_data.get("purpose")

#         # if pur:

#         #     pur_obj=Purpose.objects.filter(
#         #         name__iexact=pur.strip()
#         #     ).first()

#         #     if pur_obj:
#         #         validated_data["purpose"]=pur_obj

#         instance=Property.objects.create(
#             **validated_data
#         )

#         self.handle_related(instance)

#         return instance

#     def update(self,instance,validated_data):
#         request = self.context.get("request")

#         if request:

#             # old image urls
#             old_images = request.data.getlist("images")

#             # new uploaded files
#             new_images = request.FILES.getlist("images")

#             for img_obj in instance.images.all():

#                 image_url = request.build_absolute_uri(
#                     img_obj.image.url
#                 )

#                 if image_url not in old_images:
#                     img_obj.delete()


#             if new_images:

#                 PropertyImage.objects.bulk_create([
#                     PropertyImage(
#                         property=instance,
#                         image=img
#                     )
#                     for img in new_images
#                 ])

#         if request and request.FILES.get("image"):

#             instance.image = request.FILES.get("image")
    

#         # =================================================
#         # OWNER TEXT UPDATE ONLY
#         # =================================================

#         owner_name=self.initial_data.get("owner")

#         if owner_name is not None:

#             instance.owner=owner_name.strip()

#         # =================================================
#         # SUBCATEGORY UPDATE
#         # =================================================
#         sub = self.initial_data.get("subcategory")
#         sub_obj = self.get_subcategory_obj(sub)

#         if sub_obj:
#             instance.subcategory = sub_obj

#         # REMOVE FROM validated_data (CRITICAL FIX)
#         validated_data.pop("subcategory", None)

#         # ==============================
#         # PURPOSE (FIXED)
#         # ==============================
#         pur = self.initial_data.get("purpose")
#         pur_obj = self.get_purpose_obj(pur)

#         if pur_obj:
#             instance.purpose = pur_obj

#         # REMOVE FROM validated_data (CRITICAL FIX)
#         validated_data.pop("purpose", None)


#         for k,v in validated_data.items():

#             if k in ["owner","user"]:
#                 continue

#             setattr(instance,k,v)

#         instance.save()

#         self.handle_related(instance)

#         return instance


#     def handle_related(self, instance):

#         # =================================================
#         # AMENITIES
#         # =================================================

#         # amenities = self.context.get(
#         #     "amenities_list",
#         #     None
#         # )

#         # # ONLY UPDATE IF USER SENT AMENITIES
#         # if amenities is not None:

#         #     amenity_objects = Amenities.objects.filter(
#         #         id__in=amenities
#         #     )

#         #     instance.amenities.set(
#         #         amenity_objects
#         #     )

#         request = self.context.get("request")

#         # ONLY RUN IF FIELD EXISTS IN REQUEST
#         if (
#             request
#             and hasattr(request, "data")
#             and "amenities" in request.data
#         ):

#             amenities = self.context.get(
#                 "amenities_list",
#                 []
#             )

#             # REMOVE EMPTY VALUES
#             amenities = [
#                 a for a in amenities
#                 if a not in ["", None]
#             ]

#             # KEEP OLD AMENITIES IF EMPTY VALUE SENT
#             if amenities:

#                 amenity_objects = Amenities.objects.filter(
#                     id__in=amenities
#                 )

#                 instance.amenities.set(
#                     amenity_objects
#                 )

#         # =================================================
#         # SELLING POINTS
#         # =================================================

#         sp = self.context.get(
#             "selling_points_list",
#             None
#         )

#         if sp is not None:

#             instance.selling_points = sp

#             instance.save(
#                 update_fields=[
#                     "selling_points"
#                 ]
#             )

#         # =================================================
#         # LANDMARKS
#         # =================================================

#         lm = self.context.get(
#             "land_mark_list",
#             None
#         )

#         if lm is not None:

#             instance.land_mark = lm

#             instance.save(
#                 update_fields=[
#                     "land_mark"
#                 ]
#             )

#         # =================================================
#         # FEATURES
#         # =================================================

#         fv_list = self.context.get(
#             "field_values",
#             None
#         )

#         # fallback support
#         if fv_list is None:

#             fv_list = self.context.get(
#                 "features_list",
#                 None
#             )

#         # ONLY UPDATE IF FEATURES SENT
#         if fv_list is not None:

#             # remove old
#             PropertyFeature.objects.filter(
#                 property=instance
#             ).delete()

#             for fv in fv_list:

#                 if not isinstance(fv, dict):
#                     continue

#                 field_name = str(
#                     fv.get("name", "")
#                 ).strip()

#                 if not field_name:
#                     continue

#                 field = SubcategoryField.objects.filter(
#                     subcategory=instance.subcategory,
#                     field_name__iexact=field_name
#                 ).first()

#                 if not field:
#                     continue

#                 PropertyFeature.objects.create(

#                     property=instance,

#                     field=field,

#                     value=json.dumps({

#                         "option": fv.get(
#                             "option"
#                         ),

#                         "value": fv.get(
#                             "value"
#                         ),

#                         "icon": fv.get(
#                             "icon"
#                         )
#                     })
#                 )

#     # =====================================================
#     # OUTPUT
#     # =====================================================

#     def to_representation(self,instance):

#         data=super().to_representation(
#             instance
#         )

#         data["owner"]=(
#             instance.owner
#             if instance.owner
#             else None
#         )

#         return data

#     def get_amenities(self,obj):

#         return [
#             {
#                 "id":a.id,
#                 "name":a.name
#             }
#             for a in obj.amenities.all()
#         ]

#     def get_selling_points(self,obj):

#         if isinstance(
#             obj.selling_points,
#             list
#         ):
#             return obj.selling_points

#         return []

#     def get_landmarks(self,obj):

#         if isinstance(
#             obj.land_mark,
#             list
#         ):
#             return obj.land_mark

#         return []

#     def get_features(self, obj):

#         data = []

#         for f in obj.property_features.select_related("field"):

#             try:
#                 value = json.loads(f.value)

#             except:
#                 value = {
#                     "value": f.value
#                 }

#             # =========================================
#             # USE OPTION NAME IF EXISTS
#             # =========================================

#             feature_name = (
#                 value.get("option")
#                 if value.get("option")
#                 else f.field.field_name
#             )

#             # =========================================
#             # CLEAN VALUE
#             # =========================================

#             feature_value = value.get("value")

#             if feature_value is None:
#                 feature_value = ""

#             data.append({

#                 "name": feature_name,

#                 "value": str(feature_value),

#                 "icon": (
#                     f.field.icon.url
#                     if f.field.icon
#                     else None
#                 )
#             })

#         return data

#     def get_images(self, obj):

#         request = self.context.get("request")

#         images = obj.images.all()

#         if not images:
#             return []

#         if request:

#             return [
#                 request.build_absolute_uri(i.image.url)
#                 for i in images
#                 if i.image
#             ]

#         return [
#             i.image.url
#             for i in images
#             if i.image
#         ]

#     # def get_images(self,obj):

#     #     request=self.context.get(
#     #         "request"
#     #     )

#     #     return [

#     #         request.build_absolute_uri(
#     #             i.image.url
#     #         )

#     #         if request else i.image.url

#     #         for i in obj.images.all()

#     #         if i.image
#     #     ]

#     def get_image(self,obj):

#         if not obj.image:
#             return None

#         request=self.context.get(
#             "request"
#         )

#         return (
#             request.build_absolute_uri(
#                 obj.image.url
#             )
#             if request
#             else obj.image.url
#         )


import json

from rest_framework import serializers

from developer.models import (
    Property,
    PropertyImage,
    PropertyFeature,
    Category,
    Subcategory,
    Purpose,
    Amenities,
    SubcategoryField
)


class UserPropertySerializer(serializers.ModelSerializer):

    id = serializers.UUIDField(
        read_only=True
    )

    images = serializers.SerializerMethodField()
    # image = serializers.SerializerMethodField()
    amenities = serializers.SerializerMethodField()
    selling_points = serializers.SerializerMethodField()
    landmarks = serializers.SerializerMethodField()
    # landmarks = serializers.ListField(source="land_mark",required=False)
    features = serializers.SerializerMethodField()

    # =====================================================
    # REQUIRED FIELDS
    # =====================================================

    owner = serializers.CharField(
        required=True,
        allow_null=False,
        allow_blank=False
    )

    category = serializers.PrimaryKeyRelatedField(
        queryset=Category.objects.all(),
        required=True
    )

    subcategory = serializers.CharField(
        required=True,
        allow_null=False,
        allow_blank=False
    )

    purpose = serializers.CharField(
        required=True,
        allow_null=False,
        allow_blank=False
    )

    # =====================================================
    # OPTIONAL FIELDS
    # =====================================================

    taluk = serializers.CharField(
        required=False,
        allow_null=True,
        allow_blank=True
    )

    village = serializers.CharField(
        required=False,
        allow_null=True,
        allow_blank=True
    )
    land_area = models.CharField(
        max_length=255,
        blank=True,
        null=True,
        validators=[validate_safe_text]
    )
    sq_ft = models.CharField(
        max_length=10,
        blank=True,
        null=True,
        validators=[validate_safe_text]
    )
    location = models.URLField(
        max_length=3000,
        blank=True,
        null=True
    )
    district = models.CharField(
        max_length=255,
        blank=True,
        null=True,
        validators=[validate_safe_text]
    )

    class Meta:

        model = Property

        fields = "__all__"

        read_only_fields = [
            "user"
        ]

    # =====================================================
    # FIELD VALIDATIONS
    # =====================================================

    def validate_owner(self, value):

        value = str(value).strip()

        if not value:

            raise serializers.ValidationError(
                "Owner is required."
            )

        return value

    def validate_subcategory(self, value):

        value = str(value).strip()

        if not value:

            raise serializers.ValidationError(
                "Subcategory is required."
            )

        sub_obj = Subcategory.objects.filter(
            name__iexact=value
        ).first()

        if not sub_obj:

            raise serializers.ValidationError(
                "Invalid subcategory."
            )

        return value

    def validate_purpose(self, value):

        value = str(value).strip()

        if not value:

            raise serializers.ValidationError(
                "Purpose is required."
            )

        pur_obj = Purpose.objects.filter(
            name__iexact=value
        ).first()

        if not pur_obj:

            raise serializers.ValidationError(
                "Invalid purpose."
            )

        return value

    def validate(self, attrs):

        request = self.context.get("request")

        is_create = self.instance is None

        # =================================================
        # REQUIRED FIELDS FOR CREATE & UPDATE
        # =================================================

        required_fields = [
            "owner",
            "category",
            "subcategory",
            "purpose",
        ]

        for field in required_fields:

            value = self.initial_data.get(field)

            if value is None:

                raise serializers.ValidationError({
                    field: f"{field} is required."
                })

            if isinstance(value, str) and not value.strip():

                raise serializers.ValidationError({
                    field: f"{field} is required."
                })

        # =================================================
        # REQUIRED CONTEXT FIELDS
        # =================================================

        # amenities = self.context.get("amenities_list")

        # selling_points = self.context.get("selling_points_list")

        # landmarks = self.context.get("land_mark_list")

        # features = self.context.get("features_list")

        # context_required_fields = {

        #     "amenities": amenities,
        #     "selling_points": selling_points,
        #     "landmarks": landmarks,
        #     "features": features,
        # }

        # for field_name, value in context_required_fields.items():

        #     if value is None:

        #         raise serializers.ValidationError({
        #             field_name: f"{field_name} is required."
        #         })

        #     if isinstance(value, list) and len(value) == 0:

        #         raise serializers.ValidationError({
        #             field_name: f"{field_name} cannot be empty."
        #         })
        amenities = self.context.get("amenities_list", [])

        selling_points = self.context.get("selling_points_list", [])

        landmarks = self.context.get("land_mark_list", [])

        features = self.context.get("features_list", [])

        # =================================================
        # PURPOSE VALIDATION
        # =================================================

        purpose = str(
            self.initial_data.get(
                "purpose",
                getattr(
                    getattr(self.instance, "purpose", None),
                    "name",
                    ""
                )
            )
        ).strip().lower()

        price = self.initial_data.get("price")

        deposit = self.initial_data.get("deposit")

        perprice = self.initial_data.get("perprice")

        # =================================================
        # RENT
        # =================================================

        if purpose == "rent":

            if price in ["", None]:

                raise serializers.ValidationError({
                    "price": "Price is required for rent."
                })

            if deposit in ["", None]:

                raise serializers.ValidationError({
                    "deposit": "Deposit is required for rent."
                })

        # =================================================
        # SALE
        # =================================================

        elif purpose == "sale":

            if price in ["", None]:

                raise serializers.ValidationError({
                    "price": "Price is required for sale."
                })

            if perprice in ["", None]:

                raise serializers.ValidationError({
                    "perprice": "Per price is required for sale."
                })

        # =================================================
        # LEASE
        # =================================================

        elif purpose == "lease":

            if price in ["", None]:

                raise serializers.ValidationError({
                    "price": "Price is required for lease."
                })

        # =================================================
        # IMAGES VALIDATION
        # =================================================

        if request:

            images = request.FILES.getlist("images")

            if is_create:

                # Minimum validation
                if not images or len(images) < 3:

                    raise serializers.ValidationError({

                        "images": (
                            "Minimum 3 property images are required."
                        )

                    })

                # Maximum validation
                if len(images) > 10:

                    raise serializers.ValidationError({

                        "images": (
                            "Maximum 10 property images are allowed."
                        )

                    })

            # if is_create and not images:

            #     raise serializers.ValidationError({
            #         "images": "Property images are required."
            #     })

        # =================================================
        # AMENITIES VALIDATION
        # =================================================

        # if not isinstance(amenities, list):

        #     raise serializers.ValidationError({
        #         "amenities": "Amenities must be list."
        #     })

        # cleaned_amenities = []

        # for a in amenities:

        #     try:

        #         cleaned_amenities.append(int(a))

        #     except Exception:

        #         raise serializers.ValidationError({
        #             "amenities": f"Invalid amenity id: {a}"
        #         })
            
        

        # =================================================
        # LANDMARK VALIDATION
        # =================================================

        # if not isinstance(landmarks, list):

        #     raise serializers.ValidationError({
        #         "landmarks": "Landmarks must be list."
        #     })

        # for item in landmarks:

        #     if not isinstance(item, dict):

        #         raise serializers.ValidationError({
        #             "landmarks": "Each landmark must be object."
        #         })

        #     name = str(item.get("name", "")).strip()

        #     distance = str(item.get("distance", "")).strip()

        #     if not name:

        #         raise serializers.ValidationError({
        #             "landmarks": "Landmark name is required."
        #         })

        #     if not distance:

        #         raise serializers.ValidationError({
        #             "landmarks": "Landmark distance is required."
        #         })
        
        # =================================================
        # SELLING POINTS VALIDATION
        # =================================================

        # if not isinstance(selling_points, list):

        #     raise serializers.ValidationError({
        #         "selling_points": "Selling points must be list."
        #     })

        # # REMOVE EMPTY VALUES
        # cleaned_selling_points = []

        # for item in selling_points:

        #     if item is None:
        #         continue

        #     item = str(item).strip()

        #     if item:
        #         cleaned_selling_points.append(item)

        # # THROW ERROR IF EMPTY
        # if len(cleaned_selling_points) == 0:

        #     raise serializers.ValidationError({
        #         "selling_points": (
        #             "Selling points cannot be empty."
        #         )
        #     })

        # =================================================
        # FEATURES VALIDATION
        # =================================================

        # if not isinstance(features, list):

        #     raise serializers.ValidationError({
        #         "features": "Features must be list."
        #     })

        # for feature in features:

        #     if not isinstance(feature, dict):

        #         raise serializers.ValidationError({
        #             "features": "Each feature must be object."
        #         })

        #     name = str(feature.get("name", "")).strip()

        #     if not name:

        #         raise serializers.ValidationError({
        #             "features": "Feature name is required."
        #         })

        return attrs
    # =====================================================
    # HELPERS
    # =====================================================

    def get_subcategory_obj(self, sub):

        if not sub:
            return None

        return Subcategory.objects.filter(
            name__iexact=str(sub).strip()
        ).first()

    def get_purpose_obj(self, pur):

        if not pur:
            return None

        return Purpose.objects.filter(
            name__iexact=str(pur).strip()
        ).first()

    # =====================================================
    # CREATE
    # =====================================================

    def create(self, validated_data):

        request = self.context.get("request")

        if request and request.user:

            validated_data["user"] = request.user

        owner_name = self.initial_data.get("owner")

        if owner_name is not None:

            validated_data["owner"] = owner_name.strip()

        sub = self.initial_data.get("subcategory")

        sub_obj = self.get_subcategory_obj(sub)

        if sub_obj:

            validated_data["subcategory"] = sub_obj

        pur = self.initial_data.get("purpose")

        pur_obj = self.get_purpose_obj(pur)

        if pur_obj:

            validated_data["purpose"] = pur_obj

        instance = Property.objects.create(
            **validated_data
        )

        self.handle_related(instance)

        return instance

    # =====================================================
    # UPDATE
    # =====================================================

    def update(self, instance, validated_data):

        request = self.context.get("request")
        if request:

            old_images = request.data.getlist("images")

            new_images = request.FILES.getlist("images")

            existing_images = instance.images.all()
            kept_images = []

            for img_obj in existing_images:

                image_url = request.build_absolute_uri(
                    img_obj.image.url
                )

                if image_url in old_images:

                    kept_images.append(img_obj)
            total_images_after_update = (
                len(kept_images) + len(new_images)
            )

            # if total_images_after_update == 0:

            #     raise serializers.ValidationError({

            #         "images": (
            #             "At least one property image is required."
            #         )

            #     })

            total_images_after_update = (
                len(old_images) + len(new_images)
            )


            if total_images_after_update < 3:

                raise serializers.ValidationError({

                    "images": (
                        "Minimum 3 property images are required."
                    )

                })

            if total_images_after_update > 10:

                raise serializers.ValidationError({

                    "images": (
                        "Maximum 10 property images are allowed."
                    )

                })

            if "images" in request.data:

                for img_obj in existing_images:

                    image_url = request.build_absolute_uri(
                        img_obj.image.url
                    )

                    if image_url not in old_images:

                        img_obj.delete()
            if new_images:

                PropertyImage.objects.bulk_create([

                    PropertyImage(
                        property=instance,
                        image=img
                    )

                    for img in new_images
                ])

        # if request:

        #     old_images = request.data.getlist("images")

        #     new_images = request.FILES.getlist("images")

        #     if "images" in request.data:

        #         for img_obj in instance.images.all():

        #             image_url = request.build_absolute_uri(
        #                 img_obj.image.url
        #             )

        #             if image_url not in old_images:
        #                 img_obj.delete()

        #     if new_images:
        #         # seen = set()
        #         # clean_images = []

        #         # for img in new_images:

        #         #     name = getattr(img, "name", None)

        #         #     if name and name not in seen:
        #         #         seen.add(name)
        #         #         clean_images.append(img)

        #         PropertyImage.objects.bulk_create([
        #             PropertyImage(
        #                 property=instance,
        #                 image=img
        #             )
        #             for img in new_images
        #         ])

        # if request and request.FILES.get("image"):

        #     instance.image = request.FILES.get("image")

        owner_name = self.initial_data.get("owner")

        if owner_name is not None:

            instance.owner = owner_name.strip()

        sub = self.initial_data.get("subcategory")

        sub_obj = self.get_subcategory_obj(sub)

        if sub_obj:

            instance.subcategory = sub_obj

        validated_data.pop("subcategory", None)

        pur = self.initial_data.get("purpose")

        pur_obj = self.get_purpose_obj(pur)

        if pur_obj:

            instance.purpose = pur_obj

        validated_data.pop("purpose", None)

        # =================================================
        # REMOVE INVALID FIELD BEFORE SAVE
        # =================================================

        # validated_data.pop("land_mark", None)
        validated_data.pop("selling_points", None)

        for k, v in validated_data.items():

            if k in [
                "owner",
                "user",
                "land_mark",
                "selling_points"
            ]:
                continue

            setattr(instance, k, v)

        instance.save()

        self.handle_related(instance)

        return instance

    # =====================================================
    # HANDLE RELATED
    # =====================================================

    def handle_related(self, instance):

        request = self.context.get("request")

        if (
            request
            and hasattr(request, "data")
            and "amenities" in request.data
        ):

            amenities = self.context.get(
                "amenities_list",
                []
            )

            if isinstance(amenities, str):

                try:
                    amenities = json.loads(
                        amenities
                    )

                except Exception:
                    amenities = []

            amenities = [
                int(a)
                for a in amenities
                if a not in ["", None]
            ]

            amenity_objects = Amenities.objects.filter(
                id__in=amenities
            )

            instance.amenities.set(
                amenity_objects
            )

        # =================================================
        # SELLING POINTS
        # =================================================

        sp = self.context.get(
            "selling_points_list",
            None
        )

        if sp is not None:

            if isinstance(sp, str):

                try:
                    sp = json.loads(sp)

                except Exception:
                    sp = []

            if not isinstance(sp, list):
                sp = []

            instance.selling_points = sp

            instance.save(
                update_fields=[
                    "selling_points"
                ]
            )

        # =================================================
        # LANDMARKS
        # =================================================

        lm = self.context.get(
            "land_mark_list",
            None
        )

        if lm is not None:

            if isinstance(lm, str):

                try:
                    lm = json.loads(lm)

                except Exception:
                    lm = []

            if not isinstance(lm, list):
                lm = []

            cleaned_landmarks = []

            for item in lm:

                if not isinstance(item, dict):
                    continue

                cleaned_landmarks.append({

                    "name": str(
                        item.get("name", "")
                    ).strip(),

                    "distance": str(
                        item.get("distance", "")
                    ).strip()
                })

            instance.land_mark = cleaned_landmarks

            instance.save(
                update_fields=[
                    "land_mark"
                ]
            )

        # =================================================
        # FEATURES
        # =================================================

        fv_list = self.context.get(
            "field_values",
            None
        )

        if fv_list is None:

            fv_list = self.context.get(
                "features_list",
                None
            )

        if fv_list is not None:

            if isinstance(fv_list, str):

                try:
                    fv_list = json.loads(
                        fv_list
                    )

                except Exception:
                    fv_list = []

            if not isinstance(fv_list, list):
                fv_list = []

            PropertyFeature.objects.filter(
                property=instance
            ).delete()

            for fv in fv_list:

                if not isinstance(fv, dict):
                    continue

                field_name = str(
                    fv.get("name", "")
                ).strip()

                if not field_name:
                    continue

                field = SubcategoryField.objects.filter(
                    subcategory=instance.subcategory,
                    field_name__iexact=field_name
                ).first()

                if not field:
                    continue

                PropertyFeature.objects.create(

                    property=instance,

                    field=field,

                    value=json.dumps({

                        "option": fv.get(
                            "option"
                        ),

                        "value": fv.get(
                            "value"
                        ),

                        "icon": fv.get(
                            "icon"
                        )
                    })
                )

    # =====================================================
    # OUTPUT
    # =====================================================

    def to_representation(self, instance):

        data = super().to_representation(
            instance
        )

        data["owner"] = (
            instance.owner
            if instance.owner
            else None
        )

        return data

    def get_amenities(self, obj):

        return [
            {
                "id": a.id,
                "name": a.name
            }
            for a in obj.amenities.all()
        ]

    def get_selling_points(self, obj):

        if isinstance(
            obj.selling_points,
            list
        ):
            return obj.selling_points

        return []

    def get_landmarks(self, obj):

        if isinstance(
            obj.land_mark,
            list
        ):
            return obj.land_mark

        return []

    def get_features(self, obj):

        data = []

        for f in obj.property_features.select_related("field"):

            try:
                value = json.loads(f.value)

            except Exception:

                value = {
                    "value": f.value
                }

            feature_name = (
                value.get("option")
                if value.get("option")
                else f.field.field_name
            )

            feature_value = value.get("value")

            if feature_value is None:
                feature_value = ""

            data.append({

                "name": feature_name,

                "value": str(feature_value),

                "icon": (
                    f.field.icon.url
                    if f.field.icon
                    else None
                )
            })

        return data

    def get_images(self, obj):

        request = self.context.get("request")

        images = obj.images.all()

        if not images:
            return []

        if request:

            return [
                request.build_absolute_uri(i.image.url)
                for i in images
                if i.image
            ]

        return [
            i.image.url
            for i in images
            if i.image
        ]

    # def get_image(self, obj):

    #     if not obj.image:
    #         return None

    #     request = self.context.get(
    #         "request"
    #     )

    #     return (
    #         request.build_absolute_uri(
    #             obj.image.url
    #         )
    #         if request
    #         else obj.image.url
    #     )
    

class AgentContactMessageSerializer(
    serializers.ModelSerializer
):

    agent_id = serializers.UUIDField(
        source="agent.id",
        read_only=True
    )

    class Meta:

        model = AgentContactMessage

        fields = [

            "id",

            "agent_id",

            "agent_name",
            "agent_email",
            "agent_phone",
            "agent_whatsapp",

            "name",
            "message",

            "status",
            "replied_at",

            "created_at"
        ]

        read_only_fields = [

            "agent_id",

            "agent_name",
            "agent_email",
            "agent_phone",
            "agent_whatsapp",

            "status",
            "replied_at",
            "created_at"
        ]


class UserPlanActivateSerializer(serializers.Serializer):

    plan_id = serializers.CharField()


class CurrentUserPlanSerializer(serializers.ModelSerializer):

    # =====================================
    # BASIC PLAN DETAILS
    # =====================================

    plan_id = serializers.UUIDField(
        source="user_plan.id",
        read_only=True
    )

    plan_type = serializers.CharField(
        source="user_plan.plan_type",
        read_only=True
    )

    name = serializers.CharField(
        source="user_plan.name",
        read_only=True
    )

    validity = serializers.CharField(
        source="user_plan.validity",
        read_only=True
    )

    price = serializers.DecimalField(
        source="user_plan.price",
        max_digits=10,
        decimal_places=2,
        read_only=True
    )

    # =====================================
    # FEATURES
    # =====================================

    features = serializers.SerializerMethodField()

    # =====================================
    # PLAN DATES
    # =====================================

    plan_start_date = serializers.DateTimeField(
        read_only=True
    )

    plan_expiry_date = serializers.DateTimeField(
        read_only=True
    )

    is_paid_user = serializers.BooleanField(
        read_only=True
    )

    user_role = serializers.CharField(
        read_only=True
    )

    class Meta:

        model = UserProfile

        fields = [
            "plan_id",
            "plan_type",
            "name",
            "validity",
            "price",
            "features",
            "plan_start_date",
            "plan_expiry_date",
            "is_paid_user",
            "user_role",
        ]

    # =====================================
    # FEATURES METHOD
    # =====================================

    def get_features(self, obj):

        plan = obj.user_plan

        if not plan:
            return {}

        return {

            "property_listing_limit":
                plan.property_listing_limit,

            "listing_type":
                plan.listing_type,

            "enquiry_limit":
                plan.enquiry_limit,

            "property_edit_option":
                plan.property_edit_option,

            "property_visibility":
                plan.property_visibility,

            "priority_search":
                plan.priority_search,

            "meta_ads_promotion":
                plan.meta_ads_promotion,

            "bulk_whatsapp_message":
                plan.bulk_whatsapp_message,

            "poster_creation":
                plan.poster_creation,

            "social_media_marketing":
                plan.social_media_marketing,

            "lead_follow_support":
                plan.lead_follow_support,

            "best_suited_for":
                plan.best_suited_for,
        }


class CreatePaymentSerializer(serializers.Serializer):

    plan_id = serializers.UUIDField()

class ReelPurchaseNotificationSerializer(serializers.ModelSerializer):

    package_name = serializers.SerializerMethodField()
    package_type = serializers.SerializerMethodField()
    price = serializers.SerializerMethodField()
    features = serializers.SerializerMethodField()

    class Meta:
        model = ReelPurchaseNotification
        fields = [
            "id",
            "title",
            "message",
            "status",
            "is_read",
            "created_at",
            "package_name",
            "package_type",
            "price",
            "features",
        ]

    def get_package_name(self, obj):
        if obj.payment and obj.payment.reel_package:
            return obj.payment.reel_package.name
        return None

    def get_package_type(self, obj):
        if obj.payment and obj.payment.reel_package:
            return obj.payment.reel_package.reel_type
        return None

    def get_price(self, obj):
        if obj.payment and obj.payment.reel_package:
            return obj.payment.reel_package.price_per_day
        return None

    def get_features(self, obj):
        if not (obj.payment and obj.payment.reel_package):
            return []

        package = obj.payment.reel_package

        features = []

        if package.reel_format:
            features.append(f"Format: {package.reel_format}")

        if package.duration:
            features.append(f"Duration: {package.duration}")

        if package.description:
            features.append(package.description)

        features.append(
            f"Price per day: ₹{package.price_per_day}"
        )

        return features
    


class PurchaseHistorySerializer(serializers.Serializer):
    plan_type = serializers.CharField()
    plan_name = serializers.CharField()
    price = serializers.DecimalField(max_digits=10, decimal_places=2)
    purchase_date = serializers.DateField(format="%Y-%m-%d")
    status = serializers.CharField()

    order_id = serializers.CharField(
        allow_null=True,
        required=False
    )

    payment_id = serializers.CharField(
        allow_null=True,
        required=False
    )

    def to_representation(self, instance):
        data = super().to_representation(instance)

        # Remove keys if they don't exist or are None
        if not instance.get("order_id"):
            data.pop("order_id", None)

        if not instance.get("payment_id"):
            data.pop("payment_id", None)

        return data
    