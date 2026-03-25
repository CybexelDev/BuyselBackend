from rest_framework import serializers
from .models import *
from django.contrib.auth.hashers import check_password
from django.core.mail import send_mail
from django.contrib.auth.hashers import make_password
from agents.models import *
from developer.models import*
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

import shortuuid
class AgentSerializer(serializers.ModelSerializer):
    premium_plan = serializers.PrimaryKeyRelatedField(read_only=True)
    elite_plan = serializers.PrimaryKeyRelatedField(read_only=True)
    premium_plan_name = serializers.CharField(source="premium_plan.name", read_only=True)
    elite_plan_name = serializers.CharField(source="elite_plan.name", read_only=True)

    class Meta:
        model = AgentUserProfile
        fields = [
            "id",
            "agent_code",
            "username",
            "email",
            "phone_number",
            "address",
            "pin_code",
            "profile_image",
            "is_agent",
            "agent_type",
            "paid",
            "professional_bio",
            "specializations",
            "operating_cities",
            "social_media",
            "created_at",
            "premium_plan",
            "premium_plan_name",
            "elite_plan",
            "elite_plan_name",
            "plan_start_date",
            "plan_end_date",
        ]



class AgentRegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    premium_plan_name = serializers.CharField(write_only=True, required=False)
    elite_plan_name = serializers.CharField(write_only=True, required=False)

    premium_plan = serializers.SerializerMethodField(read_only=True)
    premium_plan_code = serializers.SerializerMethodField(read_only=True)
    elite_plan = serializers.SerializerMethodField(read_only=True)
    elite_plan_code = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = AgentUserProfile
        fields = [
            "username",
            "password",
            "email",
            "phone_number",
            "address",
            "pin_code",
            "profile_image",
            "is_agent",
            "agent_type",
            "paid",
            "professional_bio",
            "specializations",
            "operating_cities",
            "social_media",
            "premium_plan_name",
            "elite_plan_name",
            "premium_plan",
            "premium_plan_code",
            "elite_plan",
            "elite_plan_code",
            "plan_start_date",
            "plan_end_date",
        ]
        read_only_fields = [
            "premium_plan",
            "premium_plan_code",
            "elite_plan",
            "elite_plan_code",
            "plan_start_date",
            "plan_end_date",
        ]

    def get_premium_plan(self, obj):
        return obj.premium_plan.name if obj.premium_plan else None

    def get_premium_plan_code(self, obj):
        return obj.premium_plan.plan_code if obj.premium_plan else None

    def get_elite_plan(self, obj):
        return obj.elite_plan.name if obj.elite_plan else None

    def get_elite_plan_code(self, obj):
        return obj.elite_plan.plan_code if obj.elite_plan else None

    def validate(self, attrs):
        agent_type = attrs.get("agent_type")
        premium_plan_name = attrs.get("premium_plan_name")
        elite_plan_name = attrs.get("elite_plan_name")

        if agent_type == "premium":
            if not premium_plan_name:
                raise serializers.ValidationError({
                    "premium_plan_name": "Premium plan name is required for premium agents."
                })

        elif agent_type == "elite":
            if not elite_plan_name:
                raise serializers.ValidationError({
                    "elite_plan_name": "Elite plan name is required for elite agents."
                })

        return attrs

    def create(self, validated_data):
        premium_plan_name = validated_data.pop("premium_plan_name", None)
        elite_plan_name = validated_data.pop("elite_plan_name", None)
        password = validated_data.pop("password")

        specializations = validated_data.get("specializations")
        social_media = validated_data.get("social_media")

        if isinstance(specializations, str):
            validated_data["specializations"] = json.loads(specializations)

        if isinstance(social_media, str):
            validated_data["social_media"] = json.loads(social_media)

        if premium_plan_name:
            try:
                validated_data["premium_plan"] = PremiumPlan.objects.get(name=premium_plan_name)
            except PremiumPlan.DoesNotExist:
                raise serializers.ValidationError({
                    "premium_plan_name": "Selected premium plan does not exist."
                })

        if elite_plan_name:
            try:
                validated_data["elite_plan"] = ElitePlan.objects.get(name=elite_plan_name)
            except ElitePlan.DoesNotExist:
                raise serializers.ValidationError({
                    "elite_plan_name": "Selected elite plan does not exist."
                })

        agent = AgentUserProfile(**validated_data)
        agent.set_password(password)
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
    agent_code = serializers.CharField(read_only=True)
    premium_plan_name = serializers.CharField(source="premium_plan.name", read_only=True)
    elite_plan_name = serializers.CharField(source="elite_plan.name", read_only=True)

    class Meta:
        model = AgentUserProfile
        fields = [
            "id",
            "agent_code",
            "username",
            "email",
            "phone_number",
            "address",
            "pin_code",
            "profile_image",
            "is_agent",
            "agent_type",
            "paid",
            "professional_bio",
            "specializations",
            "operating_cities",
            "social_media",
            "created_at",
            "plan_start_date",
            "plan_end_date",
            "premium_plan",
            "premium_plan_name",
            "elite_plan",
            "elite_plan_name",
        ]


class PremiumPlanSerializer(serializers.ModelSerializer):
    class Meta:
        model = PremiumPlan
        fields = "__all__"


class ElitePlanSerializer(serializers.ModelSerializer):
    class Meta:
        model = ElitePlan
        fields = "__all__"