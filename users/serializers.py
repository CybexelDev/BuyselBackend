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
from django.db.models import Avg, Count

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

        # ---------------------
        # USER CHECK
        # ---------------------
        try:
            premium = Premium.objects.get(
                username=username
            )

        except Premium.DoesNotExist:

            raise serializers.ValidationError(
                "Invalid Username"
            )

        # ---------------------
        # PASSWORD CHECK (IMPORTANT)
        # ---------------------
        if not check_password(
            old_password,
            premium.password
        ):

            raise serializers.ValidationError(
                "Old Password Incorrect"
            )

        # ---------------------
        # CONFIRM PASSWORD
        # ---------------------
        if new_password != confirm_password:

            raise serializers.ValidationError(
                "Password Does Not Match"
            )

        data["premium"] = premium

        return data


class AgentFormSerializer(serializers.ModelSerializer):

    # ✅ Custom Image URL
    image = serializers.SerializerMethodField()

    class Meta:
        model = AgentForm
        fields = "__all__"

    # ✅ OUTSIDE Meta
    def get_image(self, obj):

        if obj.image:
            try:
                return obj.image.url   # Cloudinary full URL
            except:
                return None

        return None



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

    def validate(self, data):

        # Password match validation
        if data["password"] != data["confirm_password"]:
            raise serializers.ValidationError({
                "confirm_password": "Passwords do not match"
            })

        # Email uniqueness check
        if UserCreate.objects.filter(email=data["email"]).exists():
            raise serializers.ValidationError({
                "email": "Email already registered"
            })

        return data

    def create(self, validated_data):
        validated_data.pop("confirm_password")

        validated_data["password"] = make_password(
            validated_data["password"]
        )

        return UserCreate.objects.create(**validated_data)


class VerifyOTPSerializer(serializers.Serializer):
    email = serializers.EmailField()
    otp = serializers.CharField(max_length=6)

class ForgotPasswordSerializer(serializers.Serializer):

    email = serializers.EmailField()


class VerifyForgotOTPSerializer(serializers.Serializer):

    email = serializers.EmailField()

    otp = serializers.CharField(max_length=6)


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


# class UserProfileSerializer(serializers.ModelSerializer):

#     email = serializers.CharField(source="user.email", read_only=True)
#     mobile = serializers.CharField(source="user.mobile", required=False)
#     name = serializers.CharField(source="user.name", read_only=True)
#     city = serializers.CharField(required=False, allow_blank=True, allow_null=True)
#     is_verified = serializers.BooleanField(source="user.is_verified", read_only=True)

#     created_at = serializers.DateTimeField(format="%d-%m-%Y", read_only=True)

#     #  Cloudinary full URL
#     image = serializers.SerializerMethodField()

#     class Meta:
#         model = UserProfile
#         fields = [
#             "custom_user_id",
#             "email",
#             "name",
#             "username",
#             "full_name",
#             "mobile",
#             "alternate_mobile",
#             "city",
#             "image",
#             "auth_provider",
#             "is_active",
#             "is_verified",
#             "created_at",
#         ]

#         read_only_fields = [
#             "custom_user_id",
#             "email",
#             "name",
#             "username",
#             "auth_provider",
#             "is_active",
#             "created_at",
#             "is_verified",
#         ]

#     # ✅ Always show city
#     def to_representation(self, instance):
#         data = super().to_representation(instance)
#         data["city"] = instance.city or ""
#         return data

#     # ✅ Convert Cloudinary image to full URL
#     def get_image(self, obj):
#         if obj.image:
#             try:
#                 url, _ = cloudinary_url(
#                     obj.image.public_id,
#                     secure=True
#                 )
#                 return url
#             except Exception:
#                 return None
#         return None

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

# class AgentReviewSerializer(serializers.ModelSerializer):

#     user_name = serializers.SerializerMethodField()
#     user_image = serializers.SerializerMethodField()
#     total_likes = serializers.SerializerMethodField()
#     created_at = serializers.SerializerMethodField()

#     class Meta:
#         model = AgentReview

#         fields = [
#             "id",
#             "user_name",
#             "user_image",
#             "rating",
#             "review",
#             "total_likes",
#             "created_at"
#         ]

#     def get_user_name(self, obj):

#         if obj.user:
#             return obj.user.name

#         return "Anonymous"

#     def get_user_image(self, obj):

#         if not obj.user:
#             return None

#         try:

#             profile = obj.user.profile

#             if profile.image:
#                 return profile.image.url

#         except Exception:
#             pass
#         name = obj.user.name or "Anonymous"

#         return (
#             "https://ui-avatars.com/api/"
#             f"?name={name}"
#             "&background=random"
#             "&color=fff"
#         )

#     def get_total_likes(self, obj):

#         return obj.likes.count()

#     def get_created_at(self, obj):

#         return obj.created_at.strftime(
#             "%d-%m-%Y"
#         )
    
# import shortuuid
# class AgentReviewSerializer(serializers.ModelSerializer):
#     user_name = serializers.SerializerMethodField()
#     user_image = serializers.SerializerMethodField()
#     total_likes = serializers.SerializerMethodField()
#     created_at = serializers.SerializerMethodField()

#     class Meta:
#         model = AgentReview
#         fields = [
#             "id",
#             "user_name",
#             "user_image",
#             "rating",
#             "review",
#             "total_likes",
#             "created_at"
#         ]

#     def get_user_name(self, obj):
#         if obj.user:
#             return obj.user.name
#         return "Anonymous"

#     def get_user_image(self, obj):
#         if obj.user and obj.user.name:
#             name = obj.user.name
#         else:
#             name = "Anonymous"
#         return f"https://ui-avatars.com/api/?name={name}&background=random&color=fff"

#     def get_total_likes(self, obj):
#         return obj.likes.count()
    
#     def get_created_at(self, obj):
#         return obj.created_at.strftime("%d-%m-%Y")
    
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

class PendingAgentRegistrationSerializer(serializers.ModelSerializer):
    class Meta:
        model = PendingAgentRegistration
        fields = [
            "full_name",
            "email",
            "phone_number",
            "password",
            "city",
            "pin_code",
            "agent_type",
            "plan_name",
            "address"
        ]

    def create(self, validated_data):
        # hash password
        validated_data['password'] = make_password(validated_data['password'])
        return PendingAgentRegistration.objects.create(**validated_data)


# class AgentProfileSerializer(serializers.ModelSerializer):
#     agent_id = serializers.CharField(source='agent_code', read_only=True)
#     plan_name = serializers.SerializerMethodField()
#     profile_image = serializers.SerializerMethodField()
#     specializations = serializers.SerializerMethodField()

#     class Meta:
#         model = AgentUserProfile
#         fields = [
#             'agent_id',
#             'username',
#             'email',
#             'phone_number',
#             'whatsapp_number',
#             'address',
#             'city',
#             'pin_code',
#             'profile_image',
#             'professional_title',
#             'professional_bio',
#             'years_of_experience',
#             'properties_listed',
#             'deals_closed',
#             'specializations',
#             'operating_cities',
#             'instagram',
#             'facebook',
#             'website',
#             'agent_type',
#             'plan_name',
#             'paid',
#             'plan_start_date',
#             'plan_expiry_date',
#             'created_at'
#         ]

#     def get_profile_image(self, obj):
#         return obj.get_profile_image()

#     def get_specializations(self, obj):
#         return [cat.name for cat in obj.specializations.all()]

#     def get_plan_name(self, obj):
#         if obj.plan:
#             return obj.plan.name
#         if obj.elite_plan:
#             return obj.elite_plan.name
#         return None

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

from .utils import hashids
from django.db import IntegrityError, transaction
import time

# class AgentPropertySerializer(serializers.ModelSerializer):

#     id = serializers.SerializerMethodField()
#     images = serializers.SerializerMethodField()
#     image = serializers.SerializerMethodField()
#     amenities = serializers.SerializerMethodField()
#     selling_points = serializers.SerializerMethodField()
#     landmarks = serializers.SerializerMethodField()
#     features = serializers.SerializerMethodField()
#     screenshot = serializers.SerializerMethodField()

#     category = serializers.PrimaryKeyRelatedField(queryset=Category.objects.all())
#     subcategory = serializers.CharField(required=False, allow_null=True, allow_blank=True)
#     purpose = serializers.CharField()
#     wishlisted = serializers.SerializerMethodField()

#     class Meta:
#         model = AgentProperty
#         fields = "__all__"
#         read_only_fields = ["agent", "phone", "whatsapp"]

#     def get_screenshot(self, obj):
#         return obj.screenshot.url if obj.screenshot else None

#     def get_wishlisted(self, obj):
#         request = self.context.get("request")
#         user = getattr(request, "user", None)

#         if not user or not user.is_authenticated:
#             return False

#         return Wishlist.objects.filter(
#             user=user,
#             property=obj
#         ).exists()
    
#     def get_id(self, obj):
#         return hashids.encode(obj.id)

#     # ================= CREATE =================
#     def create(self, validated_data):
#         request = self.context["request"]
#         agent = request.user

#         validated_data = self.handle_foreign_keys(validated_data)

#         amenities_list = self.context.get("amenities_list", [])
#         selling_points_list = self.context.get("selling_points_list", [])
#         landmarks_list = self.context.get("landmarks_list", [])
#         field_values = self.context.get("field_values", [])

#         # ================= SUBCATEGORY (NAME → OBJECT) =================
#         subcategory_name = validated_data.pop("subcategory", None)
#         subcategory_obj = None

#         if subcategory_name:
#             subcategory_obj = Subcategory.objects.filter(
#                 name__iexact=subcategory_name.strip()
#             ).first()

#             if not subcategory_obj:
#                 raise serializers.ValidationError({
#                     "subcategory": "Invalid subcategory name"
#                 })

#         # ================= PURPOSE (NAME → OBJECT) =================
#         purpose_name = validated_data.pop("purpose", None)

#         purpose_obj = Purpose.objects.filter(
#             name__iexact=purpose_name.strip()
#         ).first()

#         if not purpose_obj:
#             raise serializers.ValidationError({
#                 "purpose": "Invalid purpose name"
#             })

#         # ================= CREATE PROPERTY =================
#         # instance = AgentProperty.objects.create(
#         #     agent=request.user,
#         #     subcategory=subcategory_obj,
#         #     purpose=purpose_obj,
#         #     **validated_data
#         # )

#         instance = None

#         for _ in range(5):  # retry max 5 times
#             try:
#                 with transaction.atomic():
#                     instance = AgentProperty.objects.create(
#                         agent=request.user,
#                         subcategory=subcategory_obj,
#                         purpose=purpose_obj,
#                         **validated_data
#                     )
#                 break  # success

#             except IntegrityError as e:
#                 if "property_code" in str(e):
#                     time.sleep(0.1)  # small delay before retry
#                     continue
#                 raise e

#         if not instance:
#             raise serializers.ValidationError("Unable to create property. Please try again.")

#         # ================= AMENITIES =================
#         if amenities_list:
#             instance.amenities.set(amenities_list)

#         # SELLING POINTS
#         if selling_points_list:
#             instance.selling_points.all().delete()
#             AgentPropertySellingPoint.objects.bulk_create([
#                 AgentPropertySellingPoint(property=instance, point=sp)
#                 for sp in selling_points_list
#             ])

#         # LANDMARKS
#         if landmarks_list:
#             instance.landmarks.all().delete()
#             AgentPropertyLandmark.objects.bulk_create([
#                 AgentPropertyLandmark(
#                     property=instance,
#                     name=lm.get("name"),
#                     distance=lm.get("distance")
#                 )
#                 for lm in landmarks_list if isinstance(lm, dict)
#             ])

#         # FEATURES
#         if field_values:
#             instance.field_values.all().delete()

#             for fv in field_values:
#                 if not isinstance(fv, dict):
#                     raise serializers.ValidationError("Invalid field_values format")

#                 name = fv.get("name")
#                 value = fv.get("value")

#                 if not name:
#                     raise serializers.ValidationError("Feature name missing")

#                 name = name.strip()

#                 option = FieldOption.objects.filter(
#                     name__iexact=name,
#                     field__subcategory=instance.subcategory
#                 ).select_related("field").first()

#                 if option:
#                     field = option.field
#                 else:
#                     field = SubcategoryField.objects.filter(
#                         subcategory=instance.subcategory,
#                         field_name__iexact=name
#                     ).first()

#                 if not field:
#                     raise serializers.ValidationError(f"Invalid feature: {name}")

#                 if field.field_type == "countable":
#                     AgentPropertyFieldValue.objects.create(
#                         property=instance,
#                         field=field,
#                         value=name
#                     )
#                 else:
#                     AgentPropertyFieldValue.objects.create(
#                         property=instance,
#                         field=field,
#                         value=str(value)
#                     )

#     # ================= RESPONSE =================
#     def get_features(self, obj):
#         result = []

#         for fv in obj.field_values.select_related("field"):
#             field = fv.field

#             if field.field_type == "countable" and fv.value:
#                 for v in fv.value.split(","):
#                     result.append({"name": v.strip(), "value": 1})
#             else:
#                 result.append({
#                     "name": field.field_name,
#                     "value": fv.value
#                 })

#         return result

#     def get_images(self, obj):
#         return [img.image.url for img in obj.images.all() if img.image]

#     def get_image(self, obj):
#         return obj.image.url if obj.image else None

#     def get_amenities(self, obj):
#         return [{"id": a.id, "name": a.name} for a in obj.amenities.all()]

#     def get_selling_points(self, obj):
#         return list(obj.selling_points.values_list("point", flat=True))

#     def get_landmarks(self, obj):
#         return [{"name": l.name, "distance": l.distance} for l in obj.landmarks.all()]

# from .utils import encode_id
# class AgentPropertySerializer(serializers.ModelSerializer):

#     id = serializers.UUIDField(
#         source="uuid",
#         read_only=True
#     )
#     images = serializers.SerializerMethodField()
#     image = serializers.SerializerMethodField()
#     amenities = serializers.SerializerMethodField()
#     selling_points = serializers.SerializerMethodField()
#     landmarks = serializers.SerializerMethodField()
#     features = serializers.SerializerMethodField()

#     category = serializers.PrimaryKeyRelatedField(queryset=Category.objects.all())
#     subcategory = serializers.CharField(required=False, allow_null=True, allow_blank=True)
#     purpose = serializers.CharField()

#     class Meta:
#         model = AgentProperty
#         fields = "__all__"
#         read_only_fields = ["agent", "phone", "whatsapp"]

#     # def get_id(self, obj):
#     #     return encode_id(obj.id)

#     # ================= FK HANDLER =================
#     def handle_foreign_keys(self, validated_data):

#         subcategory_name = self.initial_data.get("subcategory")
#         if subcategory_name:
#             subcategory = Subcategory.objects.filter(
#                 name__iexact=subcategory_name.strip()
#             ).first()
#             if not subcategory:
#                 raise serializers.ValidationError({"subcategory": "Invalid subcategory"})
#             validated_data["subcategory"] = subcategory

#         purpose_name = self.initial_data.get("purpose")
#         if purpose_name:
#             purpose = Purpose.objects.filter(
#                 name__iexact=purpose_name.strip()
#             ).first()
#             if not purpose:
#                 raise serializers.ValidationError({"purpose": "Invalid purpose"})
#             validated_data["purpose"] = purpose

#         return validated_data

#     # ================= CREATE =================
#     def create(self, validated_data):
#         request = self.context["request"]
#         agent = request.user

#         validated_data = self.handle_foreign_keys(validated_data)

#         instance = AgentProperty.objects.create(
#             agent=agent,
#             phone=agent.phone_number,
#             whatsapp=agent.whatsapp_number,
#             **validated_data
#         )

#         self.handle_related_fields(instance)
#         return instance

#     # ================= UPDATE =================
#     def update(self, instance, validated_data):

#         validated_data = self.handle_foreign_keys(validated_data)
#         instance = super().update(instance, validated_data)

#         self.handle_related_fields(instance)
#         return instance

#     # ================= RELATED HANDLER =================
#     def handle_related_fields(self, instance):

#         amenities_list = self.context.get("amenities_list", [])
#         selling_points_list = self.context.get("selling_points_list", [])
#         landmarks_list = self.context.get("landmarks_list", [])
#         field_values = self.context.get("field_values", [])

#         # -------- AMENITIES --------
#         if amenities_list:
#             instance.amenities.set(amenities_list)

#         # -------- SELLING POINTS --------
#         if selling_points_list:
#             instance.selling_points.all().delete()
#             AgentPropertySellingPoint.objects.bulk_create([
#                 AgentPropertySellingPoint(property=instance, point=sp)
#                 for sp in selling_points_list
#             ])

#         # -------- LANDMARKS --------
#         if landmarks_list:
#             instance.landmarks.all().delete()
#             AgentPropertyLandmark.objects.bulk_create([
#                 AgentPropertyLandmark(
#                     property=instance,
#                     name=lm.get("name"),
#                     distance=lm.get("distance")
#                 )
#                 for lm in landmarks_list if isinstance(lm, dict)
#             ])

#         # -------- FEATURES (FINAL LOGIC) --------
#         if field_values:

#             for fv in field_values:
#                 if not isinstance(fv, dict):
#                     raise serializers.ValidationError("Invalid field_values format")

#                 field_name = fv.get("name")       # flat furnishings / bhk type
#                 option_name = fv.get("option")   # Wardrobe / TV
#                 value = fv.get("value")          # 3 / 1 / "3 bhk"

#                 if not field_name:
#                     raise serializers.ValidationError("Feature name missing")

#                 field = SubcategoryField.objects.filter(
#                     subcategory=instance.subcategory,
#                     field_name__iexact=field_name.strip()
#                 ).first()

#                 if not field:
#                     raise serializers.ValidationError(f"Invalid feature: {field_name}")

#                 # -------- OPTION BASED FIELD --------
#                 if option_name:
#                     option = FieldOption.objects.filter(
#                         name__iexact=option_name.strip(),
#                         field=field
#                     ).first()

#                     if not option:
#                         raise serializers.ValidationError(f"Invalid option: {option_name}")

#                     try:
#                         value = int(value)
#                     except:
#                         raise serializers.ValidationError(f"{option_name} must be a number")

#                     # remove existing same option
#                     AgentPropertyFieldValue.objects.filter(
#                         property=instance,
#                         field=field,
#                         value__icontains=f'"option": "{option.name}"'
#                     ).delete()

#                     # save JSON
#                     AgentPropertyFieldValue.objects.create(
#                         property=instance,
#                         field=field,
#                         value=json.dumps({
#                             "option": option.name,
#                             "count": value
#                         })
#                     )

#                 # -------- NORMAL FIELD --------
#                 else:
#                     AgentPropertyFieldValue.objects.filter(
#                         property=instance,
#                         field=field
#                     ).delete()

#                     AgentPropertyFieldValue.objects.create(
#                         property=instance,
#                         field=field,
#                         value=str(value)
#                     )

#     # ================= CLEAN RESPONSE =================
#     def get_features(self, obj):
#         result = {}

#         for fv in obj.field_values.select_related("field"):
#             field = fv.field

#             # -------- TRY NEW JSON STRUCTURE --------
#             try:
#                 data = json.loads(fv.value)

#                 option = data.get("option")
#                 count = data.get("count", 0)

#                 if option:
#                     result[option] = count
#                     continue

#             except Exception:
#                 pass

#             # -------- SKIP OLD BROKEN DATA --------
#             if field.field_name.lower() == "flat furnishings":
#                 continue

#             # -------- NORMAL FIELD --------
#             if field.field_type == "countable":
#                 try:
#                     value = int(fv.value)
#                 except:
#                     value = 0
#             else:
#                 value = fv.value

#             result[field.field_name] = value

#         return [
#             {"name": k, "value": v}
#             for k, v in result.items()
#         ]

#     # ================= OTHER =================
#     def get_images(self, obj):
#         return [img.image.url for img in obj.images.all() if img.image]

#     def get_image(self, obj):
#         return obj.image.url if obj.image else None

#     def get_amenities(self, obj):
#         return [{"id": a.id, "name": a.name} for a in obj.amenities.all()]

#     def get_selling_points(self, obj):
#         return list(obj.selling_points.values_list("point", flat=True))

#     def get_landmarks(self, obj):
#         return [{"name": l.name, "distance": l.distance} for l in obj.landmarks.all()]

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

        if purpose_name == "sale":

            if not price:
                raise serializers.ValidationError({
                    "price": "Price is required for sale"
                })

            if not perprice:
                raise serializers.ValidationError({
                    "perprice": "Per price is required for sale"
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

        validated_data = self.handle_foreign_keys(
            validated_data
        )

        instance = super().update(
            instance,
            validated_data
        )

        self.handle_related_fields(instance)

        return instance

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

    # =====================================================
    # FEATURES
    # =====================================================

    def get_features(self, obj):

        result = {}

        for fv in obj.field_values.select_related(
            "field"
        ):

            field = fv.field

            icon = (
                field.icon.url
                if field.icon else None
            )

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

            if field.field_name.lower() == "flat furnishings":
                continue

            if field.field_type == "countable":

                try:
                    value = int(fv.value)

                except:
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
    # OTHER FIELDS
    # =====================================================

    def get_images(self, obj):

        request = self.context.get("request")

        urls = []

        for img in obj.images.all():

            if img.image:

                try:
                    url = img.image.url

                    if request:
                        url = request.build_absolute_uri(url)

                    urls.append(url)

                except:
                    pass

        return urls

    def get_image(self, obj):

        if not obj.image:
            return None

        request = self.context.get("request")

        try:

            url = obj.image.url

            if request:
                return request.build_absolute_uri(url)

            return url

        except:
            return None

    def get_amenities(self, obj):

        return [
            {
                "id": a.id,
                "name": a.name
            }
            for a in obj.amenities.all()
        ]

    def get_selling_points(self, obj):

        return list(
            obj.selling_points.values_list(
                "point",
                flat=True
            )
        )

    def get_landmarks(self, obj):

        return [
            {
                "name": l.name,
                "distance": l.distance
            }
            for l in obj.landmarks.all()
        ]

# class AgentPropertySerializer(serializers.ModelSerializer):

#     id = serializers.UUIDField(
#         # source="uuid",
#         read_only=True
#     )

#     images = serializers.SerializerMethodField()
#     image = serializers.SerializerMethodField()
#     amenities = serializers.SerializerMethodField()
#     selling_points = serializers.SerializerMethodField()
#     landmarks = serializers.SerializerMethodField()
#     features = serializers.SerializerMethodField()

#     # =========================================
#     # INPUT FIELDS
#     # =========================================

#     category = serializers.PrimaryKeyRelatedField(
#         queryset=Category.objects.all()
#     )

#     subcategory = serializers.CharField(
#         required=False,
#         allow_null=True,
#         allow_blank=True
#     )

#     purpose = serializers.CharField(
#         required=False,
#         allow_null=True,
#         allow_blank=True
#     )

#     class Meta:
#         model = AgentProperty

#         exclude = [
#             "property_hash_id"
#         ]

#         # ONLY THESE ARE READ ONLY
#         read_only_fields = [
#             "agent",
#             "id"
#         ]

#     # =====================================================
#     # FK HANDLER
#     # =====================================================

#     def handle_foreign_keys(self, validated_data):

#         # =========================================
#         # SUBCATEGORY
#         # =========================================

#         subcategory_name = self.initial_data.get(
#             "subcategory"
#         )

#         if subcategory_name:

#             subcategory = Subcategory.objects.filter(
#                 name__iexact=str(subcategory_name).strip()
#             ).first()

#             if not subcategory:
#                 raise serializers.ValidationError({
#                     "subcategory": "Invalid subcategory"
#                 })

#             validated_data["subcategory"] = subcategory

#         # =========================================
#         # PURPOSE
#         # =========================================

#         purpose_name = self.initial_data.get(
#             "purpose"
#         )

#         if purpose_name:

#             purpose = Purpose.objects.filter(
#                 name__iexact=str(purpose_name).strip()
#             ).first()

#             if not purpose:
#                 raise serializers.ValidationError({
#                     "purpose": "Invalid purpose"
#                 })

#             validated_data["purpose"] = purpose

#         return validated_data

#     # =====================================================
#     # VALIDATION
#     # =====================================================

#     def validate(self, attrs):

#         """
#         FIX FOR:
#         'str' object has no attribute 'name'
#         """

#         purpose_obj = None

#         # =========================================
#         # GET PURPOSE
#         # =========================================

#         if "purpose" in attrs:

#             purpose_value = attrs.get("purpose")

#             # IF STRING
#             if isinstance(purpose_value, str):

#                 purpose_obj = Purpose.objects.filter(
#                     name__iexact=purpose_value.strip()
#                 ).first()

#             else:
#                 purpose_obj = purpose_value

#         elif self.instance:
#             purpose_obj = self.instance.purpose

#         # no purpose
#         if not purpose_obj:
#             return attrs

#         # =========================================
#         # PURPOSE NAME
#         # =========================================

#         purpose_name = str(
#             purpose_obj.name
#         ).lower().strip()

#         # =========================================
#         # VALUES
#         # =========================================

#         price = attrs.get(
#             "price",
#             getattr(self.instance, "price", None)
#         )

#         perprice = attrs.get(
#             "perprice",
#             getattr(self.instance, "perprice", None)
#         )

#         deposit = attrs.get(
#             "deposit",
#             getattr(self.instance, "deposit", None)
#         )

#         # =========================================
#         # SALE
#         # =========================================

#         if purpose_name == "sale":

#             if not price:
#                 raise serializers.ValidationError({
#                     "price": "Price is required for sale"
#                 })

#             if not perprice:
#                 raise serializers.ValidationError({
#                     "perprice": "Per price is required for sale"
#                 })

#             # REMOVE UNWANTED
#             attrs["deposit"] = None

#         # =========================================
#         # RENT
#         # =========================================

#         elif purpose_name == "rent":

#             if not price:
#                 raise serializers.ValidationError({
#                     "price": "Rent amount is required"
#                 })

#             if not deposit:
#                 raise serializers.ValidationError({
#                     "deposit": "Deposit is required for rent"
#                 })

#             # REMOVE UNWANTED
#             attrs["perprice"] = None

#         # =========================================
#         # LEASE
#         # =========================================

#         elif purpose_name == "lease":

#             if not price:
#                 raise serializers.ValidationError({
#                     "price": "Price is required for lease"
#                 })

#             # REMOVE UNWANTED
#             attrs["deposit"] = None
#             attrs["perprice"] = None

#         return attrs

#     # =====================================================
#     # CREATE
#     # =====================================================

#     def create(self, validated_data):

#         request = self.context["request"]

#         agent = request.user

#         validated_data = self.handle_foreign_keys(
#             validated_data
#         )

#         # AUTO PHONE ONLY IF EMPTY
#         if not validated_data.get("phone"):
#             validated_data["phone"] = agent.phone_number

#         if not validated_data.get("whatsapp"):
#             validated_data["whatsapp"] = agent.whatsapp_number

#         instance = AgentProperty.objects.create(
#             agent=agent,
#             **validated_data
#         )

#         self.handle_related_fields(instance)

#         return instance

#     # =====================================================
#     # UPDATE
#     # =====================================================

#     def update(self, instance, validated_data):

#         validated_data = self.handle_foreign_keys(
#             validated_data
#         )

#         instance = super().update(
#             instance,
#             validated_data
#         )

#         self.handle_related_fields(instance)

#         return instance

#     # =====================================================
#     # RELATED FIELDS
#     # =====================================================

#     def handle_related_fields(self, instance):

#         amenities_list = self.context.get(
#             "amenities_list",
#             []
#         )

#         selling_points_list = self.context.get(
#             "selling_points_list",
#             []
#         )

#         landmarks_list = self.context.get(
#             "landmarks_list",
#             []
#         )

#         field_values = self.context.get(
#             "field_values",
#             []
#         )

#         # =========================================
#         # AMENITIES
#         # =========================================

#         if amenities_list:

#             instance.amenities.set(
#                 amenities_list
#             )

#         # =========================================
#         # SELLING POINTS
#         # =========================================

#         if selling_points_list:

#             instance.selling_points.all().delete()

#             AgentPropertySellingPoint.objects.bulk_create([

#                 AgentPropertySellingPoint(
#                     property=instance,
#                     point=sp
#                 )

#                 for sp in selling_points_list
#             ])

#         # =========================================
#         # LANDMARKS
#         # =========================================

#         if landmarks_list:

#             instance.landmarks.all().delete()

#             AgentPropertyLandmark.objects.bulk_create([

#                 AgentPropertyLandmark(
#                     property=instance,
#                     name=lm.get("name"),
#                     distance=lm.get("distance")
#                 )

#                 for lm in landmarks_list
#                 if isinstance(lm, dict)
#             ])

#         # =========================================
#         # FEATURES
#         # =========================================

#         if field_values:

#             for fv in field_values:

#                 if not isinstance(fv, dict):
#                     raise serializers.ValidationError(
#                         "Invalid field_values format"
#                     )

#                 field_name = fv.get("name")
#                 option_name = fv.get("option")
#                 value = fv.get("value")

#                 if not field_name:
#                     raise serializers.ValidationError(
#                         "Feature name missing"
#                     )

#                 field = SubcategoryField.objects.filter(
#                     subcategory=instance.subcategory,
#                     field_name__iexact=field_name.strip()
#                 ).first()

#                 if not field:
#                     raise serializers.ValidationError(
#                         f"Invalid feature: {field_name}"
#                     )

#                 # =========================================
#                 # OPTION FIELD
#                 # =========================================

#                 if option_name:

#                     option = FieldOption.objects.filter(
#                         name__iexact=option_name.strip(),
#                         field=field
#                     ).first()

#                     if not option:
#                         raise serializers.ValidationError(
#                             f"Invalid option: {option_name}"
#                         )

#                     try:
#                         value = int(value)

#                     except:
#                         raise serializers.ValidationError(
#                             f"{option_name} must be a number"
#                         )

#                     AgentPropertyFieldValue.objects.filter(
#                         property=instance,
#                         field=field,
#                         value__icontains=f'"option": "{option.name}"'
#                     ).delete()

#                     AgentPropertyFieldValue.objects.create(
#                         property=instance,
#                         field=field,
#                         value=json.dumps({
#                             "option": option.name,
#                             "count": value
#                         })
#                     )

#                 # =========================================
#                 # NORMAL FIELD
#                 # =========================================

#                 else:

#                     AgentPropertyFieldValue.objects.filter(
#                         property=instance,
#                         field=field
#                     ).delete()

#                     AgentPropertyFieldValue.objects.create(
#                         property=instance,
#                         field=field,
#                         value=str(value)
#                     )

#     # =====================================================
#     # CLEAN OUTPUT
#     # =====================================================

#     def to_representation(self, instance):

#         data = super().to_representation(
#             instance
#         )

#         # =========================================
#         # PURPOSE NAME
#         # =========================================

#         data["purpose"] = (
#             instance.purpose.name
#             if instance.purpose else None
#         )

#         # =========================================
#         # SUBCATEGORY NAME
#         # =========================================

#         data["subcategory"] = (
#             instance.subcategory.name
#             if instance.subcategory else None
#         )

#         purpose = (
#             instance.purpose.name.lower().strip()
#             if instance.purpose else ""
#         )

#         # =========================================
#         # RENT
#         # =========================================

#         if purpose == "rent":

#             data.pop("perprice", None)

#         # =========================================
#         # SALE
#         # =========================================

#         elif purpose == "sale":

#             data.pop("deposit", None)

#         # =========================================
#         # LEASE
#         # =========================================

#         elif purpose == "lease":

#             data.pop("deposit", None)
#             data.pop("perprice", None)

#         return data

#     # =====================================================
#     # FEATURES
#     # =====================================================

#     # def get_features(self, obj):

#     #     result = {}

#     #     for fv in obj.field_values.select_related(
#     #         "field"
#     #     ):

#     #         field = fv.field

#     #         try:

#     #             data = json.loads(fv.value)

#     #             option = data.get("option")

#     #             count = data.get("count", 0)

#     #             if option:

#     #                 result[option] = count
#     #                 continue

#     #         except Exception:
#     #             pass

#     #         if field.field_name.lower() == "flat furnishings":
#     #             continue

#     #         if field.field_type == "countable":

#     #             try:
#     #                 value = int(fv.value)

#     #             except:
#     #                 value = 0

#     #         else:
#     #             value = fv.value

#     #         result[field.field_name] = value

#     #     return [
#     #         {
#     #             "name": k,
#     #             "value": v
#     #         }
#     #         for k, v in result.items()
#     #     ]

#     def get_features(self, obj):

#         result = {}

#         for fv in obj.field_values.select_related(
#             "field"
#         ):

#             field = fv.field

#             icon = (
#                 field.icon.url
#                 if field.icon else None
#             )

#             try:

#                 data = json.loads(fv.value)

#                 option = data.get("option")

#                 count = data.get("count", 0)

#                 if option:

#                     result[option] = {
#                         "value": count,
#                         "icon": icon
#                     }

#                     continue

#             except Exception:
#                 pass

#             if field.field_name.lower() == "flat furnishings":
#                 continue

#             if field.field_type == "countable":

#                 try:
#                     value = int(fv.value)

#                 except:
#                     value = 0

#             else:
#                 value = fv.value

#             result[field.field_name] = {
#                 "value": value,
#                 "icon": icon
#             }

#         return [
#             {
#                 "name": k,
#                 "value": v["value"],
#                 "icon": v["icon"]
#             }
#             for k, v in result.items()
#         ]

#     # =====================================================
#     # OTHER FIELDS
#     # =====================================================

#     def get_images(self, obj):

#         return [
#             img.image.url
#             for img in obj.images.all()
#             if img.image
#         ]

#     def get_image(self, obj):

#         return (
#             obj.image.url
#             if obj.image else None
#         )

#     def get_amenities(self, obj):

#         return [
#             {
#                 "id": a.id,
#                 "name": a.name
#             }
#             for a in obj.amenities.all()
#         ]

#     def get_selling_points(self, obj):

#         return list(
#             obj.selling_points.values_list(
#                 "point",
#                 flat=True
#             )
#         )

#     def get_landmarks(self, obj):

#         return [
#             {
#                 "name": l.name,
#                 "distance": l.distance
#             }
#             for l in obj.landmarks.all()
#         ]
    
    
# class AgentPropertyEnquirySerializer(serializers.ModelSerializer):

#     class Meta:
#         model = AgentPropertyEnquiry
#         fields = "__all__"
#         read_only_fields = ["user", "agent_property"]

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
    owner = serializers.CharField(source="owner.name")
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

# from .utils import hashids

# class PropertyCardSerializer(serializers.ModelSerializer):

#     id = serializers.UUIDField(source="uuid", read_only=True)
#     owner = serializers.CharField(source="owner.name")
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
#             "is_wishlisted"
#         ]

#     def get_images(self, obj):
#         return [
#             img.image.url
#             for img in obj.images.all()[:2]
#             if img.image
#         ]

#     def get_is_wishlisted(self, obj):
#         wishlist_ids = self.context.get("wishlist_ids", set())

#         # ✅ MUST compare UUID to UUID
#         return obj.uuid in wishlist_ids
    
# class WishlistSerializer(serializers.ModelSerializer):
#         id = serializers.SerializerMethodField()  # 👈 masked id
#         owner = serializers.CharField(source="owner.name")
#         images = serializers.SerializerMethodField()
#         is_wishlisted = serializers.SerializerMethodField()

#         class Meta:
#             model = Property
#             fields = [
#                 "id",
#                 "label",
#                 "city",
#                 "perprice",
#                 "price",
#                 "sq_ft",
#                 "land_area",
#                 "owner",
#                 "whatsapp",
#                 "phone",
#                 "location",
#                 "images",
#                 "is_wishlisted"
#             ]

#         def get_id(self, obj):
#             return hashids.encode(obj.id)

#         def get_images(self, obj):
#             return [
#                 img.image.url
#                 for img in obj.images.all()[:2]
#                 if img.image
#             ]

#         def get_is_wishlisted(self, obj):
#             return True  # 👈 since it's wishlist



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



# from rest_framework import serializers
# from .models import Property
# from .utils import hashids


# class PropertyDetailSerializer(serializers.ModelSerializer):

#     # -----------------------------
#     # CUSTOM FIELDS
#     # -----------------------------
#     id = serializers.SerializerMethodField()
#     images = serializers.SerializerMethodField()

#     purpose = serializers.SerializerMethodField()
#     category = serializers.SerializerMethodField()
#     subcategory = serializers.SerializerMethodField()

#     created_at = serializers.DateTimeField(
#         format="%Y-%m-%d"
#     )

#     property_features = serializers.SerializerMethodField()
#     price_details = serializers.SerializerMethodField()
#     contact_details = serializers.SerializerMethodField()
#     amenities = serializers.SerializerMethodField()

#     # -----------------------------
#     # META
#     # -----------------------------
#     class Meta:
#         model = Property
#         fields = [
#             "id",
#             "property_code",
#             "label",
#             "images",  # ✅ multiple images
#             "purpose",
#             "category",
#             "subcategory",
#             "description",
#             "city",
#             "state",
#             "location",
#             "land_mark",
#             "created_at",
#             "property_features",
#             "price_details",
#             "contact_details",
#             "amenities",
#         ]

#     # --------------------------------------------------
#     # HASHED ID
#     # --------------------------------------------------
#     def get_id(self, obj):
#         return hashids.encode(obj.id)

#     # --------------------------------------------------
#     # MULTIPLE PROPERTY IMAGES ✅
#     # --------------------------------------------------
#     def get_images(self, obj):
#         request = self.context.get("request")

#         images = []

#         for img in obj.images.all():  # related_name="images"
#             if img.image:
#                 url = img.image.url
#                 if request:
#                     url = request.build_absolute_uri(url)
#                 images.append(url)

#         return images

#     # --------------------------------------------------
#     # PURPOSE
#     # --------------------------------------------------
#     def get_purpose(self, obj):
#         return obj.purpose.name if obj.purpose else None

#     # --------------------------------------------------
#     # CATEGORY WITH IMAGE
#     # --------------------------------------------------
#     def get_category(self, obj):
#         request = self.context.get("request")

#         if not obj.category:
#             return None

#         image_url = None
#         if getattr(obj.category, "image", None):
#             image_url = obj.category.image.url
#             if request:
#                 image_url = request.build_absolute_uri(image_url)

#         return {
#             "id": obj.category.id,
#             "name": obj.category.name,
#             "image": image_url,
#         }

#     # --------------------------------------------------
#     # SUBCATEGORY + FIELD ICONS ✅
#     # --------------------------------------------------
#     def get_subcategory(self, obj):
#         request = self.context.get("request")

#         if not obj.subcategory:
#             return None

#         fields = []

#         for field in obj.subcategory.fields.all():
#             icon_url = None
#             if field.icon:
#                 icon_url = field.icon.url
#                 if request:
#                     icon_url = request.build_absolute_uri(icon_url)

#             fields.append({
#                 "id": field.id,
#                 "field_name": field.field_name,
#                 "field_type": field.field_type,
#                 "required": field.required,
#                 "icon": icon_url,
#             })

#         return {
#             "id": obj.subcategory.id,
#             "name": obj.subcategory.name,
#             "fields": fields,
#         }

#     # --------------------------------------------------
#     # PROPERTY FEATURES
#     # --------------------------------------------------
#     def get_property_features(self, obj):
#         return obj.dynamic_fields or {}

#     # --------------------------------------------------
#     # PRICE DETAILS
#     # --------------------------------------------------
#     def get_price_details(self, obj):
#         return {
#             "price": obj.price,
#             "sq_ft": obj.sq_ft,
#             "land_area": obj.land_area,
#             "perprice": obj.perprice,
#         }

#     # --------------------------------------------------
#     # CONTACT DETAILS
#     # --------------------------------------------------
#     def get_contact_details(self, obj):
#         return {
#             "owner": getattr(obj.owner, "name", str(obj.owner)),
#             "whatsapp": obj.whatsapp,
#             "phone": obj.phone,
#         }

#     # --------------------------------------------------
#     # AMENITIES
#     # --------------------------------------------------
#     def get_amenities(self, obj):
#         return list(
#             obj.amenities.values_list("name", flat=True)
#         )
    




# from rest_framework import serializers
# from .models import Property
# from .utils import hashids


# class PropertyDetailSerializer(serializers.ModelSerializer):

#     # -----------------------------
#     # CUSTOM FIELDS
#     # -----------------------------
#     id = serializers.UUIDField(source="uuid", read_only=True)
#     images = serializers.SerializerMethodField()

#     purpose = serializers.SerializerMethodField()
#     category = serializers.SerializerMethodField()
#     # subcategory = serializers.SerializerMethodField()

#     created_at = serializers.DateTimeField(
#         format="%Y-%m-%d"
#     )

#     property_features = serializers.SerializerMethodField()
#     price_details = serializers.SerializerMethodField()
#     contact_details = serializers.SerializerMethodField()
#     owner_profile_image = serializers.SerializerMethodField()
#     amenities = serializers.SerializerMethodField()

#     # ✅ NEW (ONLY ADDITION)
#     key_selling_points = serializers.SerializerMethodField()
#     land_mark = serializers.SerializerMethodField()
#     location_details = serializers.SerializerMethodField()

#     # -----------------------------
#     # META
#     # -----------------------------
#     class Meta:
#         model = Property
#         fields = [
#             "id",
#             "property_code",
#             "label",
#             "images",
#             "purpose",
#             "category",
#             # "subcategory",
#             "description",
#             "city",
#             "state",
#             "location",
#             "land_mark",           # ✅ list output
#             "created_at",
#             "property_features",
#             "price_details",
#             "contact_details",
#             "owner_profile_image",
#             "amenities",
#             "key_selling_points",  # ✅ added
#             "location_details",
#         ]

#     def get_owner_profile_image(self, obj):

#         if not obj.owner:
#             return None

#         owner = obj.owner

#         # --------------------------------
#         # 1. Uploaded profile image
#         # --------------------------------
#         try:
#             if hasattr(owner, "profile") and owner.profile:

#                 profile = owner.profile

#                 if profile.image:
#                     image_val = str(profile.image)

#                     # ignore old default vector placeholder
#                     if (
#                         image_val and
#                         "Vector_te4oj7" not in image_val
#                     ):
#                         try:
#                             return profile.image.url
#                         except Exception:
#                             pass

#         except Exception:
#             pass


#         # --------------------------------
#         # 2. Fallback initials avatar
#         # --------------------------------
#         name = (
#             getattr(owner, "name", "")
#             or "User"
#         ).strip()

#         words = name.split()

#         if len(words) >= 2:
#             initials = (
#                 words[0][0] +
#                 words[1][0]
#             ).upper()
#         else:
#             initials = name[:2].upper()


#         return (
#             "https://ui-avatars.com/api/"
#             f"?name={initials}"
#             "&background=8bc83f"
#             "&color=ffffff"
#             "&size=256"
#             "&bold=true"
#         )


#     # --------------------------------------------------
#     # LOCATION DETAILS (NEW FIELD)
#     # --------------------------------------------------
#     def get_location_details(self, obj):
#         return {
#             "village": obj.village,
#             "city": obj.city,
#             "state": obj.state,
#             "pincode": obj.pincode,
#         }

#     # --------------------------------------------------
#     # HASHED ID
#     # --------------------------------------------------
#     # def get_id(self, obj):
#     #     return str(obj.uuid)

#     # --------------------------------------------------
#     # MULTIPLE PROPERTY IMAGES
#     # --------------------------------------------------
#     def get_images(self, obj):
#         request = self.context.get("request")

#         images = []

#         for img in obj.images.all():
#             if img.image:
#                 url = img.image.url
#                 if request:
#                     url = request.build_absolute_uri(url)
#                 images.append(url)

#         return images

#     # --------------------------------------------------
#     # PURPOSE
#     # --------------------------------------------------
#     def get_purpose(self, obj):
#         return obj.purpose.name if obj.purpose else None

#     # --------------------------------------------------
#     # CATEGORY WITH IMAGE
#     # --------------------------------------------------
#     def get_category(self, obj):
#         request = self.context.get("request")

#         if not obj.category:
#             return None

#         image_url = None
#         if getattr(obj.category, "image", None):
#             image_url = obj.category.image.url
#             if request:
#                 image_url = request.build_absolute_uri(image_url)

#         return {
#             "id": obj.category.id,
#             "name": obj.category.name,
#             "image": image_url,
#         }

#     # --------------------------------------------------
#     # SUBCATEGORY + FIELD ICONS
#     # --------------------------------------------------
#     # def get_subcategory(self, obj):
#     #     request = self.context.get("request")

#     #     if not obj.subcategory:
#     #         return None

#     #     fields = []

#     #     for field in obj.subcategory.fields.all():
#     #         icon_url = None
#     #         if field.icon:
#     #             icon_url = field.icon.url
#     #             if request:
#     #                 icon_url = request.build_absolute_uri(icon_url)

#     #         fields.append({
#     #             "id": field.id,
#     #             "field_name": field.field_name,
#     #             "field_type": field.field_type,
#     #             "required": field.required,
#     #             "icon": icon_url,
#     #         })

#     #     return {
#     #         "id": obj.subcategory.id,
#     #         "name": obj.subcategory.name,
#     #         "fields": fields,
#     #     }

#     # --------------------------------------------------
#     # PROPERTY FEATURES
#     # --------------------------------------------------
#     # def get_property_features(self, obj):
#     #     """
#     #     Return subcategory field definitions
#     #     + property dynamic field values
#     #     """

#     #     if not obj.subcategory:
#     #         return []

#     #     request = self.context.get("request")
#     #     dynamic_data = obj.dynamic_fields or {}
        

#     #     features = []

#     #     for field in obj.subcategory.fields.all():
#     #         raw_value = dynamic_data.get(field.field_name)

#     #         icon_url = None
#     #         if field.icon:
#     #             icon_url = field.icon.url
#     #             if request:
#     #                 icon_url = request.build_absolute_uri(icon_url)

#     #         features.append({
#     #             # "id": field.id,
#     #             "field_name": field.field_name,
#     #             # "field_type": field.field_type,
#     #             # "required": field.required,
#     #             "icon": icon_url,
#     #             "value": raw_value.get("value") if isinstance(raw_value, dict) else raw_value
#     #         })

#     #     return features


#     def get_property_features(self, obj):

#         if not obj.subcategory:
#             return []

#         request = self.context.get("request")
#         dynamic_data = obj.dynamic_fields or {}

#         features = []

#         fields_qs = getattr(obj.subcategory, "fields", None)   # ✅ FIX

#         if not fields_qs:   # ✅ FIX
#             return []

#         for field in fields_qs.all():   # ✅ FIX
#             raw_value = dynamic_data.get(field.field_name)

#             icon_url = None
#             if field.icon:
#                 icon_url = field.icon.url
#                 if request:
#                     icon_url = request.build_absolute_uri(icon_url)

#             features.append({
#                 "field_name": field.field_name,
#                 "icon": icon_url,
#                 "value": raw_value.get("value") if isinstance(raw_value, dict) else raw_value
#             })

#         return features

#     # --------------------------------------------------
#     # ✅ KEY SELLING POINTS (LIST)
#     # --------------------------------------------------
#     def get_key_selling_points(self, obj):
#         return obj.key_selling_points or []

#     # --------------------------------------------------
#     # ✅ LANDMARKS (LIST)
#     # --------------------------------------------------
#     def get_land_mark(self, obj):
#         return obj.land_mark or []

#     # --------------------------------------------------
#     # PRICE DETAILS
#     # --------------------------------------------------
#     def get_price_details(self, obj):
#         return {
#             "price": obj.price,
#             "sq_ft": obj.sq_ft,
#             "land_area": obj.land_area,
#             "perprice": obj.perprice,
#         }

#     # --------------------------------------------------
#     # CONTACT DETAILS
#     # --------------------------------------------------
#     def get_contact_details(self, obj):
#         return {
#             "owner": getattr(obj.owner, "name", str(obj.owner)),
#             "whatsapp": obj.whatsapp,
#             "phone": obj.phone,
#         }

#     # --------------------------------------------------
#     # AMENITIES
#     # --------------------------------------------------
#     # def get_amenities(self, obj):
#     #     request = self.context.get("request")

#     #     amenities_data = []

#     #     for amenity in obj.amenities.all():
#     #         icon_url = None

#     #         if amenity.icon:
#     #             icon_url = amenity.icon.url
#     #             if request:
#     #                 icon_url = request.build_absolute_uri(icon_url)

#     #         amenities_data.append({
#     #             "name": amenity.name,
#     #             "icon": icon_url
#     #         })
#     #     return amenities_data
#     def get_amenities(self, obj):
#         request = self.context.get("request")

#         amenities_data = []

#         amenities = obj.amenities.all()

#         if not amenities.exists():
#             return []

#         for amenity in amenities:
#             icon_url = None

#             try:
#                 if getattr(amenity, "icon", None):
#                     icon_url = amenity.icon.url

#                     if request:
#                         icon_url = request.build_absolute_uri(
#                             icon_url
#                         )
#             except Exception:
#                 icon_url = None

#             amenities_data.append({
#                 # "id": amenity.id,
#                 "name": amenity.name,
#                 "icon": icon_url
#             })

#         return amenities_data


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

            # ✅ UPDATED
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
    
    
class RecentEnquirySerializer(serializers.ModelSerializer):
    property_name = serializers.CharField(source="property.label", read_only=True)
    agent_name = serializers.SerializerMethodField()
    date = serializers.SerializerMethodField()

    class Meta:
        model = PropertyEnquiry
        fields = ["id", "property_name", "agent_name", "date"]

    # ✅ Get agent name from Property -> owner
    def get_agent_name(self, obj):
        if obj.property and obj.property.owner:
            return getattr(obj.property.owner, "name", None)
        return None

    # ✅ Format date
    def get_date(self, obj):
        if not obj.created_at:
            return None
        return obj.created_at.strftime("%B %d, %Y %I:%M %p")



# from rest_framework import serializers
# # from .models import Property, AgentProperty
# from .utils import hashids, encode_id


# class CombinedPropertyListSerializer(serializers.Serializer):
#     id = serializers.SerializerMethodField()
#     property_type = serializers.SerializerMethodField()

#     label = serializers.SerializerMethodField()
#     city = serializers.SerializerMethodField()
#     perprice = serializers.SerializerMethodField()
#     price = serializers.SerializerMethodField()
#     sq_ft = serializers.SerializerMethodField()
#     land_area = serializers.SerializerMethodField()

#     owner = serializers.SerializerMethodField()

#     whatsapp = serializers.SerializerMethodField()
#     phone = serializers.SerializerMethodField()

#     location = serializers.SerializerMethodField()

#     images = serializers.SerializerMethodField()

#     is_wishlisted = serializers.SerializerMethodField()


#     # -----------------------
#     # HASHED ID
#     # -----------------------
#     def get_id(self, obj):
#         return str(obj.uuid)


#     def get_property_type(self,obj):
#         if isinstance(obj, Property):
#             return "user"
#         return "agent"


#     def get_label(self,obj):
#         return obj.label


#     def get_city(self,obj):
#         return obj.city


#     def get_perprice(self,obj):
#         return obj.perprice


#     def get_price(self,obj):
#         return obj.price


#     def get_sq_ft(self,obj):
#         return str(obj.sq_ft) if obj.sq_ft else None


#     def get_land_area(self,obj):
#         return obj.land_area


#     def get_owner(self,obj):
#         if isinstance(obj, Property):
#             return obj.owner.name if obj.owner else None

#         return (
#             obj.owner or
#             obj.agent.name
#         )


#     def get_whatsapp(self,obj):
#         return obj.whatsapp


#     def get_phone(self,obj):
#         return obj.phone


#     def get_location(self,obj):
#         return obj.location


#     # -----------------------
#     # IMAGES
#     # -----------------------
#     def get_images(self,obj):

#         request=self.context.get("request")

#         urls=[]

#         if hasattr(obj,"images"):
#             for img in obj.images.all()[:2]:
#                 if img.image:
#                     url=img.image.url

#                     if request:
#                         url=request.build_absolute_uri(url)

#                     urls.append(url)

#         elif getattr(obj,"image",None):
#             url=obj.image.url
#             if request:
#                 url=request.build_absolute_uri(url)

#             urls.append(url)

#         return urls


#     def get_is_wishlisted(self,obj):

#         if isinstance(obj,AgentProperty):
#             return False

#         wishlist_ids=self.context.get(
#             "wishlist_ids",
#             set()
#         )

#         return obj.id in wishlist_ids


from rest_framework import serializers
# from .models import Property
# from agent.models import AgentProperty


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

        # USER PROPERTY
        if isinstance(obj, Property):
            return obj.owner if obj.owner else None

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


    # def get_is_wishlisted(self,obj):

    #     if isinstance(
    #         obj,
    #         AgentProperty
    #     ):
    #         return False


    #     wishlist_ids=self.context.get(
    #         "wishlist_ids",
    #         set()
    #     )

    #     return obj.id in wishlist_ids

    def get_is_wishlisted(self, obj):

        wishlist_ids = self.context.get(
            "wishlist_ids",
            set()
        )

        # compare UUIDs now
        return str(obj.id) in wishlist_ids
    

# class PropertySerializer(serializers.ModelSerializer):

#     class Meta:
#         model = Property
#         fields = "__all__"

#     def update(self, instance, validated_data):
#         amenities_list = self.context.get("amenities_list")
#         selling_points = self.context.get("selling_points_list")
#         landmarks = self.context.get("landmarks_list")

#         instance = super().update(instance, validated_data)

#         if amenities_list is not None:
#             instance.amenities.set(amenities_list)

#         if selling_points is not None:
#             instance.key_selling_points = selling_points

#         if landmarks is not None:
#             instance.land_mark = landmarks

#         instance.save()

#         return instance

# =========================================
# SERIALIZER
# =========================================

# class UserPropertySerializer(serializers.ModelSerializer):

#     # =========================================
#     # UUID
#     # =========================================

#     id = serializers.UUIDField(
#         read_only=True
#     )

#     # =========================================
#     # CUSTOM FIELDS
#     # =========================================

#     amenities = serializers.SerializerMethodField()

#     image = serializers.SerializerMethodField()

#     category_name = serializers.CharField(
#         source="category.name",
#         read_only=True
#     )

#     subcategory_name = serializers.CharField(
#         source="subcategory.name",
#         read_only=True
#     )

#     purpose_name = serializers.CharField(
#         source="purpose.name",
#         read_only=True
#     )

#     # =========================================
#     # FK INPUTS
#     # =========================================

#     category = serializers.PrimaryKeyRelatedField(
#         queryset=Category.objects.all()
#     )

#     subcategory = serializers.CharField(
#         required=False,
#         allow_blank=True,
#         allow_null=True
#     )

#     purpose = serializers.CharField(
#         required=False,
#         allow_blank=True,
#         allow_null=True
#     )

#     class Meta:

#         model = Property

#         fields = "__all__"

#         read_only_fields = [
#             "id",
#             "owner",
#             "property_code",
#             "created_at",
#             "updated_at",
#             "expiry_date",
#             "duration_days"
#         ]

#     # =========================================
#     # HANDLE FK
#     # =========================================

#     def handle_foreign_keys(self, validated_data):

#         # =====================================
#         # SUBCATEGORY
#         # =====================================

#         subcategory_name = self.initial_data.get(
#             "subcategory"
#         )

#         if subcategory_name:

#             subcategory = Subcategory.objects.filter(
#                 name__iexact=str(
#                     subcategory_name
#                 ).strip()
#             ).first()

#             if not subcategory:

#                 raise serializers.ValidationError({
#                     "subcategory":
#                     "Invalid subcategory"
#                 })

#             validated_data["subcategory"] = (
#                 subcategory
#             )

#         # =====================================
#         # PURPOSE
#         # =====================================

#         purpose_name = self.initial_data.get(
#             "purpose"
#         )

#         if purpose_name:

#             purpose = Purpose.objects.filter(
#                 name__iexact=str(
#                     purpose_name
#                 ).strip()
#             ).first()

#             if not purpose:

#                 raise serializers.ValidationError({
#                     "purpose":
#                     "Invalid purpose"
#                 })

#             validated_data["purpose"] = (
#                 purpose
#             )

#         return validated_data

#     # =========================================
#     # VALIDATION
#     # =========================================

#     def validate(self, attrs):

#         purpose_obj = None

#         # =====================================
#         # PURPOSE
#         # =====================================

#         if "purpose" in attrs:

#             purpose_value = attrs.get(
#                 "purpose"
#             )

#             if isinstance(
#                 purpose_value,
#                 str
#             ):

#                 purpose_obj = Purpose.objects.filter(
#                     name__iexact=purpose_value.strip()
#                 ).first()

#             else:

#                 purpose_obj = purpose_value

#         elif self.instance:

#             purpose_obj = self.instance.purpose

#         if not purpose_obj:

#             return attrs

#         purpose_name = str(
#             purpose_obj.name
#         ).lower().strip()

#         price = attrs.get(
#             "price",
#             getattr(
#                 self.instance,
#                 "price",
#                 None
#             )
#         )

#         perprice = attrs.get(
#             "perprice",
#             getattr(
#                 self.instance,
#                 "perprice",
#                 None
#             )
#         )

#         deposit = attrs.get(
#             "deposit",
#             getattr(
#                 self.instance,
#                 "deposit",
#                 None
#             )
#         )

#         # =====================================
#         # SALE
#         # =====================================

#         if purpose_name == "sale":

#             if not price:

#                 raise serializers.ValidationError({
#                     "price":
#                     "Price is required for sale"
#                 })

#             if not perprice:

#                 raise serializers.ValidationError({
#                     "perprice":
#                     "Per price is required"
#                 })

#             attrs["deposit"] = None

#         # =====================================
#         # RENT
#         # =====================================

#         elif purpose_name == "rent":

#             if not price:

#                 raise serializers.ValidationError({
#                     "price":
#                     "Rent amount is required"
#                 })

#             if not deposit:

#                 raise serializers.ValidationError({
#                     "deposit":
#                     "Deposit is required"
#                 })

#             attrs["perprice"] = None

#         # =====================================
#         # LEASE
#         # =====================================

#         elif purpose_name == "lease":

#             if not price:

#                 raise serializers.ValidationError({
#                     "price":
#                     "Price is required"
#                 })

#             attrs["deposit"] = None
#             attrs["perprice"] = None

#         return attrs

#     # =========================================
#     # CREATE
#     # =========================================

#     def create(self, validated_data):

#         request = self.context["request"]

#         user = request.user

#         validated_data = self.handle_foreign_keys(
#             validated_data
#         )

#         # =====================================
#         # AUTO PHONE
#         # =====================================

#         if not validated_data.get("phone"):

#             validated_data["phone"] = (
#                 user.mobile
#             )

#         if not validated_data.get("whatsapp"):

#             validated_data["whatsapp"] = (
#                 user.mobile
#             )

#         property_obj = Property.objects.create(
#             owner=user,
#             **validated_data
#         )

#         # =====================================
#         # AMENITIES
#         # =====================================

#         amenities = self.context.get(
#             "amenities_list",
#             []
#         )

#         if amenities:

#             property_obj.amenities.set(
#                 amenities
#             )

#         return property_obj

#     # =========================================
#     # UPDATE
#     # =========================================

#     def update(
#         self,
#         instance,
#         validated_data
#     ):

#         validated_data = self.handle_foreign_keys(
#             validated_data
#         )

#         amenities = self.context.get(
#             "amenities_list",
#             []
#         )

#         instance = super().update(
#             instance,
#             validated_data
#         )

#         if amenities:

#             instance.amenities.set(
#                 amenities
#             )

#         return instance

#     # =========================================
#     # RESPONSE
#     # =========================================

#     def to_representation(
#         self,
#         instance
#     ):

#         data = super().to_representation(
#             instance
#         )

#         data["id"] = str(instance.id)

#         purpose = (
#             instance.purpose.name.lower().strip()
#             if instance.purpose else ""
#         )

#         # =====================================
#         # RENT
#         # =====================================

#         if purpose == "rent":

#             data.pop(
#                 "perprice",
#                 None
#             )

#         # =====================================
#         # SALE
#         # =====================================

#         elif purpose == "sale":

#             data.pop(
#                 "deposit",
#                 None
#             )

#         # =====================================
#         # LEASE
#         # =====================================

#         elif purpose == "lease":

#             data.pop(
#                 "deposit",
#                 None
#             )

#             data.pop(
#                 "perprice",
#                 None
#             )

#         return data

#     # =========================================
#     # IMAGE
#     # =========================================

#     def get_image(self, obj):

#         if not obj.image:
#             return None

#         request = self.context.get(
#             "request"
#         )

#         try:

#             url = obj.image.url

#             if request:

#                 return request.build_absolute_uri(
#                     url
#                 )

#             return url

#         except:
#             return None

#     # =========================================
#     # AMENITIES
#     # =========================================

#     def get_amenities(self, obj):

#         return [
#             {
#                 "id": str(a.id),
#                 "name": a.name
#             }
#             for a in obj.amenities.all()
#         ]

# class UserPropertySerializer(serializers.ModelSerializer):

#     # =====================================================
#     # UUID
#     # =====================================================

#     id = serializers.UUIDField(
#         read_only=True
#     )

#     # =====================================================
#     # FILE FIELDS
#     # =====================================================

#     image = serializers.ImageField(
#         required=False,
#         allow_null=True
#     )

#     screenshot = serializers.ImageField(
#         required=False,
#         allow_null=True
#     )

#     # =====================================================
#     # RESPONSE FIELDS
#     # =====================================================

#     category_name = serializers.CharField(
#         source="category.name",
#         read_only=True
#     )

#     subcategory_name = serializers.CharField(
#         source="subcategory.name",
#         read_only=True
#     )

#     purpose_name = serializers.CharField(
#         source="purpose.name",
#         read_only=True
#     )

#     owner_id = serializers.SerializerMethodField()
#     owner_name = serializers.SerializerMethodField()
#     owner_email = serializers.SerializerMethodField()

#     amenities = serializers.SerializerMethodField()

#     # =====================================================
#     # INPUT FIELDS
#     # =====================================================

#     category = serializers.IntegerField(
#         write_only=True
#     )

#     subcategory = serializers.CharField(
#         required=False,
#         allow_blank=True,
#         allow_null=True
#     )

#     purpose = serializers.CharField(
#         required=False,
#         allow_blank=True,
#         allow_null=True
#     )

#     class Meta:

#         model = Property

#         fields = "__all__"

#         read_only_fields = [
#             "id",
#             "owner",
#             "property_code",
#             "created_at",
#             "updated_at",
#             "duration_days",
#             "expiry_date",
#         ]

#     # =====================================================
#     # CATEGORY VALIDATION
#     # =====================================================

#     def validate_category(self, value):

#         category = Category.objects.filter(
#             id=value
#         ).first()

#         if not category:

#             raise serializers.ValidationError(
#                 "Invalid category id"
#             )

#         return value

#     # =====================================================
#     # HANDLE FOREIGN KEYS
#     # =====================================================

#     def handle_foreign_keys(self, validated_data):

#         # CATEGORY

#         category_id = validated_data.pop(
#             "category",
#             None
#         )

#         if category_id:

#             category = Category.objects.filter(
#                 id=category_id
#             ).first()

#             if not category:

#                 raise serializers.ValidationError({
#                     "category":
#                     "Invalid category"
#                 })

#             validated_data["category"] = category

#         # SUBCATEGORY

#         validated_data.pop(
#             "subcategory",
#             None
#         )

#         subcategory_name = self.initial_data.get(
#             "subcategory"
#         )

#         if subcategory_name:

#             subcategory = Subcategory.objects.filter(
#                 name__iexact=str(
#                     subcategory_name
#                 ).strip()
#             ).first()

#             if not subcategory:

#                 raise serializers.ValidationError({
#                     "subcategory":
#                     "Invalid subcategory"
#                 })

#             validated_data["subcategory"] = (
#                 subcategory
#             )

#         # PURPOSE

#         validated_data.pop(
#             "purpose",
#             None
#         )

#         purpose_name = self.initial_data.get(
#             "purpose"
#         )

#         if purpose_name:

#             purpose = Purpose.objects.filter(
#                 name__iexact=str(
#                     purpose_name
#                 ).strip()
#             ).first()

#             if not purpose:

#                 raise serializers.ValidationError({
#                     "purpose":
#                     "Invalid purpose"
#                 })

#             validated_data["purpose"] = purpose

#         return validated_data

#     # =====================================================
#     # VALIDATE
#     # =====================================================

#     def validate(self, attrs):

#         purpose_name = str(
#             self.initial_data.get(
#                 "purpose",
#                 ""
#             )
#         ).lower().strip()

#         price = attrs.get(
#             "price",
#             getattr(self.instance, "price", None)
#         )

#         perprice = attrs.get(
#             "perprice",
#             getattr(self.instance, "perprice", None)
#         )

#         deposit = attrs.get(
#             "deposit",
#             getattr(self.instance, "deposit", None)
#         )

#         # SALE

#         if purpose_name == "sale":

#             if not price:

#                 raise serializers.ValidationError({
#                     "price":
#                     "Price required for sale"
#                 })

#             if not perprice:

#                 raise serializers.ValidationError({
#                     "perprice":
#                     "Perprice required"
#                 })

#             attrs["deposit"] = None

#         # RENT

#         elif purpose_name == "rent":

#             if not price:

#                 raise serializers.ValidationError({
#                     "price":
#                     "Rent amount required"
#                 })

#             if not deposit:

#                 raise serializers.ValidationError({
#                     "deposit":
#                     "Deposit required"
#                 })

#             attrs["perprice"] = None

#         # LEASE

#         elif purpose_name == "lease":

#             if not price:

#                 raise serializers.ValidationError({
#                     "price":
#                     "Price required"
#                 })

#             attrs["deposit"] = None
#             attrs["perprice"] = None

#         return attrs

#     # =====================================================
#     # CREATE
#     # =====================================================

#     def create(self, validated_data):

#         request = self.context["request"]

#         user = request.user

#         validated_data = self.handle_foreign_keys(
#             validated_data
#         )

#         # AUTO PHONE

#         if not validated_data.get("phone"):

#             validated_data["phone"] = (
#                 user.mobile
#             )

#         if not validated_data.get("whatsapp"):

#             validated_data["whatsapp"] = (
#                 user.mobile
#             )

#         # JSON FIELDS

#         key_selling_points = self.initial_data.get(
#             "key_selling_points"
#         )

#         if key_selling_points:

#             if isinstance(
#                 key_selling_points,
#                 str
#             ):

#                 try:

#                     key_selling_points = json.loads(
#                         key_selling_points
#                     )

#                 except:

#                     key_selling_points = []

#             validated_data[
#                 "key_selling_points"
#             ] = key_selling_points

#         land_mark = self.initial_data.get(
#             "land_mark"
#         )

#         if land_mark:

#             if isinstance(
#                 land_mark,
#                 str
#             ):

#                 try:

#                     land_mark = json.loads(
#                         land_mark
#                     )

#                 except:

#                     land_mark = []

#             validated_data["land_mark"] = (
#                 land_mark
#             )

#         dynamic_fields = self.initial_data.get(
#             "dynamic_fields"
#         )

#         if dynamic_fields:

#             if isinstance(
#                 dynamic_fields,
#                 str
#             ):

#                 try:

#                     dynamic_fields = json.loads(
#                         dynamic_fields
#                     )

#                 except:

#                     dynamic_fields = {}

#             validated_data[
#                 "dynamic_fields"
#             ] = dynamic_fields

#         # =================================================
#         # FILES
#         # =================================================

#         image = request.FILES.get("image")

#         screenshot = request.FILES.get(
#             "screenshot"
#         )

#         if image:

#             validated_data["image"] = image

#         if screenshot:

#             validated_data["screenshot"] = screenshot

#         # =================================================
#         # CREATE PROPERTY
#         # =================================================

#         property_obj = Property.objects.create(
#             owner=user,
#             **validated_data
#         )

#         # =================================================
#         # AMENITIES
#         # =================================================

#         amenities = self.context.get(
#             "amenities_list",
#             []
#         )

#         if amenities:

#             amenity_objects = Amenities.objects.filter(
#                 id__in=amenities
#             )

#             property_obj.amenities.set(
#                 amenity_objects
#             )

#         return property_obj

#     # =====================================================
#     # RESPONSE
#     # =====================================================

#     def to_representation(self, instance):

#         data = super().to_representation(
#             instance
#         )

#         data["id"] = str(instance.id)

#         data["category_id"] = (
#             instance.category.id
#             if instance.category else None
#         )

#         data["subcategory_id"] = (
#             instance.subcategory.id
#             if instance.subcategory else None
#         )

#         data["purpose_id"] = (
#             instance.purpose.id
#             if instance.purpose else None
#         )

#         data["package_id"] = (
#             str(instance.package.id)
#             if instance.package else None
#         )

#         # IMAGE URL

#         data["image"] = (
#             instance.image.url
#             if instance.image else None
#         )

#         data["screenshot"] = (
#             instance.screenshot.url
#             if instance.screenshot else None
#         )

#         purpose = (
#             instance.purpose.name.lower().strip()
#             if instance.purpose else ""
#         )

#         if purpose == "rent":

#             data.pop("perprice", None)

#         elif purpose == "sale":

#             data.pop("deposit", None)

#         elif purpose == "lease":

#             data.pop("deposit", None)
#             data.pop("perprice", None)

#         return data

#     # =====================================================
#     # OWNER DETAILS
#     # =====================================================

#     def get_owner_id(self, obj):

#         if obj.owner:
#             return str(obj.owner.id)

#         return None

#     def get_owner_name(self, obj):

#         if obj.owner:
#             return obj.owner.name

#         return None

#     def get_owner_email(self, obj):

#         if obj.owner:
#             return obj.owner.email

#         return None

#     # =====================================================
#     # AMENITIES
#     # =====================================================

#     def get_amenities(self, obj):

#         return [
#             {
#                 "id": a.id,
#                 "name": a.name
#             }
#             for a in obj.amenities.all()
#         ]

# from rest_framework import serializers
# import json

# from developer.models import (
#     Property,
#     Category,
#     Subcategory,
#     Purpose,
#     Amenities,
#     PropertyFeature,
#     SubcategoryField,
#     FieldOption,
# )


# class UserPropertySerializer(serializers.ModelSerializer):

#     # =====================================================
#     # BASIC
#     # =====================================================

#     id = serializers.UUIDField(read_only=True)

#     owner = serializers.PrimaryKeyRelatedField(
#         read_only=True
#     )

#     # =====================================================
#     # FOREIGN KEYS
#     # =====================================================

#     category = serializers.PrimaryKeyRelatedField(
#         queryset=Category.objects.all()
#     )

#     subcategory = serializers.SlugRelatedField(
#         slug_field="name",
#         queryset=Subcategory.objects.all()
#     )

#     purpose = serializers.SlugRelatedField(
#         slug_field="name",
#         queryset=Purpose.objects.all()
#     )

#     # =====================================================
#     # CUSTOM RESPONSE FIELDS
#     # =====================================================

#     amenities = serializers.SerializerMethodField()

#     images = serializers.SerializerMethodField()

#     image = serializers.SerializerMethodField()

#     features = serializers.SerializerMethodField()

#     # =====================================================
#     # JSON FIELDS
#     # =====================================================

#     selling_points = serializers.JSONField(
#         required=False
#     )

#     land_mark = serializers.JSONField(
#         required=False
#     )

#     # =====================================================
#     # META
#     # =====================================================

#     class Meta:

#         model = Property

#         fields = [

#             "id",
#             "owner",

#             "category",
#             "subcategory",
#             "purpose",

#             "label",
#             "land_area",
#             "sq_ft",
#             "description",

#             "amenities",

#             "image",
#             "images",
#             "screenshot",

#             "perprice",
#             "price",
#             "deposit",

#             "phone",
#             "whatsapp",

#             "location",
#             "city",
#             "district",
#             "taluk",
#             "village",
#             "state",
#             "pincode",

#             "land_mark",
#             "selling_points",

#             "paid",
#             "added_by",
#             "market_staff",
#             "message",
#             "note",

#             "features",

#             "created_at",
#             "updated_at",
#             "duration_days",
#             "expiry_date",
#         ]

#         read_only_fields = [
#             "id",
#             "owner",
#             "created_at",
#             "updated_at",
#             "duration_days",
#             "expiry_date",
#         ]

#     # =====================================================
#     # VALIDATION
#     # =====================================================

#     def validate(self, attrs):

#         purpose_obj = attrs.get("purpose")

#         if not purpose_obj:
#             return attrs

#         purpose_name = purpose_obj.name.lower().strip()

#         price = attrs.get("price")

#         perprice = attrs.get("perprice")

#         deposit = attrs.get("deposit")

#         # =================================================
#         # SALE
#         # =================================================

#         if purpose_name == "sale":

#             if not price:
#                 raise serializers.ValidationError({
#                     "price": "Price is required for sale"
#                 })

#             if not perprice:
#                 raise serializers.ValidationError({
#                     "perprice": "Per price is required for sale"
#                 })

#             attrs["deposit"] = None

#         # =================================================
#         # RENT
#         # =================================================

#         elif purpose_name == "rent":

#             if not price:
#                 raise serializers.ValidationError({
#                     "price": "Rent amount is required"
#                 })

#             if not deposit:
#                 raise serializers.ValidationError({
#                     "deposit": "Deposit is required for rent"
#                 })

#             attrs["perprice"] = None

#         # =================================================
#         # LEASE
#         # =================================================

#         elif purpose_name == "lease":

#             if not price:
#                 raise serializers.ValidationError({
#                     "price": "Price is required for lease"
#                 })

#             attrs["deposit"] = None
#             attrs["perprice"] = None

#         return attrs

#     # =====================================================
#     # CREATE
#     # =====================================================

#     def create(self, validated_data):

#         request = self.context.get("request")

#         if not request:
#             raise serializers.ValidationError(
#                 "Request missing"
#             )

#         # =========================================
#         # AMENITIES FIXED
#         # =========================================

#         amenities_ids = []

#         amenities_raw = request.data.get(
#             "amenities"
#         )

#         if amenities_raw:

#             try:

#                 # JSON ARRAY
#                 if (
#                     isinstance(amenities_raw, str)
#                     and amenities_raw.startswith("[")
#                 ):

#                     parsed = json.loads(
#                         amenities_raw
#                     )

#                     if isinstance(parsed, list):

#                         amenities_ids = [

#                             int(item)

#                             for item in parsed

#                             if str(item).isdigit()
#                         ]

#                 # COMMA SEPARATED
#                 else:

#                     amenities_ids = [

#                         int(item.strip())

#                         for item in str(
#                             amenities_raw
#                         ).split(",")

#                         if item.strip().isdigit()
#                     ]

#             except Exception:

#                 amenities_ids = []

#         else:

#             raw_list = request.data.getlist(
#                 "amenities"
#             )

#             cleaned_ids = []

#             for item in raw_list:

#                 try:

#                     if (
#                         isinstance(item, str)
#                         and item.startswith("[")
#                     ):

#                         parsed = json.loads(item)

#                         if isinstance(parsed, list):

#                             cleaned_ids.extend([

#                                 int(i)

#                                 for i in parsed

#                                 if str(i).isdigit()
#                             ])

#                     else:

#                         cleaned_ids.append(
#                             int(item)
#                         )

#                 except:
#                     pass

#             amenities_ids = cleaned_ids

#         amenities_ids = list(
#             set(amenities_ids)
#         )

#         # =========================================
#         # RAW JSON FIELDS
#         # =========================================

#         features_raw = request.data.get(
#             "features"
#         )

#         landmarks_raw = request.data.get(
#             "land_mark"
#         )

#         selling_points_raw = request.data.get(
#             "selling_points"
#         )

#         # =========================================
#         # FEATURES JSON PARSE
#         # =========================================

#         try:
#             features = json.loads(features_raw) \
#                 if features_raw else []

#         except Exception:
#             features = []

#         # =========================================
#         # LANDMARK JSON PARSE
#         # =========================================

#         try:
#             land_mark = json.loads(landmarks_raw) \
#                 if landmarks_raw else []

#         except Exception:
#             land_mark = []

#         # =========================================
#         # SELLING POINTS JSON PARSE
#         # =========================================

#         try:
#             selling_points = json.loads(
#                 selling_points_raw
#             ) if selling_points_raw else []

#         except Exception:
#             selling_points = []

#         # =========================================
#         # REMOVE DUPLICATE VALUES
#         # =========================================

#         validated_data.pop("land_mark", None)

#         validated_data.pop("selling_points", None)

#         # =========================================
#         # CREATE PROPERTY
#         # =========================================

#         property_obj = Property.objects.create(

#             owner=request.user,

#             land_mark=land_mark,

#             selling_points=selling_points,

#             **validated_data
#         )

#         # =========================================
#         # SAVE AMENITIES
#         # =========================================

#         if amenities_ids:

#             amenities = Amenities.objects.filter(
#                 id__in=amenities_ids
#             )

#             property_obj.amenities.set(
#                 amenities
#             )

#         # =========================================
#         # ADD FEATURES
#         # =========================================

#         for item in features:

#             field_id = item.get("field_id")

#             option_id = item.get("option_id")

#             value = item.get("value")

#             field = SubcategoryField.objects.filter(
#                 id=field_id
#             ).first()

#             if not field:
#                 continue

#             # OPTION BASED
#             if option_id:

#                 option = FieldOption.objects.filter(
#                     id=option_id,
#                     field=field
#                 ).first()

#                 if option:

#                     PropertyFeature.objects.create(

#                         property=property_obj,

#                         field=field,

#                         value=option.name
#                     )

#             # NORMAL VALUE
#             else:

#                 if value is not None:

#                     PropertyFeature.objects.create(

#                         property=property_obj,

#                         field=field,

#                         value=str(value)
#                     )

#         return property_obj

#     # =====================================================
#     # UPDATE
#     # =====================================================

#     def update(self, instance, validated_data):

#         request = self.context.get("request")

#         for attr, value in validated_data.items():
#             setattr(instance, attr, value)

#         instance.save()

#         # =========================================
#         # AMENITIES FIXED
#         # =========================================

#         amenities_ids = []

#         amenities_raw = request.data.get(
#             "amenities"
#         )

#         if amenities_raw:

#             try:

#                 if (
#                     isinstance(amenities_raw, str)
#                     and amenities_raw.startswith("[")
#                 ):

#                     parsed = json.loads(
#                         amenities_raw
#                     )

#                     if isinstance(parsed, list):

#                         amenities_ids = [

#                             int(item)

#                             for item in parsed

#                             if str(item).isdigit()
#                         ]

#                 else:

#                     amenities_ids = [

#                         int(item.strip())

#                         for item in str(
#                             amenities_raw
#                         ).split(",")

#                         if item.strip().isdigit()
#                     ]

#             except:
#                 amenities_ids = []

#         else:

#             raw_list = request.data.getlist(
#                 "amenities"
#             )

#             cleaned_ids = []

#             for item in raw_list:

#                 try:

#                     if (
#                         isinstance(item, str)
#                         and item.startswith("[")
#                     ):

#                         parsed = json.loads(item)

#                         if isinstance(parsed, list):

#                             cleaned_ids.extend([

#                                 int(i)

#                                 for i in parsed

#                                 if str(i).isdigit()
#                             ])

#                     else:

#                         cleaned_ids.append(
#                             int(item)
#                         )

#                 except:
#                     pass

#             amenities_ids = cleaned_ids

#         amenities_ids = list(
#             set(amenities_ids)
#         )

#         if amenities_ids:

#             amenities = Amenities.objects.filter(
#                 id__in=amenities_ids
#             )

#             instance.amenities.set(
#                 amenities
#             )

#         # =========================================
#         # FEATURES UPDATE
#         # =========================================

#         features_raw = request.data.get(
#             "features"
#         )

#         if features_raw:

#             try:
#                 features = json.loads(
#                     features_raw
#                 )

#             except:
#                 features = []

#             instance.property_features.all().delete()

#             for item in features:

#                 if not isinstance(item, dict):
#                     continue

#                 field_id = item.get("field_id")

#                 option_id = item.get("option_id")

#                 value = item.get("value")

#                 field = SubcategoryField.objects.filter(
#                     id=field_id
#                 ).first()

#                 if not field:
#                     continue

#                 if option_id:

#                     option = FieldOption.objects.filter(
#                         id=option_id,
#                         field=field
#                     ).first()

#                     if not option:
#                         continue

#                     PropertyFeature.objects.create(
#                         property=instance,
#                         field=field,
#                         value=option.name
#                     )

#                 else:

#                     PropertyFeature.objects.create(
#                         property=instance,
#                         field=field,
#                         value=str(value)
#                     )

#         return instance

#     # =====================================================
#     # RESPONSE FORMAT
#     # =====================================================

#     def to_representation(self, instance):

#         data = {

#             "id": str(instance.id),

#             "images": self.get_images(instance),

#             "image": self.get_image(instance),

#             "amenities": self.get_amenities(instance),

#             "selling_points": (
#                 instance.selling_points or []
#             ),

#             "landmarks": (
#                 instance.land_mark or []
#             ),

#             "features": self.get_features(instance),

#             "category": (
#                 instance.category.id
#                 if instance.category else None
#             ),

#             "subcategory": (
#                 instance.subcategory.name
#                 if instance.subcategory else None
#             ),

#             "purpose": (
#                 instance.purpose.name
#                 if instance.purpose else None
#             ),

#             "label": instance.label,

#             "land_area": instance.land_area,

#             "sq_ft": instance.sq_ft,

#             "description": instance.description,

#             "screenshot": (
#                 instance.screenshot.url
#                 if instance.screenshot else None
#             ),

#             "price": instance.price,

#             "deposit": instance.deposit,

#             "perprice": instance.perprice,

#             "whatsapp": instance.whatsapp,

#             "phone": instance.phone,

#             "location": instance.location,

#             "city": instance.city,

#             "pincode": instance.pincode,

#             "district": instance.district,

#             "land_mark": instance.land_mark,

#             "owner": (
#                 instance.owner.name
#                 if instance.owner else None
#             ),

#             "taluk": instance.taluk,

#             "village": instance.village,

#             "state": instance.state,

#             "paid": instance.paid,

#             "notes": instance.note,

#             "created_at": instance.created_at,

#             "updated_at": instance.updated_at,

#             "duration_days": instance.duration_days,

#             "expiry_date": instance.expiry_date,

#             "user": str(instance.owner.id),
#         }

#         # =========================================
#         # REMOVE BASED ON PURPOSE
#         # =========================================

#         purpose = (
#             instance.purpose.name.lower().strip()
#             if instance.purpose else ""
#         )

#         if purpose == "rent":
#             data.pop("perprice", None)

#         elif purpose == "sale":
#             data.pop("deposit", None)

#         elif purpose == "lease":
#             data.pop("deposit", None)
#             data.pop("perprice", None)

#         return data

#     # =====================================================
#     # AMENITIES
#     # =====================================================

#     def get_amenities(self, obj):

#         return [
#             {
#                 "id": a.id,
#                 "name": a.name,
#                 "icon": (
#                     a.icon.url
#                     if a.icon else None
#                 )
#             }

#             for a in obj.amenities.all()
#         ]

#     # =====================================================
#     # IMAGES
#     # =====================================================

#     def get_images(self, obj):

#         return [

#             img.image.url
#             if img.image else None

#             for img in obj.images.all()
#         ]

#     def get_image(self, obj):

#         return (
#             obj.image.url
#             if obj.image else None
#         )

#     # =====================================================
#     # FEATURES
#     # =====================================================

#     def get_features(self, obj):

#         result = []

#         for feature in obj.property_features.select_related(
#             "field"
#         ):

#             icon = (
#                 feature.field.icon.url
#                 if feature.field.icon else None
#             )

#             result.append({

#                 "name": (
#                     feature.field.field_name
#                 ),

#                 "value": feature.value,

#                 "icon": icon
#             })

#         return result

# from rest_framework import serializers
# import json

# from developer.models import (
#     Property,
#     Category,
#     Subcategory,
#     Purpose,
#     Amenities,
#     PropertyFeature,
#     SubcategoryField,
#     FieldOption,
#     PropertyImage
# )


# class UserPropertySerializer(serializers.ModelSerializer):

#     # =====================================================
#     # BASIC
#     # =====================================================

#     id = serializers.UUIDField(read_only=True)

#     owner = serializers.PrimaryKeyRelatedField(
#         read_only=True
#     )

#     # =====================================================
#     # FOREIGN KEYS
#     # =====================================================

#     category = serializers.PrimaryKeyRelatedField(
#         queryset=Category.objects.all()
#     )

#     subcategory = serializers.SlugRelatedField(
#         slug_field="name",
#         queryset=Subcategory.objects.all()
#     )

#     purpose = serializers.SlugRelatedField(
#         slug_field="name",
#         queryset=Purpose.objects.all()
#     )

#     # =====================================================
#     # CUSTOM FIELDS
#     # =====================================================

#     # amenities = serializers.SerializerMethodField()
#     amenities = serializers.PrimaryKeyRelatedField(
#         queryset=Amenities.objects.all(),
#         many=True,
#         write_only=True,
#         required=False
#     )

#     amenities_data = serializers.SerializerMethodField(
#         read_only=True
#     )

#     images = serializers.SerializerMethodField()

#     image = serializers.SerializerMethodField()

#     features = serializers.SerializerMethodField()

#     # =====================================================
#     # JSON FIELDS
#     # =====================================================

#     selling_points = serializers.JSONField(
#         required=False
#     )

#     land_mark = serializers.JSONField(
#         required=False
#     )

#     # =====================================================
#     # META
#     # =====================================================

#     class Meta:

#         model = Property

#         fields = "__all__"

#         read_only_fields = [
#             "id",
#             "owner",
#             "created_at",
#             "updated_at",
#             "duration_days",
#             "expiry_date",
#         ]

#         def get_field_names(self, declared_fields, info):

#             expanded_fields = super().get_field_names(
#                 declared_fields,
#                 info
#             )

#             expanded_fields.append(
#                 "amenities_data"
#             )

#             return expanded_fields

#     # =====================================================
#     # VALIDATION
#     # =====================================================

#     def validate(self, attrs):

#         purpose_obj = attrs.get(
#             "purpose",
#             getattr(self.instance, "purpose", None)
#         )

#         if not purpose_obj:
#             return attrs

#         purpose_name = purpose_obj.name.lower().strip()

#         price = attrs.get(
#             "price",
#             getattr(self.instance, "price", None)
#         )

#         perprice = attrs.get(
#             "perprice",
#             getattr(self.instance, "perprice", None)
#         )

#         deposit = attrs.get(
#             "deposit",
#             getattr(self.instance, "deposit", None)
#         )

#         # =========================================
#         # SALE
#         # =========================================

#         if purpose_name == "sale":

#             if not price:
#                 raise serializers.ValidationError({
#                     "price": "Price is required for sale"
#                 })

#             if not perprice:
#                 raise serializers.ValidationError({
#                     "perprice": "Per price is required for sale"
#                 })

#             attrs["deposit"] = None

#         # =========================================
#         # RENT
#         # =========================================

#         elif purpose_name == "rent":

#             if not price:
#                 raise serializers.ValidationError({
#                     "price": "Rent amount required"
#                 })

#             if not deposit:
#                 raise serializers.ValidationError({
#                     "deposit": "Deposit required"
#                 })

#             attrs["perprice"] = None

#         # =========================================
#         # LEASE
#         # =========================================

#         elif purpose_name == "lease":

#             if not price:
#                 raise serializers.ValidationError({
#                     "price": "Price required"
#                 })

#             attrs["deposit"] = None
#             attrs["perprice"] = None

#         return attrs

#     # =====================================================
#     # CREATE
#     # =====================================================

#     def create(self, validated_data):

#         request = self.context.get("request")

#         validated_data.pop("selling_points", None)
#         validated_data.pop("land_mark", None)

#         property_obj = Property.objects.create(
#             owner=request.user,
#             **validated_data
#         )

#         self.handle_related_fields(
#             property_obj
#         )

#         return property_obj

#     # =====================================================
#     # UPDATE
#     # =====================================================

#     def update(self, instance, validated_data):

#         validated_data.pop("selling_points", None)
#         validated_data.pop("land_mark", None)

#         for attr, value in validated_data.items():
#             setattr(instance, attr, value)

#         instance.save()

#         self.handle_related_fields(
#             instance
#         )

#         return instance

#     # =====================================================
#     # HANDLE RELATED FIELDS
#     # =====================================================

#     def handle_related_fields(self, instance):

#         request = self.context.get("request")

#         # # =========================================
#         # # AMENITIES
#         # # =========================================

#         # # =========================================
#         # # AMENITIES FULL FIX
#         # # =========================================

#         # amenities_ids = []

#         # # SINGLE VALUE
#         # amenities_raw = request.data.get(
#         #     "amenities"
#         # )

#         # # =========================================
#         # # JSON STRING
#         # # example: [1,2,3]
#         # # =========================================

#         # if amenities_raw:

#         #     try:

#         #         if (
#         #             isinstance(amenities_raw, str)
#         #             and amenities_raw.startswith("[")
#         #         ):

#         #             parsed = json.loads(
#         #                 amenities_raw
#         #             )

#         #             if isinstance(parsed, list):

#         #                 amenities_ids = [

#         #                     int(item)

#         #                     for item in parsed

#         #                     if str(item).isdigit()
#         #                 ]

#         #         # =================================
#         #         # COMMA SEPARATED
#         #         # example: 1,2,3
#         #         # =================================

#         #         else:

#         #             amenities_ids = [

#         #                 int(item.strip())

#         #                 for item in str(
#         #                     amenities_raw
#         #                 ).split(",")

#         #                 if item.strip().isdigit()
#         #             ]

#         #     except Exception:

#         #         amenities_ids = []

#         # # =========================================
#         # # MULTIPART ARRAY
#         # # amenities=1
#         # # amenities=2
#         # # =========================================

#         # else:

#         #     raw_list = request.data.getlist(
#         #         "amenities"
#         #     )

#         #     cleaned_ids = []

#         #     for item in raw_list:

#         #         try:

#         #             # JSON ARRAY STRING
#         #             if (
#         #                 isinstance(item, str)
#         #                 and item.startswith("[")
#         #             ):

#         #                 parsed = json.loads(item)

#         #                 if isinstance(parsed, list):

#         #                     cleaned_ids.extend([

#         #                         int(i)

#         #                         for i in parsed

#         #                         if str(i).isdigit()
#         #                     ])

#         #             # NORMAL VALUE
#         #             else:

#         #                 cleaned_ids.append(
#         #                     int(item)
#         #                 )

#         #         except:
#         #             pass

#         #     amenities_ids = cleaned_ids

#         # # REMOVE DUPLICATES
#         # amenities_ids = list(
#         #     set(amenities_ids)
#         # )

#         # # =========================================
#         # # SAVE AMENITIES
#         # # =========================================

#         # instance.amenities.clear()

#         # if amenities_ids:

#         #     amenities = Amenities.objects.filter(
#         #         id__in=amenities_ids
#         #     )

#         #     instance.amenities.set(
#         #         amenities
#         #     )

#         # =========================================
#         # SELLING POINTS
#         # =========================================

#         selling_points_raw = request.data.get(
#             "selling_points"
#         )

#         if selling_points_raw:

#             try:

#                 selling_points = json.loads(
#                     selling_points_raw
#                 )

#             except:
#                 selling_points = []

#             instance.selling_points = (
#                 selling_points
#             )

#         # =========================================
#         # LANDMARKS
#         # =========================================

#         land_mark_raw = request.data.get(
#             "land_mark"
#         )

#         if land_mark_raw:

#             try:

#                 land_mark = json.loads(
#                     land_mark_raw
#                 )

#             except:
#                 land_mark = []

#             instance.land_mark = land_mark

#         instance.save()

#         # =========================================
#         # FEATURES
#         # =========================================

#         features_raw = request.data.get(
#             "features"
#         )

#         if features_raw:

#             try:

#                 features = json.loads(
#                     features_raw
#                 )

#             except:
#                 features = []

#             # DELETE OLD FEATURES
#             instance.property_features.all().delete()

#             for item in features:

#                 if not isinstance(item, dict):
#                     continue

#                 field_id = item.get("field_id")

#                 option_id = item.get("option_id")

#                 value = item.get("value")

#                 field = SubcategoryField.objects.filter(
#                     id=field_id
#                 ).first()

#                 if not field:
#                     continue

#                 # OPTION
#                 if option_id:

#                     option = FieldOption.objects.filter(
#                         id=option_id,
#                         field=field
#                     ).first()

#                     if option:

#                         PropertyFeature.objects.create(
#                             property=instance,
#                             field=field,
#                             value=option.name
#                         )

#                 # NORMAL
#                 else:

#                     if value is not None:

#                         PropertyFeature.objects.create(
#                             property=instance,
#                             field=field,
#                             value=str(value)
#                         )

#         # =========================================
#         # MULTIPLE IMAGES
#         # =========================================

#         images = request.FILES.getlist(
#             "images"
#         )

#         if images:

#             # DELETE OLD
#             instance.images.all().delete()

#             for image in images:

#                 PropertyImage.objects.create(
#                     property=instance,
#                     image=image
#                 )

#         # =========================================
#         # MAIN IMAGE
#         # =========================================

#         main_image = request.FILES.get(
#             "image"
#         )

#         if main_image:

#             instance.image = main_image
#             instance.save()

#     # =====================================================
#     # AMENITIES
#     # =====================================================

#     def get_amenities(self, obj):

#         return [
#             {
#                 "id": a.id,
#                 "name": a.name,
#                 "icon": (
#                     a.icon.url
#                     if a.icon else None
#                 )
#             }
#             for a in obj.amenities.all()
#         ]

#     # =====================================================
#     # IMAGES
#     # =====================================================

#     def get_images(self, obj):

#         request = self.context.get("request")

#         urls = []

#         for img in obj.images.all():

#             if img.image:

#                 try:

#                     url = img.image.url

#                     if request:
#                         url = request.build_absolute_uri(url)

#                     urls.append(url)

#                 except:
#                     pass

#         return urls

#     def get_image(self, obj):

#         if not obj.image:
#             return None

#         request = self.context.get("request")

#         try:

#             url = obj.image.url

#             if request:
#                 return request.build_absolute_uri(url)

#             return url

#         except:
#             return None

#     # =====================================================
#     # FEATURES
#     # =====================================================

#     def get_features(self, obj):

#         result = []

#         for feature in obj.property_features.select_related(
#             "field"
#         ):

#             icon = (
#                 feature.field.icon.url
#                 if feature.field.icon else None
#             )

#             result.append({

#                 "name":
#                 feature.field.field_name,

#                 "value":
#                 feature.value,

#                 "icon":
#                 icon
#             })

#         return result



# from rest_framework import serializers
# import json

# from developer.models import (
#     Property,
#     Category,
#     Subcategory,
#     Purpose,
#     Amenities,
#     PropertyFeature,
#     SubcategoryField,
#     FieldOption,
#     PropertyImage
# )


# class UserPropertySerializer(serializers.ModelSerializer):

#     # =====================================================
#     # BASIC
#     # =====================================================

#     id = serializers.UUIDField(read_only=True)

#     owner = serializers.PrimaryKeyRelatedField(
#         read_only=True
#     )

#     # =====================================================
#     # FOREIGN KEYS
#     # =====================================================

#     category = serializers.PrimaryKeyRelatedField(
#         queryset=Category.objects.all()
#     )

#     subcategory = serializers.SlugRelatedField(
#         slug_field="name",
#         queryset=Subcategory.objects.all()
#     )

#     purpose = serializers.SlugRelatedField(
#         slug_field="name",
#         queryset=Purpose.objects.all()
#     )

#     # =====================================================
#     # AMENITIES FIX
#     # =====================================================

#     amenities = serializers.JSONField(
#         required=False,
#         write_only=True
#     )

#     amenities_data = serializers.SerializerMethodField()

#     # =====================================================
#     # CUSTOM FIELDS
#     # =====================================================

#     images = serializers.SerializerMethodField()

#     image = serializers.SerializerMethodField()

#     features = serializers.SerializerMethodField()

#     # =====================================================
#     # JSON FIELDS
#     # =====================================================

#     selling_points = serializers.JSONField(
#         required=False
#     )

#     land_mark = serializers.JSONField(
#         required=False
#     )

#     # =====================================================
#     # META
#     # =====================================================

#     class Meta:

#         model = Property

#         fields = "__all__"

#         read_only_fields = [
#             "id",
#             "owner",
#             "created_at",
#             "updated_at",
#             "duration_days",
#             "expiry_date",
#         ]

#     # =====================================================
#     # VALIDATION
#     # =====================================================

#     def validate(self, attrs):

#         purpose_obj = attrs.get(
#             "purpose",
#             getattr(self.instance, "purpose", None)
#         )

#         if not purpose_obj:
#             return attrs

#         purpose_name = purpose_obj.name.lower().strip()

#         price = attrs.get(
#             "price",
#             getattr(self.instance, "price", None)
#         )

#         perprice = attrs.get(
#             "perprice",
#             getattr(self.instance, "perprice", None)
#         )

#         deposit = attrs.get(
#             "deposit",
#             getattr(self.instance, "deposit", None)
#         )

#         # =========================================
#         # SALE
#         # =========================================

#         if purpose_name == "sale":

#             if not price:
#                 raise serializers.ValidationError({
#                     "price": "Price is required for sale"
#                 })

#             if not perprice:
#                 raise serializers.ValidationError({
#                     "perprice": "Per price is required for sale"
#                 })

#             attrs["deposit"] = None

#         # =========================================
#         # RENT
#         # =========================================

#         elif purpose_name == "rent":

#             if not price:
#                 raise serializers.ValidationError({
#                     "price": "Rent amount required"
#                 })

#             if not deposit:
#                 raise serializers.ValidationError({
#                     "deposit": "Deposit required"
#                 })

#             attrs["perprice"] = None

#         # =========================================
#         # LEASE
#         # =========================================

#         elif purpose_name == "lease":

#             if not price:
#                 raise serializers.ValidationError({
#                     "price": "Price required"
#                 })

#             attrs["deposit"] = None
#             attrs["perprice"] = None

#         return attrs

#     # =====================================================
#     # CREATE
#     # =====================================================

#     def create(self, validated_data):

#         request = self.context.get("request")

#         # =========================================
#         # AMENITIES FIX
#         # =========================================

#         amenities_data = validated_data.pop(
#             "amenities",
#             []
#         )

#         amenities_ids = []

#         if isinstance(amenities_data, str):

#             try:
#                 amenities_data = json.loads(
#                     amenities_data
#                 )
#             except:
#                 amenities_data = []

#         if isinstance(amenities_data, list):

#             for item in amenities_data:

#                 try:
#                     amenities_ids.append(
#                         int(item)
#                     )
#                 except:
#                     pass

#         validated_data.pop("selling_points", None)
#         validated_data.pop("land_mark", None)

#         property_obj = Property.objects.create(
#             owner=request.user,
#             **validated_data
#         )

#         # SAVE AMENITIES
#         if amenities_ids:

#             amenities = Amenities.objects.filter(
#                 id__in=amenities_ids
#             )

#             property_obj.amenities.set(
#                 amenities
#             )

#         self.handle_related_fields(
#             property_obj
#         )

#         return property_obj

#     # =====================================================
#     # UPDATE
#     # =====================================================

#     def update(self, instance, validated_data):

#         # =========================================
#         # AMENITIES FIX
#         # =========================================

#         amenities_data = validated_data.pop(
#             "amenities",
#             None
#         )

#         amenities_ids = []

#         if amenities_data is not None:

#             if isinstance(amenities_data, str):

#                 try:
#                     amenities_data = json.loads(
#                         amenities_data
#                     )
#                 except:
#                     amenities_data = []

#             if isinstance(amenities_data, list):

#                 for item in amenities_data:

#                     try:
#                         amenities_ids.append(
#                             int(item)
#                         )
#                     except:
#                         pass

#         validated_data.pop("selling_points", None)
#         validated_data.pop("land_mark", None)

#         for attr, value in validated_data.items():
#             setattr(instance, attr, value)

#         instance.save()

#         # UPDATE AMENITIES
#         if amenities_data is not None:

#             amenities = Amenities.objects.filter(
#                 id__in=amenities_ids
#             )

#             instance.amenities.set(
#                 amenities
#             )

#         self.handle_related_fields(
#             instance
#         )

#         return instance

#     # =====================================================
#     # HANDLE RELATED FIELDS
#     # =====================================================

#     def handle_related_fields(self, instance):

#         request = self.context.get("request")

#         # =========================================
#         # SELLING POINTS
#         # =========================================

#         selling_points_raw = request.data.get(
#             "selling_points"
#         )

#         if selling_points_raw:

#             try:

#                 selling_points = json.loads(
#                     selling_points_raw
#                 )

#             except:
#                 selling_points = []

#             instance.selling_points = (
#                 selling_points
#             )

#         # =========================================
#         # LANDMARKS
#         # =========================================

#         land_mark_raw = request.data.get(
#             "land_mark"
#         )

#         if land_mark_raw:

#             try:

#                 land_mark = json.loads(
#                     land_mark_raw
#                 )

#             except:
#                 land_mark = []

#             instance.land_mark = land_mark

#         instance.save()

#         # =========================================
#         # FEATURES
#         # =========================================

#         features_raw = request.data.get(
#             "features"
#         )

#         if features_raw:

#             try:

#                 features = json.loads(
#                     features_raw
#                 )

#             except:
#                 features = []

#             instance.property_features.all().delete()

#             for item in features:

#                 if not isinstance(item, dict):
#                     continue

#                 field_id = item.get("field_id")

#                 option_id = item.get("option_id")

#                 value = item.get("value")

#                 field = SubcategoryField.objects.filter(
#                     id=field_id
#                 ).first()

#                 if not field:
#                     continue

#                 # OPTION
#                 if option_id:

#                     option = FieldOption.objects.filter(
#                         id=option_id,
#                         field=field
#                     ).first()

#                     if option:

#                         PropertyFeature.objects.create(
#                             property=instance,
#                             field=field,
#                             value=option.name
#                         )

#                 # NORMAL
#                 else:

#                     if value is not None:

#                         PropertyFeature.objects.create(
#                             property=instance,
#                             field=field,
#                             value=str(value)
#                         )

#         # =========================================
#         # MULTIPLE IMAGES
#         # =========================================

#         images = request.FILES.getlist(
#             "images"
#         )

#         if images:

#             instance.images.all().delete()

#             for image in images:

#                 PropertyImage.objects.create(
#                     property=instance,
#                     image=image
#                 )

#         # =========================================
#         # MAIN IMAGE
#         # =========================================

#         main_image = request.FILES.get(
#             "image"
#         )

#         if main_image:

#             instance.image = main_image
#             instance.save()

#     # =====================================================
#     # AMENITIES RESPONSE
#     # =====================================================

#     def get_amenities_data(self, obj):

#         return [
#             {
#                 "id": a.id,
#                 "name": a.name,
#                 "icon": (
#                     a.icon.url
#                     if a.icon else None
#                 )
#             }
#             for a in obj.amenities.all()
#         ]

#     # =====================================================
#     # IMAGES
#     # =====================================================

#     def get_images(self, obj):

#         request = self.context.get("request")

#         urls = []

#         for img in obj.images.all():

#             if img.image:

#                 try:

#                     url = img.image.url

#                     if request:
#                         url = request.build_absolute_uri(url)

#                     urls.append(url)

#                 except:
#                     pass

#         return urls

#     def get_image(self, obj):

#         if not obj.image:
#             return None

#         request = self.context.get("request")

#         try:

#             url = obj.image.url

#             if request:
#                 return request.build_absolute_uri(url)

#             return url

#         except:
#             return None

#     # =====================================================
#     # FEATURES
#     # =====================================================

#     def get_features(self, obj):

#         result = []

#         for feature in obj.property_features.select_related(
#             "field"
#         ):

#             icon = (
#                 feature.field.icon.url
#                 if feature.field.icon else None
#             )

#             result.append({

#                 "name":
#                 feature.field.field_name,

#                 "value":
#                 feature.value,

#                 "icon":
#                 icon
#             })

#         return result

class UserPropertySerializer(serializers.ModelSerializer):

    id=serializers.UUIDField(
        read_only=True
    )

    images=serializers.SerializerMethodField()
    image=serializers.SerializerMethodField()
    amenities=serializers.SerializerMethodField()
    selling_points=serializers.SerializerMethodField()
    landmarks=serializers.SerializerMethodField()
    features=serializers.SerializerMethodField()

    # =====================================================
    # OWNER TEXT FIELD ONLY
    # =====================================================

    owner=serializers.CharField(
        required=False,
        allow_null=True,
        allow_blank=True
    )

    category=serializers.PrimaryKeyRelatedField(
        queryset=Category.objects.all()
    )

    subcategory=serializers.CharField(
        required=False,
        allow_null=True,
        allow_blank=True
    )

    purpose=serializers.CharField(
        required=False,
        allow_null=True,
        allow_blank=True
    )

    class Meta:

        model=Property

        fields="__all__"

        read_only_fields=[
            "user"
        ]

    # =====================================================
    # CREATE
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

    def create(self,validated_data):

        request=self.context.get("request")

        # =================================================
        # STORE LOGGED USER INTO USER FIELD
        # =================================================

        if request and request.user:

            validated_data["user"]=request.user

        # =================================================
        # OWNER TEXT FIELD
        # =================================================

        owner_name=self.initial_data.get("owner")

        if owner_name is not None:

            validated_data["owner"]=owner_name.strip()

        # =================================================
        # SUBCATEGORY
        # =================================================
        sub = self.initial_data.get("subcategory")
        sub_obj = self.get_subcategory_obj(sub)

        if sub_obj:
            validated_data["subcategory"] = sub_obj

        # ==============================
        # PURPOSE (TEXT → OBJECT)
        # ==============================
        pur = self.initial_data.get("purpose")
        pur_obj = self.get_purpose_obj(pur)

        if pur_obj:
            validated_data["purpose"] = pur_obj

        # sub=self.initial_data.get("subcategory")

        # if sub:

        #     sub_obj=Subcategory.objects.filter(
        #         name__iexact=sub.strip()
        #     ).first()

        #     if sub_obj:
        #         validated_data["subcategory"]=sub_obj

        # # =================================================
        # # PURPOSE
        # # =================================================

        # pur=self.initial_data.get("purpose")

        # if pur:

        #     pur_obj=Purpose.objects.filter(
        #         name__iexact=pur.strip()
        #     ).first()

        #     if pur_obj:
        #         validated_data["purpose"]=pur_obj

        instance=Property.objects.create(
            **validated_data
        )

        self.handle_related(instance)

        return instance

    # =====================================================
    # UPDATE
    # =====================================================

    def update(self,instance,validated_data):
        request = self.context.get("request")

        # =================================================
        # MULTIPLE IMAGES UPDATE
        # =================================================

        if request and "images" in request.FILES:

            images = request.FILES.getlist("images")

            if images:

                # OPTIONAL: remove old images (safe update behavior)
                instance.images.all().delete()

                PropertyImage.objects.bulk_create([
                    PropertyImage(
                        property=instance,
                        image=img
                    )
                    for img in images
                ])


        # =================================================
        # SINGLE IMAGE UPDATE
        # =================================================

        if request and request.FILES.get("image"):

            instance.image = request.FILES.get("image")
    

        # =================================================
        # OWNER TEXT UPDATE ONLY
        # =================================================

        owner_name=self.initial_data.get("owner")

        if owner_name is not None:

            instance.owner=owner_name.strip()

        # =================================================
        # SUBCATEGORY UPDATE
        # =================================================
        sub = self.initial_data.get("subcategory")
        sub_obj = self.get_subcategory_obj(sub)

        if sub_obj:
            instance.subcategory = sub_obj

        # REMOVE FROM validated_data (CRITICAL FIX)
        validated_data.pop("subcategory", None)

        # ==============================
        # PURPOSE (FIXED)
        # ==============================
        pur = self.initial_data.get("purpose")
        pur_obj = self.get_purpose_obj(pur)

        if pur_obj:
            instance.purpose = pur_obj

        # REMOVE FROM validated_data (CRITICAL FIX)
        validated_data.pop("purpose", None)


        # sub=self.initial_data.get("subcategory")

        # if sub:

        #     sub_obj=Subcategory.objects.filter(
        #         name__iexact=sub.strip()
        #     ).first()

        #     if sub_obj:
        #         instance.subcategory=sub_obj

        # # =================================================
        # # PURPOSE UPDATE
        # # =================================================

        # pur=self.initial_data.get("purpose")

        # if pur:

        #     pur_obj=Purpose.objects.filter(
        #         name__iexact=pur.strip()
        #     ).first()

        #     if pur_obj:
        #         instance.purpose=pur_obj

        # =================================================
        # OTHER FIELDS
        # =================================================

        for k,v in validated_data.items():

            if k in ["owner","user"]:
                continue

            setattr(instance,k,v)

        instance.save()

        self.handle_related(instance)

        return instance

    # =====================================================
    # RELATED
    # =====================================================

    # def handle_related(self,instance):

    #     amenities=self.context.get(
    #         "amenities_list"
    #     )

    #     if amenities is not None:

    #         amenity_objects=Amenities.objects.filter(
    #             id__in=amenities
    #         )

    #         instance.amenities.set(
    #             amenity_objects
    #         )

    #     sp=self.context.get(
    #         "selling_points_list"
    #     )

    #     if sp is not None:

    #         instance.selling_points=sp

    #         instance.save(
    #             update_fields=[
    #                 "selling_points"
    #             ]
    #         )

    #     lm=self.context.get(
    #         "land_mark_list"
    #     )

    #     if lm is not None:

    #         instance.land_mark=lm

    #         instance.save(
    #             update_fields=[
    #                 "land_mark"
    #             ]
    #         )

    #     fv_list=self.context.get(
    #         "features_list"
    #     )

    #     if fv_list is not None:

    #         PropertyFeature.objects.filter(
    #             property=instance
    #         ).delete()

    #         for fv in fv_list:

    #             if not isinstance(fv,dict):
    #                 continue

    #             field=SubcategoryField.objects.filter(
    #                 subcategory=instance.subcategory,
    #                 field_name__iexact=fv.get("name")
    #             ).first()

    #             if not field:
    #                 continue

    #             PropertyFeature.objects.create(
    #                 property=instance,
    #                 field=field,
    #                 value=json.dumps({
    #                     "option":fv.get("option"),
    #                     "value":fv.get("value"),
    #                     "icon":fv.get("icon")
    #                 })
    #             )

    def handle_related(self, instance):

        # =================================================
        # AMENITIES
        # =================================================

        # amenities = self.context.get(
        #     "amenities_list",
        #     None
        # )

        # # ONLY UPDATE IF USER SENT AMENITIES
        # if amenities is not None:

        #     amenity_objects = Amenities.objects.filter(
        #         id__in=amenities
        #     )

        #     instance.amenities.set(
        #         amenity_objects
        #     )

        request = self.context.get("request")

        # ONLY RUN IF FIELD EXISTS IN REQUEST
        if (
            request
            and hasattr(request, "data")
            and "amenities" in request.data
        ):

            amenities = self.context.get(
                "amenities_list",
                []
            )

            # REMOVE EMPTY VALUES
            amenities = [
                a for a in amenities
                if a not in ["", None]
            ]

            # KEEP OLD AMENITIES IF EMPTY VALUE SENT
            if amenities:

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

            instance.land_mark = lm

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

        # fallback support
        if fv_list is None:

            fv_list = self.context.get(
                "features_list",
                None
            )

        # ONLY UPDATE IF FEATURES SENT
        if fv_list is not None:

            # remove old
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

    def to_representation(self,instance):

        data=super().to_representation(
            instance
        )

        data["owner"]=(
            instance.owner
            if instance.owner
            else None
        )

        return data

    def get_amenities(self,obj):

        return [
            {
                "id":a.id,
                "name":a.name
            }
            for a in obj.amenities.all()
        ]

    def get_selling_points(self,obj):

        if isinstance(
            obj.selling_points,
            list
        ):
            return obj.selling_points

        return []

    def get_landmarks(self,obj):

        if isinstance(
            obj.land_mark,
            list
        ):
            return obj.land_mark

        return []

    # def get_features(self,obj):

    #     data=[]

    #     for f in obj.property_features.select_related(
    #         "field"
    #     ):

    #         try:
    #             value=json.loads(f.value)

    #         except:
    #             value={
    #                 "value":f.value
    #             }

    #         data.append({

    #             "name":
    #             f.field.field_name,

    #             "value":
    #             value.get("value"),

    #             "option":
    #             value.get("option"),

    #             "icon":
    #             (
    #                 f.field.icon.url
    #                 if f.field.icon
    #                 else None
    #             )
    #         })

    #     return data

    def get_features(self, obj):

        data = []

        for f in obj.property_features.select_related("field"):

            try:
                value = json.loads(f.value)

            except:
                value = {
                    "value": f.value
                }

            # =========================================
            # USE OPTION NAME IF EXISTS
            # =========================================

            feature_name = (
                value.get("option")
                if value.get("option")
                else f.field.field_name
            )

            # =========================================
            # CLEAN VALUE
            # =========================================

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

    # def get_images(self,obj):

    #     request=self.context.get(
    #         "request"
    #     )

    #     return [

    #         request.build_absolute_uri(
    #             i.image.url
    #         )

    #         if request else i.image.url

    #         for i in obj.images.all()

    #         if i.image
    #     ]

    def get_image(self,obj):

        if not obj.image:
            return None

        request=self.context.get(
            "request"
        )

        return (
            request.build_absolute_uri(
                obj.image.url
            )
            if request
            else obj.image.url
        )

# class UserPropertySerializer(serializers.ModelSerializer):

#     id = serializers.UUIDField(
#         read_only=True
#     )

#     images = serializers.SerializerMethodField()
#     image = serializers.SerializerMethodField()
#     amenities = serializers.SerializerMethodField()
#     selling_points = serializers.SerializerMethodField()
#     landmarks = serializers.SerializerMethodField()
#     features = serializers.SerializerMethodField()

#     # =====================================================
#     # ✅ OWNER FIELD
#     # =====================================================

#     owner = serializers.CharField(
#         required=False
#     )

#     category = serializers.PrimaryKeyRelatedField(
#         queryset=Category.objects.all()
#     )

#     subcategory = serializers.CharField(
#         required=False,
#         allow_null=True,
#         allow_blank=True
#     )

#     purpose = serializers.CharField(
#         required=False,
#         allow_null=True,
#         allow_blank=True
#     )

#     class Meta:

#         model = Property

#         fields = "__all__"

#     # =====================================================
#     # CREATE
#     # =====================================================

#     def create(self, validated_data):

#         # =================================================
#         # ✅ OWNER CREATE
#         # =================================================

#         owner_name = self.initial_data.get(
#             "owner"
#         )

#         if owner_name:

#             owner_obj = UserCreate.objects.filter(
#                 name__iexact=owner_name.strip()
#             ).first()

#             if not owner_obj:

#                 raise serializers.ValidationError({
#                     "owner":
#                     "Owner not found"
#                 })

#             validated_data["owner"] = owner_obj

#         # =================================================
#         # SUBCATEGORY
#         # =================================================

#         sub = self.initial_data.get(
#             "subcategory"
#         )

#         if sub:

#             sub_obj = Subcategory.objects.filter(
#                 name__iexact=sub
#             ).first()

#             if sub_obj:
#                 validated_data["subcategory"] = sub_obj

#         # =================================================
#         # PURPOSE
#         # =================================================

#         pur = self.initial_data.get(
#             "purpose"
#         )

#         if pur:

#             pur_obj = Purpose.objects.filter(
#                 name__iexact=pur
#             ).first()

#             if pur_obj:
#                 validated_data["purpose"] = pur_obj

#         instance = Property.objects.create(
#             **validated_data
#         )

#         self.handle_related(instance)

#         return instance

#     # =====================================================
#     # UPDATE
#     # =====================================================

#     def update(self, instance, validated_data):

#         # =================================================
#         # ✅ OWNER UPDATE
#         # =================================================

#         owner_name = self.initial_data.get(
#             "owner"
#         )

#         if owner_name:

#             owner_obj = UserCreate.objects.filter(
#                 name__iexact=owner_name.strip()
#             ).first()

#             if not owner_obj:

#                 raise serializers.ValidationError({
#                     "owner":
#                     "Owner not found"
#                 })

#             instance.owner = owner_obj

#         # =================================================
#         # SUBCATEGORY UPDATE
#         # =================================================

#         sub = self.initial_data.get(
#             "subcategory"
#         )

#         if sub:

#             sub_obj = Subcategory.objects.filter(
#                 name__iexact=sub
#             ).first()

#             if sub_obj:
#                 instance.subcategory = sub_obj

#         # =================================================
#         # PURPOSE UPDATE
#         # =================================================

#         pur = self.initial_data.get(
#             "purpose"
#         )

#         if pur:

#             pur_obj = Purpose.objects.filter(
#                 name__iexact=pur
#             ).first()

#             if pur_obj:
#                 instance.purpose = pur_obj

#         # =================================================
#         # OTHER FIELDS UPDATE
#         # =================================================

#         for k, v in validated_data.items():

#             if k == "owner":
#                 continue

#             setattr(instance, k, v)

#         instance.save()

#         self.handle_related(instance)

#         return instance

#     # =====================================================
#     # RELATED
#     # =====================================================

#     def handle_related(self, instance):

#         amenities = self.context.get(
#             "amenities_list"
#         )

#         if amenities is not None:

#             amenity_objects = Amenities.objects.filter(
#                 id__in=amenities
#             )

#             instance.amenities.set(
#                 amenity_objects
#             )

#         sp = self.context.get(
#             "selling_points_list"
#         )

#         if sp is not None:

#             instance.selling_points = sp

#             instance.save(
#                 update_fields=[
#                     "selling_points"
#                 ]
#             )

#         lm = self.context.get(
#             "landmarks_list"
#         )

#         if lm is not None:

#             instance.land_mark = lm

#             instance.save(
#                 update_fields=[
#                     "land_mark"
#                 ]
#             )

#         fv_list = self.context.get(
#             "field_values"
#         )

#         if fv_list is not None:

#             PropertyFeature.objects.filter(
#                 property=instance
#             ).delete()

#             for fv in fv_list:

#                 if not isinstance(fv, dict):
#                     continue

#                 field = SubcategoryField.objects.filter(
#                     subcategory=instance.subcategory,
#                     field_name__iexact=fv.get("name")
#                 ).first()

#                 if not field:
#                     continue

#                 PropertyFeature.objects.create(
#                     property=instance,
#                     field=field,
#                     value=json.dumps({
#                         "option": fv.get("option"),
#                         "value": fv.get("value"),
#                         "icon": fv.get("icon")
#                     })
#                 )

#     # =====================================================
#     # OUTPUT
#     # =====================================================

#     def to_representation(self, instance):

#         data = super().to_representation(
#             instance
#         )

#         # =================================================
#         # ✅ OWNER NAME ONLY
#         # =================================================

#         data["owner"] = (
#             instance.owner.name
#             if instance.owner
#             else None
#         )

#         return data

#     def get_amenities(self, obj):

#         return [

#             {
#                 "id": a.id,
#                 "name": a.name
#             }

#             for a in obj.amenities.all()
#         ]

#     def get_selling_points(self, obj):

#         if isinstance(
#             obj.selling_points,
#             list
#         ):
#             return obj.selling_points

#         return []

#     def get_landmarks(self, obj):

#         if isinstance(
#             obj.land_mark,
#             list
#         ):
#             return obj.land_mark

#         return []

#     def get_features(self, obj):

#         data = []

#         for f in obj.property_features.select_related(
#             "field"
#         ):

#             try:
#                 value = json.loads(f.value)

#             except:
#                 value = {
#                     "value": f.value
#                 }

#             data.append({

#                 "field_name":
#                 f.field.field_name,

#                 "value":
#                 value.get("value"),

#                 "option":
#                 value.get("option"),

#                 "icon":
#                 (
#                     f.field.icon.url
#                     if f.field.icon
#                     else None
#                 )
#             })

#         return data

#     def get_images(self, obj):

#         request = self.context.get(
#             "request"
#         )

#         return [

#             request.build_absolute_uri(
#                 i.image.url
#             )

#             if request else i.image.url

#             for i in obj.images.all()

#             if i.image
#         ]

#     def get_image(self, obj):

#         if not obj.image:
#             return None

#         request = self.context.get(
#             "request"
#         )

#         return (
#             request.build_absolute_uri(
#                 obj.image.url
#             )
#             if request
#             else obj.image.url
#         )

# class UserPropertySerializer(serializers.ModelSerializer):

#     id = serializers.UUIDField(
#         read_only=True
#     )

#     images = serializers.SerializerMethodField()
#     image = serializers.SerializerMethodField()
#     amenities = serializers.SerializerMethodField()
#     selling_points = serializers.SerializerMethodField()
#     landmarks = serializers.SerializerMethodField()
#     features = serializers.SerializerMethodField()

#     category = serializers.PrimaryKeyRelatedField(
#         queryset=Category.objects.all()
#     )

#     subcategory = serializers.CharField(
#         required=False,
#         allow_null=True,
#         allow_blank=True
#     )

#     purpose = serializers.CharField(
#         required=False,
#         allow_null=True,
#         allow_blank=True
#     )

#     class Meta:

#         model = Property

#         fields = "__all__"

#     # =====================================================
#     # UPDATE
#     # =====================================================

#     def update(self, instance, validated_data):

#         sub = self.initial_data.get(
#             "subcategory"
#         )

#         if sub:

#             sub_obj = Subcategory.objects.filter(
#                 name__iexact=sub
#             ).first()

#             if sub_obj:
#                 instance.subcategory = sub_obj

#         pur = self.initial_data.get(
#             "purpose"
#         )

#         if pur:

#             pur_obj = Purpose.objects.filter(
#                 name__iexact=pur
#             ).first()

#             if pur_obj:
#                 instance.purpose = pur_obj

#         for k, v in validated_data.items():
#             setattr(instance, k, v)

#         instance.save()

#         self.handle_related(instance)

#         return instance

#     # =====================================================
#     # RELATED
#     # =====================================================

#     def handle_related(self, instance):

#         # =================================================
#         # ✅ FIXED AMENITIES
#         # =================================================

#         amenities = self.context.get(
#             "amenities_list"
#         )

#         if amenities is not None:

#             amenity_objects = Amenities.objects.filter(
#                 id__in=amenities
#             )

#             instance.amenities.set(
#                 amenity_objects
#             )

#         # =================================================
#         # SELLING POINTS
#         # =================================================

#         sp = self.context.get(
#             "selling_points_list"
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
#             "landmarks_list"
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
#             "field_values"
#         )

#         if fv_list is not None:

#             PropertyFeature.objects.filter(
#                 property=instance
#             ).delete()

#             for fv in fv_list:

#                 if not isinstance(fv, dict):
#                     continue

#                 field = SubcategoryField.objects.filter(
#                     subcategory=instance.subcategory,
#                     field_name__iexact=fv.get("name")
#                 ).first()

#                 if not field:
#                     continue

#                 PropertyFeature.objects.create(
#                     property=instance,
#                     field=field,
#                     value=json.dumps({
#                         "option": fv.get("option"),
#                         "value": fv.get("value"),
#                         "icon": fv.get("icon")
#                     })
#                 )

#     # =====================================================
#     # OUTPUT
#     # =====================================================

#     def get_amenities(self, obj):

#         return [

#             {
#                 "id": a.id,
#                 "name": a.name
#             }

#             for a in obj.amenities.all()
#         ]

#     def get_selling_points(self, obj):

#         if isinstance(
#             obj.selling_points,
#             list
#         ):
#             return obj.selling_points

#         return []

#     def get_landmarks(self, obj):

#         if isinstance(
#             obj.land_mark,
#             list
#         ):
#             return obj.land_mark

#         return []

#     def get_features(self, obj):

#         data = []

#         for f in obj.property_features.select_related(
#             "field"
#         ):

#             try:
#                 value = json.loads(f.value)

#             except:
#                 value = {
#                     "value": f.value
#                 }

#             data.append({

#                 "field_name":
#                 f.field.field_name,

#                 "value":
#                 value.get("value"),

#                 "option":
#                 value.get("option"),

#                 "icon":
#                 (
#                     f.field.icon.url
#                     if f.field.icon
#                     else None
#                 )
#             })

#         return data

#     def get_images(self, obj):

#         request = self.context.get(
#             "request"
#         )

#         return [

#             request.build_absolute_uri(
#                 i.image.url
#             )

#             if request else i.image.url

#             for i in obj.images.all()

#             if i.image
#         ]

#     def get_image(self, obj):

#         if not obj.image:
#             return None

#         request = self.context.get(
#             "request"
#         )

#         return (
#             request.build_absolute_uri(
#                 obj.image.url
#             )
#             if request
#             else obj.image.url
#         )

# from rest_framework import serializers
# import json

# from developer.models import (
#     Property,
#     Category,
#     Subcategory,
#     Purpose,
#     Amenities,
#     PropertyFeature,
#     SubcategoryField,
#     FieldOption,
# )


# class UserPropertySerializer(serializers.ModelSerializer):

#     # =====================================================
#     # BASIC
#     # =====================================================

#     id = serializers.UUIDField(read_only=True)

#     owner = serializers.PrimaryKeyRelatedField(
#         read_only=True
#     )

#     # =====================================================
#     # FOREIGN KEYS
#     # =====================================================

#     category = serializers.PrimaryKeyRelatedField(
#         queryset=Category.objects.all()
#     )

#     subcategory = serializers.SlugRelatedField(
#         slug_field="name",
#         queryset=Subcategory.objects.all()
#     )

#     purpose = serializers.SlugRelatedField(
#         slug_field="name",
#         queryset=Purpose.objects.all()
#     )

#     # =====================================================
#     # CUSTOM RESPONSE FIELDS
#     # =====================================================

#     amenities = serializers.SerializerMethodField()

#     images = serializers.SerializerMethodField()

#     image = serializers.SerializerMethodField()

#     features = serializers.SerializerMethodField()

#     # =====================================================
#     # JSON FIELDS
#     # =====================================================

#     selling_points = serializers.JSONField(
#         required=False
#     )

#     land_mark = serializers.JSONField(
#         required=False
#     )

#     # =====================================================
#     # META
#     # =====================================================

#     class Meta:

#         model = Property

#         fields = [

#             "id",
#             "owner",

#             "category",
#             "subcategory",
#             "purpose",

#             "label",
#             "land_area",
#             "sq_ft",
#             "description",

#             "amenities",

#             "image",
#             "images",
#             "screenshot",

#             "perprice",
#             "price",
#             "deposit",

#             "phone",
#             "whatsapp",

#             "location",
#             "city",
#             "district",
#             "taluk",
#             "village",
#             "state",
#             "pincode",

#             "land_mark",
#             "selling_points",

#             "paid",
#             "added_by",
#             "market_staff",
#             "message",
#             "note",

#             "features",

#             "created_at",
#             "updated_at",
#             "duration_days",
#             "expiry_date",
#         ]

#         read_only_fields = [
#             "id",
#             "owner",
#             "created_at",
#             "updated_at",
#             "duration_days",
#             "expiry_date",
#         ]

#     # =====================================================
#     # VALIDATION
#     # =====================================================

#     def validate(self, attrs):

#         purpose_obj = attrs.get("purpose")

#         if not purpose_obj:
#             return attrs

#         purpose_name = purpose_obj.name.lower().strip()

#         price = attrs.get("price")

#         perprice = attrs.get("perprice")

#         deposit = attrs.get("deposit")

#         # =================================================
#         # SALE
#         # =================================================

#         if purpose_name == "sale":

#             if not price:
#                 raise serializers.ValidationError({
#                     "price": "Price is required for sale"
#                 })

#             if not perprice:
#                 raise serializers.ValidationError({
#                     "perprice": "Per price is required for sale"
#                 })

#             attrs["deposit"] = None

#         # =================================================
#         # RENT
#         # =================================================

#         elif purpose_name == "rent":

#             if not price:
#                 raise serializers.ValidationError({
#                     "price": "Rent amount is required"
#                 })

#             if not deposit:
#                 raise serializers.ValidationError({
#                     "deposit": "Deposit is required for rent"
#                 })

#             attrs["perprice"] = None

#         # =================================================
#         # LEASE
#         # =================================================

#         elif purpose_name == "lease":

#             if not price:
#                 raise serializers.ValidationError({
#                     "price": "Price is required for lease"
#                 })

#             attrs["deposit"] = None
#             attrs["perprice"] = None

#         return attrs

#     # =====================================================
#     # CREATE
#     # =====================================================

#     # =====================================================
#     # CREATE (FULL FIXED)
#     # =====================================================

#     def create(self, validated_data):

#         request = self.context.get("request")

#         if not request:
#             raise serializers.ValidationError(
#                 "Request missing"
#             )

#         # =========================================
#         # AMENITIES
#         # =========================================

#         amenities_ids = request.data.getlist(
#             "amenities"
#         )

#         # =========================================
#         # RAW JSON FIELDS
#         # =========================================

#         features_raw = request.data.get(
#             "features"
#         )

#         landmarks_raw = request.data.get(
#             "land_mark"
#         )

#         selling_points_raw = request.data.get(
#             "selling_points"
#         )

#         # =========================================
#         # FEATURES JSON PARSE
#         # =========================================

#         try:
#             features = json.loads(features_raw) \
#                 if features_raw else []

#         except Exception:
#             features = []

#         # =========================================
#         # LANDMARK JSON PARSE
#         # =========================================

#         try:
#             land_mark = json.loads(landmarks_raw) \
#                 if landmarks_raw else []

#         except Exception:
#             land_mark = []

#         # =========================================
#         # SELLING POINTS JSON PARSE
#         # =========================================

#         try:
#             selling_points = json.loads(
#                 selling_points_raw
#             ) if selling_points_raw else []

#         except Exception:
#             selling_points = []

#         # =========================================
#         # REMOVE DUPLICATE VALUES
#         # IMPORTANT FIX
#         # =========================================

#         validated_data.pop("land_mark", None)

#         validated_data.pop("selling_points", None)

#         # =========================================
#         # PURPOSE VALIDATION
#         # =========================================

#         purpose = validated_data.get("purpose")

#         purpose_name = ""

#         if purpose:
#             purpose_name = purpose.name.lower().strip()

#         # SALE
#         if purpose_name == "sale":

#             if not validated_data.get("price"):
#                 raise serializers.ValidationError({
#                     "price": "Price is required for sale"
#                 })

#             if not validated_data.get("perprice"):
#                 raise serializers.ValidationError({
#                     "perprice": "Per price is required for sale"
#                 })

#             validated_data["deposit"] = None

#         # RENT
#         elif purpose_name == "rent":

#             if not validated_data.get("price"):
#                 raise serializers.ValidationError({
#                     "price": "Rent amount required"
#                 })

#             if not validated_data.get("deposit"):
#                 raise serializers.ValidationError({
#                     "deposit": "Deposit required for rent"
#                 })

#             validated_data["perprice"] = None

#         # LEASE
#         elif purpose_name == "lease":

#             if not validated_data.get("price"):
#                 raise serializers.ValidationError({
#                     "price": "Price required for lease"
#                 })

#             validated_data["deposit"] = None
#             validated_data["perprice"] = None

#         # =========================================
#         # CREATE PROPERTY
#         # =========================================

#         property_obj = Property.objects.create(

#             owner=request.user,

#             land_mark=land_mark,

#             selling_points=selling_points,

#             **validated_data
#         )

#         # =========================================
#         # ADD AMENITIES
#         # =========================================

#         if amenities_ids:

#             amenities = Amenities.objects.filter(
#                 id__in=amenities_ids
#             )

#             property_obj.amenities.set(
#                 amenities
#             )

#         # =========================================
#         # ADD FEATURES
#         # =========================================

#         for item in features:

#             field_id = item.get("field_id")

#             option_id = item.get("option_id")

#             value = item.get("value")

#             field = SubcategoryField.objects.filter(
#                 id=field_id
#             ).first()

#             if not field:
#                 continue

#             # =====================================
#             # OPTION BASED FEATURE
#             # =====================================

#             if option_id:

#                 option = FieldOption.objects.filter(
#                     id=option_id,
#                     field=field
#                 ).first()

#                 if option:

#                     PropertyFeature.objects.create(

#                         property=property_obj,

#                         field=field,

#                         value=option.name
#                     )

#             # =====================================
#             # NORMAL VALUE FEATURE
#             # =====================================

#             else:

#                 if value is not None:

#                     PropertyFeature.objects.create(

#                         property=property_obj,

#                         field=field,

#                         value=str(value)
#                     )

#         return property_obj

#     def update(self, instance, validated_data):

#         request = self.context.get("request")

#         for attr, value in validated_data.items():
#             setattr(instance, attr, value)

#         instance.save()

#         # =================================================
#         # AMENITIES
#         # =================================================

#         amenities_ids = request.data.getlist(
#             "amenities"
#         )

#         if amenities_ids:

#             amenities = Amenities.objects.filter(
#                 id__in=amenities_ids
#             )

#             instance.amenities.set(
#                 amenities
#             )

#         # =================================================
#         # FEATURES UPDATE
#         # =================================================

#         features_raw = request.data.get(
#             "features"
#         )

#         if features_raw:

#             try:
#                 features = json.loads(
#                     features_raw
#                 )

#             except:
#                 features = []

#             instance.property_features.all().delete()

#             for item in features:

#                 if not isinstance(item, dict):
#                     continue

#                 field_id = item.get("field_id")

#                 option_id = item.get("option_id")

#                 value = item.get("value")

#                 field = SubcategoryField.objects.filter(
#                     id=field_id
#                 ).first()

#                 if not field:
#                     continue

#                 # =========================================
#                 # OPTION
#                 # =========================================

#                 if option_id:

#                     option = FieldOption.objects.filter(
#                         id=option_id,
#                         field=field
#                     ).first()

#                     if not option:
#                         continue

#                     try:
#                         count = int(value)

#                     except:
#                         count = 0

#                     PropertyFeature.objects.create(
#                         property=instance,
#                         field=field,
#                         value=json.dumps({
#                             "option": option.name,
#                             "count": count
#                         })
#                     )

#                 # =========================================
#                 # NORMAL
#                 # =========================================

#                 else:

#                     PropertyFeature.objects.create(
#                         property=instance,
#                         field=field,
#                         value=str(value)
#                     )

#         return instance

#     # =====================================================
#     # RESPONSE FORMAT
#     # =====================================================

#     def to_representation(self, instance):

#         data = {

#             "id": str(instance.id),

#             "images": self.get_images(instance),

#             "image": self.get_image(instance),

#             "amenities": self.get_amenities(instance),

#             "selling_points": (
#                 instance.selling_points or []
#             ),

#             "landmarks": (
#                 instance.land_mark or []
#             ),

#             "features": self.get_features(instance),

#             "category": (
#                 instance.category.id
#                 if instance.category else None
#             ),

#             "subcategory": (
#                 instance.subcategory.name
#                 if instance.subcategory else None
#             ),

#             "purpose": (
#                 instance.purpose.name
#                 if instance.purpose else None
#             ),

#             "label": instance.label,

#             "land_area": instance.land_area,

#             "sq_ft": instance.sq_ft,

#             "description": instance.description,

#             "screenshot": (
#                 instance.screenshot.url
#                 if instance.screenshot else None
#             ),

#             "price": instance.price,

#             "deposit": instance.deposit,

#             "perprice": instance.perprice,

#             "whatsapp": instance.whatsapp,

#             "phone": instance.phone,

#             "location": instance.location,

#             "city": instance.city,

#             "pincode": instance.pincode,

#             "district": instance.district,

#             "land_mark": instance.land_mark,

#             "owner": (
#                 instance.owner.name
#                 if instance.owner else None
#             ),

#             "taluk": instance.taluk,

#             "village": instance.village,

#             "state": instance.state,

#             "paid": instance.paid,

#             "notes": instance.note,

#             "created_at": instance.created_at,

#             "updated_at": instance.updated_at,

#             "duration_days": instance.duration_days,

#             "expiry_date": instance.expiry_date,

#             "user": str(instance.owner.id),
#         }

#         # =================================================
#         # REMOVE BASED ON PURPOSE
#         # =================================================

#         purpose = (
#             instance.purpose.name.lower().strip()
#             if instance.purpose else ""
#         )

#         if purpose == "rent":
#             data.pop("perprice", None)

#         elif purpose == "sale":
#             data.pop("deposit", None)

#         elif purpose == "lease":
#             data.pop("deposit", None)
#             data.pop("perprice", None)

#         return data

#     # =====================================================
#     # AMENITIES
#     # =====================================================

#     def get_amenities(self, obj):

#         return [
#             {
#                 "id": a.id,
#                 "name": a.name,
#                 "icon": (
#                     a.icon.url
#                     if a.icon else None
#                 )
#             }

#             for a in obj.amenities.all()
#         ]

#     # =====================================================
#     # IMAGES
#     # =====================================================

#     def get_images(self, obj):

#         return [

#             img.image.url
#             if img.image else None

#             for img in obj.images.all()
#         ]

#     def get_image(self, obj):

#         return (
#             obj.image.url
#             if obj.image else None
#         )

#     # =====================================================
#     # FEATURES
#     # =====================================================

#     def get_features(self, obj):

#         result = []

#         for feature in obj.property_features.select_related(
#             "field"
#         ):

#             icon = (
#                 feature.field.icon.url
#                 if feature.field.icon else None
#             )

#             # =============================================
#             # JSON OPTION VALUE
#             # =============================================

#             try:

#                 value_data = json.loads(
#                     feature.value
#                 )

#                 option = value_data.get(
#                     "option"
#                 )

#                 count = value_data.get(
#                     "count"
#                 )

#                 result.append({

#                     "name": option,

#                     "value": count,

#                     "icon": icon
#                 })

#             except:

#                 result.append({

#                     "name": (
#                         feature.field.field_name
#                     ),

#                     "value": feature.value,

#                     "icon": icon
#                 })

#         return result

# from rest_framework import serializers
# import json

# from developer.models import (
#     Property,
#     Category,
#     Subcategory,
#     Purpose,
#     Amenities,
#     PropertyFeature,
#     SubcategoryField,
# )


# class UserPropertySerializer(serializers.ModelSerializer):

#     # =====================================================
#     # BASIC
#     # =====================================================

#     id = serializers.UUIDField(read_only=True)

#     owner = serializers.PrimaryKeyRelatedField(
#         read_only=True
#     )

#     # =====================================================
#     # FOREIGN KEYS
#     # =====================================================

#     # SEND CATEGORY ID
#     category = serializers.PrimaryKeyRelatedField(
#         queryset=Category.objects.all()
#     )

#     # SEND SUBCATEGORY NAME
#     subcategory = serializers.SlugRelatedField(
#         slug_field="name",
#         queryset=Subcategory.objects.all()
#     )

#     # SEND PURPOSE NAME
#     purpose = serializers.SlugRelatedField(
#         slug_field="name",
#         queryset=Purpose.objects.all()
#     )

#     # =====================================================
#     # CUSTOM RESPONSE FIELDS
#     # =====================================================

#     amenities = serializers.SerializerMethodField()

#     images = serializers.SerializerMethodField()

#     image = serializers.SerializerMethodField()

#     features = serializers.SerializerMethodField()

#     # =====================================================
#     # JSON FIELDS
#     # =====================================================

#     selling_points = serializers.JSONField(
#         required=False,
#         allow_null=True
#     )

#     land_mark = serializers.JSONField(
#         required=False,
#         allow_null=True
#     )

#     # =====================================================
#     # META
#     # =====================================================

#     class Meta:

#         model = Property

#         fields = [

#             # BASIC
#             "id",
#             "owner",

#             # FK
#             "category",
#             "subcategory",
#             "purpose",

#             # PROPERTY
#             "label",
#             "land_area",
#             "sq_ft",
#             "description",

#             # AMENITIES
#             "amenities",

#             # IMAGES
#             "image",
#             "images",
#             "screenshot",

#             # PRICE
#             "perprice",
#             "price",
#             "deposit",

#             # CONTACT
#             "phone",
#             "whatsapp",

#             # LOCATION
#             "location",
#             "city",
#             "district",
#             "taluk",
#             "village",
#             "state",
#             "pincode",

#             # JSON
#             "land_mark",
#             "selling_points",

#             # EXTRA
#             "paid",
#             "added_by",
#             "market_staff",
#             "message",
#             "note",
#             "is_featured",

#             # FEATURES
#             "features",

#             # DATES
#             "created_at",
#             "updated_at",
#             "duration_days",
#             "expiry_date",
#         ]

#         read_only_fields = [
#             "id",
#             "owner",
#             "created_at",
#             "updated_at",
#             "duration_days",
#             "expiry_date",
#         ]

#     # =====================================================
#     # VALIDATE LANDMARK
#     # =====================================================

#     def validate_land_mark(self, value):

#         if not value:
#             return []

#         # ==========================================
#         # STRING -> JSON
#         # ==========================================

#         if isinstance(value, str):

#             try:
#                 value = json.loads(value)

#             except Exception:
#                 raise serializers.ValidationError(
#                     "Invalid land_mark JSON"
#                 )

#         # ==========================================
#         # MUST BE LIST
#         # ==========================================

#         if not isinstance(value, list):

#             raise serializers.ValidationError(
#                 "land_mark must be list"
#             )

#         cleaned = []

#         for item in value:

#             if not isinstance(item, dict):

#                 raise serializers.ValidationError(
#                     "Invalid landmark format"
#                 )

#             name = item.get("name")
#             distance = item.get("distance")

#             if not name or not distance:

#                 raise serializers.ValidationError(
#                     "Each landmark requires name and distance"
#                 )

#             cleaned.append({
#                 "name": str(name).strip(),
#                 "distance": str(distance).strip()
#             })

#         return cleaned

#     # =====================================================
#     # VALIDATE SELLING POINTS
#     # =====================================================

#     def validate_selling_points(self, value):

#         if not value:
#             return []

#         # ==========================================
#         # STRING -> JSON
#         # ==========================================

#         if isinstance(value, str):

#             try:
#                 value = json.loads(value)

#             except Exception:
#                 raise serializers.ValidationError(
#                     "Invalid selling_points JSON"
#                 )

#         # ==========================================
#         # MUST BE LIST
#         # ==========================================

#         if not isinstance(value, list):

#             raise serializers.ValidationError(
#                 "selling_points must be list"
#             )

#         cleaned = []

#         for item in value:

#             cleaned.append(
#                 str(item).strip()
#             )

#         return cleaned

#     # =====================================================
#     # CREATE
#     # =====================================================

#     def create(self, validated_data):

#         request = self.context.get("request")

#         if not request or not request.user:

#             raise serializers.ValidationError({
#                 "user": "Authentication required"
#             })

#         # =================================================
#         # REMOVE M2M
#         # =================================================

#         amenities_ids = request.data.getlist(
#             "amenities"
#         )

#         # =================================================
#         # CREATE PROPERTY
#         # =================================================

#         property_obj = Property.objects.create(
#             owner=request.user,
#             **validated_data
#         )

#         # =================================================
#         # ADD AMENITIES
#         # =================================================

#         if amenities_ids:

#             amenity_objects = Amenities.objects.filter(
#                 id__in=amenities_ids
#             )

#             property_obj.amenities.set(
#                 amenity_objects
#             )

#         # =================================================
#         # FEATURES CREATE
#         # =================================================

#         raw_features = request.data.get(
#             "features"
#         )

#         if raw_features:

#             try:
#                 features = json.loads(raw_features)

#             except Exception:
#                 features = []

#             if isinstance(features, list):

#                 for item in features:

#                     if not isinstance(item, dict):
#                         continue

#                     field_name = item.get(
#                         "field_name"
#                     )

#                     value = item.get(
#                         "value"
#                     )

#                     if not field_name or not value:
#                         continue

#                     field_obj = SubcategoryField.objects.filter(
#                         subcategory=property_obj.subcategory,
#                         field_name__iexact=field_name
#                     ).first()

#                     if field_obj:

#                         PropertyFeature.objects.create(
#                             property=property_obj,
#                             field=field_obj,
#                             value=str(value)
#                         )

#         return property_obj

#     # =====================================================
#     # UPDATE
#     # =====================================================

#     def update(self, instance, validated_data):

#         request = self.context.get("request")

#         validated_data.pop("owner", None)

#         # =================================================
#         # UPDATE NORMAL FIELDS
#         # =================================================

#         for attr, value in validated_data.items():

#             setattr(instance, attr, value)

#         instance.save()

#         # =================================================
#         # UPDATE AMENITIES
#         # =================================================

#         amenities_ids = request.data.getlist(
#             "amenities"
#         )

#         if amenities_ids:

#             amenity_objects = Amenities.objects.filter(
#                 id__in=amenities_ids
#             )

#             instance.amenities.set(
#                 amenity_objects
#             )

#         return instance

#     # =====================================================
#     # RESPONSE
#     # =====================================================

#     def to_representation(self, instance):

#         data = super().to_representation(instance)

#         # =================================================
#         # ID
#         # =================================================

#         data["id"] = str(instance.id)

#         # =================================================
#         # OWNER
#         # =================================================

#         data["owner"] = {
#             "id": str(instance.owner.id),
#             "name": getattr(instance.owner, "name", None)
#         }

#         # =================================================
#         # CATEGORY
#         # =================================================

#         data["category"] = {
#             "id": instance.category.id,
#             "name": instance.category.name
#         } if instance.category else None

#         # =================================================
#         # SUBCATEGORY
#         # =================================================

#         data["subcategory"] = {
#             "id": instance.subcategory.id,
#             "name": instance.subcategory.name
#         } if instance.subcategory else None

#         # =================================================
#         # PURPOSE
#         # =================================================

#         data["purpose"] = {
#             "id": instance.purpose.id,
#             "name": instance.purpose.name
#         } if instance.purpose else None

#         return data

#     # =====================================================
#     # AMENITIES RESPONSE
#     # =====================================================

#     def get_amenities(self, obj):

#         data = []

#         for amenity in obj.amenities.all():

#             icon = None

#             if amenity.icon:

#                 try:
#                     icon = amenity.icon.url

#                 except Exception:
#                     icon = str(amenity.icon)

#             data.append({

#                 "id": amenity.id,

#                 "name": amenity.name,

#                 "icon": icon
#             })

#         return data

#     # =====================================================
#     # PROPERTY IMAGES RESPONSE
#     # =====================================================

#     def get_images(self, obj):

#         data = []

#         for img in obj.images.all():

#             image_url = None

#             if img.image:

#                 try:
#                     image_url = img.image.url

#                 except Exception:
#                     image_url = str(img.image)

#             data.append({

#                 "id": str(img.id),

#                 "image": image_url
#             })

#         return data

#     # =====================================================
#     # MAIN IMAGE
#     # =====================================================

#     def get_image(self, obj):

#         if obj.image:

#             try:
#                 return obj.image.url

#             except Exception:
#                 return str(obj.image)

#         return None

#     # =====================================================
#     # FEATURES RESPONSE
#     # =====================================================

#     def get_features(self, obj):

#         data = []

#         for feature in obj.property_features.select_related(
#             "field"
#         ):

#             icon = None

#             if feature.field.icon:

#                 try:
#                     icon = feature.field.icon.url

#                 except Exception:
#                     icon = str(feature.field.icon)

#             data.append({

#                 "id": feature.id,

#                 "field_name": feature.field.field_name,

#                 "value": feature.value,

#                 "icon": icon
#             })

#         return data



# from rest_framework import serializers
# import json

# class UserPropertySerializer(serializers.ModelSerializer):

#     # =====================================================
#     # UUID
#     # =====================================================

#     id = serializers.UUIDField(read_only=True)

#     # =====================================================
#     # OWNER
#     # =====================================================

#     owner = serializers.PrimaryKeyRelatedField(
#         read_only=True
#     )

#     # =====================================================
#     # FOREIGN KEYS
#     # =====================================================

#     category = serializers.PrimaryKeyRelatedField(
#         queryset=Category.objects.all()
#     )

#     subcategory = serializers.SlugRelatedField(
#         slug_field="name",
#         queryset=Subcategory.objects.all()
#     )

#     purpose = serializers.SlugRelatedField(
#         slug_field="name",
#         queryset=Purpose.objects.all()
#     )

#     # =====================================================
#     # CUSTOM FIELDS
#     # =====================================================

#     images = serializers.SerializerMethodField()

#     image = serializers.SerializerMethodField()

#     features = serializers.SerializerMethodField()

#     # =====================================================
#     # JSON FIELDS
#     # =====================================================

#     selling_points = serializers.JSONField(
#         required=False
#     )

#     land_mark = serializers.JSONField(
#         required=False
#     )

#     # =====================================================
#     # META
#     # =====================================================

#     class Meta:

#         model = Property

#         fields = [
#             "id",
#             "owner",

#             "category",
#             "subcategory",
#             "purpose",

#             "label",
#             "land_area",
#             "sq_ft",
#             "description",

#             "amenities",

#             "image",
#             "images",
#             "screenshot",

#             "perprice",
#             "price",
#             "deposit",

#             "phone",
#             "whatsapp",

#             "location",
#             "city",
#             "district",
#             "taluk",
#             "village",
#             "state",
#             "pincode",

#             "land_mark",
#             "selling_points",

#             "paid",
#             "added_by",
#             "market_staff",
#             "message",
#             "note",

#             "is_featured",

#             "features",

#             "created_at",
#             "updated_at",
#             "duration_days",
#             "expiry_date",
#         ]

#         read_only_fields = [
#             "id",
#             "owner",
#             "property_code",
#             "created_at",
#             "updated_at",
#             "duration_days",
#             "expiry_date",
#         ]

#     # =====================================================
#     # VALIDATE JSON STRING INPUT
#     # =====================================================

#     def validate_land_mark(self, value):

#         if isinstance(value, str):
#             value = json.loads(value)

#         return value

#     def validate_selling_points(self, value):

#         if isinstance(value, str):
#             value = json.loads(value)

#         return value

#     # =====================================================
#     # CREATE
#     # =====================================================

#     def create(self, validated_data):

#         request = self.context.get("request")

#         if not request or not request.user:
#             raise serializers.ValidationError({
#                 "user": "Authentication required"
#             })

#         amenities = validated_data.pop(
#             "amenities",
#             []
#         )

#         property_obj = Property.objects.create(
#             owner=request.user,
#             **validated_data
#         )

#         if amenities:
#             property_obj.amenities.set(amenities)

#         return property_obj

#     # =====================================================
#     # UPDATE
#     # =====================================================

#     def update(self, instance, validated_data):

#         validated_data.pop("owner", None)

#         amenities = validated_data.pop(
#             "amenities",
#             None
#         )

#         for attr, value in validated_data.items():
#             setattr(instance, attr, value)

#         instance.save()

#         if amenities is not None:
#             instance.amenities.set(amenities)

#         return instance

#     # =====================================================
#     # OUTPUT
#     # =====================================================

#     def to_representation(self, instance):

#         data = super().to_representation(instance)

#         data["id"] = str(instance.id)

#         data["owner"] = (
#             str(instance.owner.id)
#             if instance.owner else None
#         )

#         data["category"] = (
#             instance.category.id
#             if instance.category else None
#         )

#         data["subcategory"] = (
#             instance.subcategory.name
#             if instance.subcategory else None
#         )

#         data["purpose"] = (
#             instance.purpose.name
#             if instance.purpose else None
#         )

#         return data

#     # =====================================================
#     # IMAGES
#     # =====================================================

#     def get_images(self, obj):

#         request = self.context.get("request")

#         data = []

#         for img in obj.images.all():

#             if img.image:

#                 if request:
#                     data.append(
#                         request.build_absolute_uri(
#                             img.image.url
#                         )
#                     )
#                 else:
#                     data.append(img.image.url)

#         return data

#     def get_image(self, obj):

#         request = self.context.get("request")

#         if obj.image:

#             if request:
#                 return request.build_absolute_uri(
#                     obj.image.url
#                 )

#             return obj.image.url

#         return None

#     # =====================================================
#     # FEATURES
#     # =====================================================

#     def get_features(self, obj):

#         return [
#             {
#                 "id": feature.id,
#                 "field": feature.field.field_name,
#                 "value": feature.value,
#                 "icon": (
#                     feature.icon.url
#                     if feature.icon else None
#                 )
#             }
#             for feature in obj.property_features.select_related("field")
#         ]
    

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

from rest_framework import serializers
from .models import UserProfile


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

    plan_type = serializers.CharField()

    plan_id = serializers.UUIDField()

