from rest_framework import serializers
from .models import *
from django.contrib.auth.hashers import check_password
from django.core.mail import send_mail
from django.contrib.auth.hashers import make_password
from agents.models import *
import shortuuid

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



class UserProfileSerializer(serializers.ModelSerializer):

    email = serializers.CharField(source="user.email", read_only=True)
    mobile = serializers.CharField(source="user.mobile")  # writable
    name = serializers.CharField(source="user.name", read_only=True)
    is_verified = serializers.BooleanField(source="user.is_verified", read_only=True)

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

    # 🔥 IMPORTANT PART
    def update(self, instance, validated_data):

        # Extract user data if present
        user_data = validated_data.pop("user", None)

        # Update UserProfile fields
        for attr, value in validated_data.items():
            setattr(instance, attr, value)

        instance.save()

        # Update related UserCreate fields (mobile)
        if user_data:
            user = instance.user
            user.mobile = user_data.get("mobile", user.mobile)
            user.save()

        return instance


class AmenitiesSerializer(serializers.ModelSerializer):

    icon = serializers.SerializerMethodField()

    class Meta:
        model = Amenities
        fields = ["id", "name", "icon"]

    def get_icon(self, obj):
        if obj.icon:
            return obj.icon.url   # 🔥 This gives full Cloudinary URL
        return None




class InboxSerializer(serializers.ModelSerializer):
    class Meta:
        model = Inbox
        fields = "__all__"
        read_only_fields = ["created_at", "is_read", "is_removed"]

import shortuuid

class AgentSerializer(serializers.ModelSerializer):
    agent_code = serializers.CharField(read_only=True)
    plan = serializers.CharField(source='plan.name', read_only=True)

    class Meta:
        model = AgentUserProfile
        fields = "__all__"
        extra_kwargs = {
            'password': {'write_only': True}
        } # exclude the actual password

class AgentRegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    plan = serializers.CharField(required=False)  # plan name from frontend

    class Meta:
        model = AgentUserProfile
        fields = [
            "username",
            "password",
            "phone_number",
            "address",
            "city",               # 🔹 new city field
            "profile_image",
            "pin_code",
            "email",
            "agent_type",
            "plan",
            "professional_bio",
            "specializations",
            "operating_cities",
            "social_media",
        ]

    def validate(self, data):
        plan_name = data.get("plan")
        agent_type = data.get("agent_type")

        # Plan required for premium & elite
        if agent_type in ["premium", "elite"] and not plan_name:
            raise serializers.ValidationError({
                "plan": "Plan is required for Premium and Elite agents"
            })

        # Convert plan name to plan object
        if plan_name:
            try:
                plan_obj = PremiumPlan.objects.get(name__iexact=plan_name)
            except PremiumPlan.DoesNotExist:
                raise serializers.ValidationError({
                    "plan": "Plan not found"
                })
            data["plan"] = plan_obj

        return data

    def create(self, validated_data):
        password = validated_data.pop("password")
        agent = AgentUserProfile(**validated_data)
        agent.set_password(password)
        agent.is_agent = True

        if agent.plan:
            agent.paid = True

        agent.save()
        return agent



class AgentLoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField(write_only=True)

    def validate(self, data):
        username = data.get("username")
        password = data.get("password")

        try:
            user = AgentUserProfile.objects.get(username=username)
        except AgentUserProfile.DoesNotExist:
            raise serializers.ValidationError({"error": "Invalid username"})

        if not user.check_password(password):
            raise serializers.ValidationError({"error": "Invalid password"})

        data["user"] = user
        return data
    
class AgentProfileSerializer(serializers.ModelSerializer):
    agent_id = serializers.CharField(source='agent_code', read_only=True)  # 🔹 renamed
    plan_name = serializers.CharField(source='plan.name', read_only=True)

    class Meta:
        model = AgentUserProfile
        fields = [
            'agent_id',              # 🔹 renamed
            'username',
            'email',
            'phone_number',
            'address',
            'city',                  # 🔹 include city
            'pin_code',
            'profile_image',
            'professional_title',
            'professional_bio',
            'specializations',
            'operating_cities',
            'social_media',
            'agent_type',
            'plan_name',
            'paid',
            'created_at'
        ]
        read_only_fields = ['agent_id', 'plan_name', 'paid', 'created_at']

    # Validate specializations list
    def validate_specializations(self, value):
        if value and not isinstance(value, list):
            raise serializers.ValidationError("Specializations must be a list.")
        return value

    # Validate social media JSON
    def validate_social_media(self, value):
        if value and not isinstance(value, dict):
            raise serializers.ValidationError("Social media must be a JSON object.")
        return value