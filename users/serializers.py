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


class UserProfileSerializer(serializers.ModelSerializer):

    email = serializers.CharField(source="user.email", read_only=True)
    mobile = serializers.CharField(source="user.mobile", required=False)
    name = serializers.CharField(source="user.name", read_only=True)
    city = serializers.CharField(required=False, allow_blank=True, allow_null=True)
    is_verified = serializers.BooleanField(source="user.is_verified", read_only=True)

    created_at = serializers.DateTimeField(format="%d-%m-%Y", read_only=True)

    #  Cloudinary full URL
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

    # ✅ Always show city
    def to_representation(self, instance):
        data = super().to_representation(instance)
        data["city"] = instance.city or ""
        return data

    # ✅ Convert Cloudinary image to full URL
    def get_image(self, obj):
        if obj.image:
            try:
                url, _ = cloudinary_url(
                    obj.image.public_id,
                    secure=True
                )
                return url
            except Exception:
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
import shortuuid
class AgentReviewSerializer(serializers.ModelSerializer):
    user_name = serializers.SerializerMethodField()
    user_image = serializers.SerializerMethodField()
    total_likes = serializers.SerializerMethodField()
    created_at = serializers.SerializerMethodField()

    class Meta:
        model = AgentReview
        fields = [
            "id",
            "user_name",
            "user_image",
            "rating",
            "review",
            "total_likes",
            "created_at"
        ]

    def get_user_name(self, obj):
        if obj.user:
            return obj.user.name
        return "Anonymous"

    def get_user_image(self, obj):
        if obj.user and obj.user.name:
            name = obj.user.name
        else:
            name = "Anonymous"
        return f"https://ui-avatars.com/api/?name={name}&background=random&color=fff"

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


class AgentProfileSerializer(serializers.ModelSerializer):
    agent_id = serializers.CharField(source='agent_code', read_only=True)
    plan_name = serializers.SerializerMethodField()
    profile_image = serializers.SerializerMethodField()
    specializations = serializers.SerializerMethodField()

    class Meta:
        model = AgentUserProfile
        fields = [
            'agent_id',
            'username',
            'email',
            'phone_number',
            'whatsapp_number',
            'address',
            'city',
            'pin_code',
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

    def get_profile_image(self, obj):
        return obj.get_profile_image()

    def get_specializations(self, obj):
        return [cat.name for cat in obj.specializations.all()]

    def get_plan_name(self, obj):
        if obj.plan:
            return obj.plan.name
        if obj.elite_plan:
            return obj.elite_plan.name
        return None

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

from .utils import encode_id
class AgentPropertySerializer(serializers.ModelSerializer):

    id = serializers.SerializerMethodField()
    images = serializers.SerializerMethodField()
    image = serializers.SerializerMethodField()
    amenities = serializers.SerializerMethodField()
    selling_points = serializers.SerializerMethodField()
    landmarks = serializers.SerializerMethodField()
    features = serializers.SerializerMethodField()

    category = serializers.PrimaryKeyRelatedField(queryset=Category.objects.all())
    subcategory = serializers.CharField(required=False, allow_null=True, allow_blank=True)
    purpose = serializers.CharField()

    class Meta:
        model = AgentProperty
        fields = "__all__"
        read_only_fields = ["agent", "phone", "whatsapp"]

    def get_id(self, obj):
        return encode_id(obj.id)

    # ================= FK HANDLER =================
    def handle_foreign_keys(self, validated_data):

        subcategory_name = self.initial_data.get("subcategory")
        if subcategory_name:
            subcategory = Subcategory.objects.filter(
                name__iexact=subcategory_name.strip()
            ).first()
            if not subcategory:
                raise serializers.ValidationError({"subcategory": "Invalid subcategory"})
            validated_data["subcategory"] = subcategory

        purpose_name = self.initial_data.get("purpose")
        if purpose_name:
            purpose = Purpose.objects.filter(
                name__iexact=purpose_name.strip()
            ).first()
            if not purpose:
                raise serializers.ValidationError({"purpose": "Invalid purpose"})
            validated_data["purpose"] = purpose

        return validated_data

    # ================= CREATE =================
    def create(self, validated_data):
        request = self.context["request"]
        agent = request.user

        validated_data = self.handle_foreign_keys(validated_data)

        instance = AgentProperty.objects.create(
            agent=agent,
            phone=agent.phone_number,
            whatsapp=agent.whatsapp_number,
            **validated_data
        )

        self.handle_related_fields(instance)
        return instance

    # ================= UPDATE =================
    def update(self, instance, validated_data):

        validated_data = self.handle_foreign_keys(validated_data)
        instance = super().update(instance, validated_data)

        self.handle_related_fields(instance)
        return instance

    # ================= RELATED HANDLER =================
    def handle_related_fields(self, instance):

        amenities_list = self.context.get("amenities_list", [])
        selling_points_list = self.context.get("selling_points_list", [])
        landmarks_list = self.context.get("landmarks_list", [])
        field_values = self.context.get("field_values", [])

        # -------- AMENITIES --------
        if amenities_list:
            instance.amenities.set(amenities_list)

        # -------- SELLING POINTS --------
        if selling_points_list:
            instance.selling_points.all().delete()
            AgentPropertySellingPoint.objects.bulk_create([
                AgentPropertySellingPoint(property=instance, point=sp)
                for sp in selling_points_list
            ])

        # -------- LANDMARKS --------
        if landmarks_list:
            instance.landmarks.all().delete()
            AgentPropertyLandmark.objects.bulk_create([
                AgentPropertyLandmark(
                    property=instance,
                    name=lm.get("name"),
                    distance=lm.get("distance")
                )
                for lm in landmarks_list if isinstance(lm, dict)
            ])

        # -------- FEATURES (FINAL LOGIC) --------
        if field_values:

            for fv in field_values:
                if not isinstance(fv, dict):
                    raise serializers.ValidationError("Invalid field_values format")

                field_name = fv.get("name")       # flat furnishings / bhk type
                option_name = fv.get("option")   # Wardrobe / TV
                value = fv.get("value")          # 3 / 1 / "3 bhk"

                if not field_name:
                    raise serializers.ValidationError("Feature name missing")

                field = SubcategoryField.objects.filter(
                    subcategory=instance.subcategory,
                    field_name__iexact=field_name.strip()
                ).first()

                if not field:
                    raise serializers.ValidationError(f"Invalid feature: {field_name}")

                # -------- OPTION BASED FIELD --------
                if option_name:
                    option = FieldOption.objects.filter(
                        name__iexact=option_name.strip(),
                        field=field
                    ).first()

                    if not option:
                        raise serializers.ValidationError(f"Invalid option: {option_name}")

                    try:
                        value = int(value)
                    except:
                        raise serializers.ValidationError(f"{option_name} must be a number")

                    # remove existing same option
                    AgentPropertyFieldValue.objects.filter(
                        property=instance,
                        field=field,
                        value__icontains=f'"option": "{option.name}"'
                    ).delete()

                    # save JSON
                    AgentPropertyFieldValue.objects.create(
                        property=instance,
                        field=field,
                        value=json.dumps({
                            "option": option.name,
                            "count": value
                        })
                    )

                # -------- NORMAL FIELD --------
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

    # ================= CLEAN RESPONSE =================
    def get_features(self, obj):
        result = {}

        for fv in obj.field_values.select_related("field"):
            field = fv.field

            # -------- TRY NEW JSON STRUCTURE --------
            try:
                data = json.loads(fv.value)

                option = data.get("option")
                count = data.get("count", 0)

                if option:
                    result[option] = count
                    continue

            except Exception:
                pass

            # -------- SKIP OLD BROKEN DATA --------
            if field.field_name.lower() == "flat furnishings":
                continue

            # -------- NORMAL FIELD --------
            if field.field_type == "countable":
                try:
                    value = int(fv.value)
                except:
                    value = 0
            else:
                value = fv.value

            result[field.field_name] = value

        return [
            {"name": k, "value": v}
            for k, v in result.items()
        ]

    # ================= OTHER =================
    def get_images(self, obj):
        return [img.image.url for img in obj.images.all() if img.image]

    def get_image(self, obj):
        return obj.image.url if obj.image else None

    def get_amenities(self, obj):
        return [{"id": a.id, "name": a.name} for a in obj.amenities.all()]

    def get_selling_points(self, obj):
        return list(obj.selling_points.values_list("point", flat=True))

    def get_landmarks(self, obj):
        return [{"name": l.name, "distance": l.distance} for l in obj.landmarks.all()]
    
    
class AgentPropertyEnquirySerializer(serializers.ModelSerializer):

    class Meta:
        model = AgentPropertyEnquiry
        fields = "__all__"
        read_only_fields = ["user", "agent_property"]



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


from .utils import hashids

class PropertyCardSerializer(serializers.ModelSerializer):
        id = serializers.SerializerMethodField()  # 👈 override ID
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

        # ✅ Masked ID
        def get_id(self, obj):
            return hashids.encode(obj.id)

        # ✅ Optimized images
        def get_images(self, obj):
            return [
                img.image.url
                for img in obj.images.all()[:2]
                if img.image
            ]

        # ✅ Wishlist check
        def get_is_wishlisted(self, obj):
            wishlist_ids = self.context.get("wishlist_ids", set())
            return obj.id in wishlist_ids

class WishlistSerializer(serializers.ModelSerializer):
        id = serializers.SerializerMethodField()  # 👈 masked id
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

        def get_id(self, obj):
            return hashids.encode(obj.id)

        def get_images(self, obj):
            return [
                img.image.url
                for img in obj.images.all()[:2]
                if img.image
            ]

        def get_is_wishlisted(self, obj):
            return True  # 👈 since it's wishlist






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
    




from rest_framework import serializers
from .models import Property
from .utils import hashids


class PropertyDetailSerializer(serializers.ModelSerializer):

    # -----------------------------
    # CUSTOM FIELDS
    # -----------------------------
    id = serializers.SerializerMethodField()
    images = serializers.SerializerMethodField()

    purpose = serializers.SerializerMethodField()
    category = serializers.SerializerMethodField()
    # subcategory = serializers.SerializerMethodField()

    created_at = serializers.DateTimeField(
        format="%Y-%m-%d"
    )

    property_features = serializers.SerializerMethodField()
    price_details = serializers.SerializerMethodField()
    contact_details = serializers.SerializerMethodField()
    owner_profile_image = serializers.SerializerMethodField()
    amenities = serializers.SerializerMethodField()

    # ✅ NEW (ONLY ADDITION)
    key_selling_points = serializers.SerializerMethodField()
    land_mark = serializers.SerializerMethodField()
    location_details = serializers.SerializerMethodField()

    # -----------------------------
    # META
    # -----------------------------
    class Meta:
        model = Property
        fields = [
            "id",
            "property_code",
            "label",
            "images",
            "purpose",
            "category",
            # "subcategory",
            "description",
            "city",
            "state",
            "location",
            "land_mark",           # ✅ list output
            "created_at",
            "property_features",
            "price_details",
            "contact_details",
            "owner_profile_image",
            "amenities",
            "key_selling_points",  # ✅ added
            "location_details",
        ]

    def get_owner_profile_image(self, obj):

        if not obj.owner:
            return None

        owner = obj.owner

        # --------------------------------
        # 1. Uploaded profile image
        # --------------------------------
        try:
            if hasattr(owner, "profile") and owner.profile:

                profile = owner.profile

                if profile.image:
                    image_val = str(profile.image)

                    # ignore old default vector placeholder
                    if (
                        image_val and
                        "Vector_te4oj7" not in image_val
                    ):
                        try:
                            return profile.image.url
                        except Exception:
                            pass

        except Exception:
            pass


        # --------------------------------
        # 2. Fallback initials avatar
        # --------------------------------
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


    # --------------------------------------------------
    # LOCATION DETAILS (NEW FIELD)
    # --------------------------------------------------
    def get_location_details(self, obj):
        return {
            "village": obj.village,
            "city": obj.city,
            "state": obj.state,
            "pincode": obj.pincode,
        }

    # --------------------------------------------------
    # HASHED ID
    # --------------------------------------------------
    def get_id(self, obj):
        return hashids.encode(obj.id)

    # --------------------------------------------------
    # MULTIPLE PROPERTY IMAGES
    # --------------------------------------------------
    def get_images(self, obj):
        request = self.context.get("request")

        images = []

        for img in obj.images.all():
            if img.image:
                url = img.image.url
                if request:
                    url = request.build_absolute_uri(url)
                images.append(url)

        return images

    # --------------------------------------------------
    # PURPOSE
    # --------------------------------------------------
    def get_purpose(self, obj):
        return obj.purpose.name if obj.purpose else None

    # --------------------------------------------------
    # CATEGORY WITH IMAGE
    # --------------------------------------------------
    def get_category(self, obj):
        request = self.context.get("request")

        if not obj.category:
            return None

        image_url = None
        if getattr(obj.category, "image", None):
            image_url = obj.category.image.url
            if request:
                image_url = request.build_absolute_uri(image_url)

        return {
            "id": obj.category.id,
            "name": obj.category.name,
            "image": image_url,
        }

    # --------------------------------------------------
    # SUBCATEGORY + FIELD ICONS
    # --------------------------------------------------
    # def get_subcategory(self, obj):
    #     request = self.context.get("request")

    #     if not obj.subcategory:
    #         return None

    #     fields = []

    #     for field in obj.subcategory.fields.all():
    #         icon_url = None
    #         if field.icon:
    #             icon_url = field.icon.url
    #             if request:
    #                 icon_url = request.build_absolute_uri(icon_url)

    #         fields.append({
    #             "id": field.id,
    #             "field_name": field.field_name,
    #             "field_type": field.field_type,
    #             "required": field.required,
    #             "icon": icon_url,
    #         })

    #     return {
    #         "id": obj.subcategory.id,
    #         "name": obj.subcategory.name,
    #         "fields": fields,
    #     }

    # --------------------------------------------------
    # PROPERTY FEATURES
    # --------------------------------------------------
    # def get_property_features(self, obj):
    #     """
    #     Return subcategory field definitions
    #     + property dynamic field values
    #     """

    #     if not obj.subcategory:
    #         return []

    #     request = self.context.get("request")
    #     dynamic_data = obj.dynamic_fields or {}
        

    #     features = []

    #     for field in obj.subcategory.fields.all():
    #         raw_value = dynamic_data.get(field.field_name)

    #         icon_url = None
    #         if field.icon:
    #             icon_url = field.icon.url
    #             if request:
    #                 icon_url = request.build_absolute_uri(icon_url)

    #         features.append({
    #             # "id": field.id,
    #             "field_name": field.field_name,
    #             # "field_type": field.field_type,
    #             # "required": field.required,
    #             "icon": icon_url,
    #             "value": raw_value.get("value") if isinstance(raw_value, dict) else raw_value
    #         })

    #     return features


    def get_property_features(self, obj):

        if not obj.subcategory:
            return []

        request = self.context.get("request")
        dynamic_data = obj.dynamic_fields or {}

        features = []

        fields_qs = getattr(obj.subcategory, "fields", None)   # ✅ FIX

        if not fields_qs:   # ✅ FIX
            return []

        for field in fields_qs.all():   # ✅ FIX
            raw_value = dynamic_data.get(field.field_name)

            icon_url = None
            if field.icon:
                icon_url = field.icon.url
                if request:
                    icon_url = request.build_absolute_uri(icon_url)

            features.append({
                "field_name": field.field_name,
                "icon": icon_url,
                "value": raw_value.get("value") if isinstance(raw_value, dict) else raw_value
            })

        return features

    # --------------------------------------------------
    # ✅ KEY SELLING POINTS (LIST)
    # --------------------------------------------------
    def get_key_selling_points(self, obj):
        return obj.key_selling_points or []

    # --------------------------------------------------
    # ✅ LANDMARKS (LIST)
    # --------------------------------------------------
    def get_land_mark(self, obj):
        return obj.land_mark or []

    # --------------------------------------------------
    # PRICE DETAILS
    # --------------------------------------------------
    def get_price_details(self, obj):
        return {
            "price": obj.price,
            "sq_ft": obj.sq_ft,
            "land_area": obj.land_area,
            "perprice": obj.perprice,
        }

    # --------------------------------------------------
    # CONTACT DETAILS
    # --------------------------------------------------
    def get_contact_details(self, obj):
        return {
            "owner": getattr(obj.owner, "name", str(obj.owner)),
            "whatsapp": obj.whatsapp,
            "phone": obj.phone,
        }

    # --------------------------------------------------
    # AMENITIES
    # --------------------------------------------------
    # def get_amenities(self, obj):
    #     request = self.context.get("request")

    #     amenities_data = []

    #     for amenity in obj.amenities.all():
    #         icon_url = None

    #         if amenity.icon:
    #             icon_url = amenity.icon.url
    #             if request:
    #                 icon_url = request.build_absolute_uri(icon_url)

    #         amenities_data.append({
    #             "name": amenity.name,
    #             "icon": icon_url
    #         })
    #     return amenities_data
    def get_amenities(self, obj):
        request = self.context.get("request")

        amenities_data = []

        amenities = obj.amenities.all()

        if not amenities.exists():
            return []

        for amenity in amenities:
            icon_url = None

            try:
                if getattr(amenity, "icon", None):
                    icon_url = amenity.icon.url

                    if request:
                        icon_url = request.build_absolute_uri(
                            icon_url
                        )
            except Exception:
                icon_url = None

            amenities_data.append({
                # "id": amenity.id,
                "name": amenity.name,
                "icon": icon_url
            })

        return amenities_data

    

from rest_framework import serializers
from .models import PropertyEnquiry, Property
from .utils import decode_id


from rest_framework import serializers
from .models import PropertyEnquiry




class PropertyEnquirySerializer(serializers.ModelSerializer):

    class Meta:
        model = PropertyEnquiry
        fields = [
            "id",
            "property_hash_id",
            "name",
            "phone",
            "email",
            "messagebox",
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



from rest_framework import serializers
from .models import UserProfile, UserCreate


class UserProfileUpdateSerializer(serializers.Serializer):

    full_name = serializers.CharField(required=False)
    email = serializers.EmailField(required=False)
    mobile = serializers.CharField(required=False)
    alternate_mobile = serializers.CharField(required=False)
    city = serializers.CharField(required=False)

    def update(self, user, validated_data):

        profile = user.profile

        # ❌ BLOCK EMAIL CHANGE
        if "email" in validated_data:
            new_email = validated_data["email"]

            if new_email != user.email:
                raise serializers.ValidationError({
                    "email": "Email cannot be changed once registered."
                })

        # ✅ UPDATE FIELDS ONLY IF PASSED
        if "full_name" in validated_data:
            profile.full_name = validated_data["full_name"]

        if "mobile" in validated_data and validated_data["mobile"].strip():
            profile.mobile = validated_data["mobile"]
            user.mobile = validated_data["mobile"]
            user.save(update_fields=["mobile"])

        if "alternate_mobile" in validated_data:
            profile.alternate_mobile = validated_data["alternate_mobile"]

        if "city" in validated_data:
            profile.city = validated_data["city"]

        profile.save()

        return profile



class MyActivitySerializer(serializers.Serializer):

    wishlist_count = serializers.IntegerField()
    enquiries_count = serializers.IntegerField()
    properties_listed_count = serializers.IntegerField()
    viewed_properties_count = serializers.IntegerField()



class SliderBannerSerializer(serializers.ModelSerializer):
    image = serializers.SerializerMethodField()

    class Meta:
        model = SliderBannerAd
        fields = ['id', 'image']

    def get_image(self, obj):
        if obj.image:
            return obj.image.url   
        return None
    

from rest_framework import serializers
from .models import HeroImage

class HeroImageSerializer(serializers.ModelSerializer):
    image = serializers.SerializerMethodField()

    class Meta:
        model = HeroImage
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
            "messagebox",
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