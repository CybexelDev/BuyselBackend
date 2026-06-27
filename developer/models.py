from django.db import models,transaction
import uuid
from cloudinary.models import CloudinaryField
import cloudinary.uploader
from playwright.sync_api import sync_playwright
import time
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import AbstractUser
import string
from django.utils import timezone
from datetime import timedelta
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey

import random
from django.utils.text import slugify
from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import AbstractUser

from django.db import models
from django.contrib.auth.models import AbstractUser

from .validators import *


class CustomUser(AbstractUser):
    rate_limit = models.IntegerField(
        default=0,
        validators=[validate_rate_limit]
    )

    last_failed_login = models.DateTimeField(
        null=True,
        blank=True
    )

    def save(self, *args, **kwargs):
        self.full_clean()  
        super().save(*args, **kwargs)

class AgentForm(models.Model):
    name = models.CharField(
        max_length=100,
        validators=[validate_agent_name]
    )

    email = models.EmailField(
        max_length=50,
        null=True,
        blank=True
    )

    address = models.TextField()

    phone_number = models.CharField(
        max_length=12,
        validators=[validate_phone_number]
    )

    category = models.CharField(
        max_length=100,
        validators=[validate_category]
    )

    image = CloudinaryField('image', folder="agentreg")

    created_at = models.DateTimeField(auto_now_add=True)

    def clean(self):
        if self.address and len(self.address.strip()) < 10:
            raise ValidationError("Address must be at least 10 characters long.")

    def save(self, *args, **kwargs):
        self.full_clean()  # runs all validation
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name


class Propertylist(models.Model):

    categories = models.CharField(
        max_length=100,
        validators=[validate_text_min_3]
    )

    purposes = models.CharField(
        max_length=100,
        validators=[validate_text_min_3]
    )

    label = models.CharField(
        max_length=100,
        validators=[validate_text_min_3]
    )

    land_area = models.CharField(
        max_length=100,
        null=True,
        blank=True
    )

    description = models.CharField(
        max_length=500
    )

    sq_ft = models.CharField(
        max_length=100
    )

    amenities = models.CharField(
        max_length=500,
        null=True,
        blank=True
    )

    owner = models.CharField(
        max_length=100,
        validators=[validate_text_min_3]
    )

    locations = models.CharField(
        max_length=100,
        validators=[validate_text_min_3]
    )

    price = models.CharField(
        max_length=50
    )

    about_the_property = models.TextField()

    pin_code = models.CharField(
        max_length=8,
        validators=[validate_pincode]
    )

    land_mark = models.CharField(
        max_length=100
    )

    phone = models.CharField(
        max_length=15,
        validators=[validate_phone_number]
    )

    image = models.ImageField(
        upload_to='property-image'
    )

    total_price = models.CharField(
        max_length=15
    )

    duration = models.CharField(
        max_length=100
    )

    whatsapp = models.CharField(
        max_length=15,
        validators=[validate_phone_number]
    )

    city = models.CharField(max_length=100)
    District = models.CharField(max_length=100)

    taluk = models.CharField(
        max_length=100,
        null=True,
        blank=True
    )

    village = models.CharField(
        max_length=100,
        null=True,
        blank=True
    )

    state = models.CharField(
        max_length=100,
        null=True,
        blank=True
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    def clean(self):
        if self.about_the_property and len(self.about_the_property.strip()) < 10:
            raise ValidationError("Property description must be at least 10 characters.")

    def save(self, *args, **kwargs):
        self.full_clean()  # enforce validation
        super().save(*args, **kwargs)

    def __str__(self):
        return self.categories


class Blog(models.Model):
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False
    )

    category = models.ForeignKey(
        "Category",
        on_delete=models.CASCADE,
        related_name="blogs",
        blank=True,
        null=True
    )

    blog_head = models.CharField(
        max_length=100,
        validators=[validate_blog_title]
    )

    date = models.DateField()

    card_paragraph = models.TextField(
        validators=[validate_blog_content]
    )

    image = CloudinaryField(
        'image',
        folder="blog"
    )

    def clean(self):
        if not self.blog_head:
            raise ValidationError("Blog title cannot be empty.")

        if not self.card_paragraph:
            raise ValidationError("Blog content cannot be empty.")

    def save(self, *args, **kwargs):
        self.full_clean()  
        super().save(*args, **kwargs)

    def __str__(self):
        return self.blog_head


class Premium(models.Model):

    name = models.CharField(max_length=100)

    speacialised = models.CharField(max_length=100)

    phone = models.CharField(
        max_length=15,
        validators=[validate_phone_number]
    )

    whatsapp = models.CharField(
        max_length=15,
        blank=True,
        null=True,
        validators=[validate_phone_number]
    )

    email = models.EmailField(
        max_length=100,
        blank=True,
        null=True
    )

    location = models.CharField(max_length=200)
    city = models.CharField(max_length=100)

    pincode = models.CharField(
        max_length=6,
        validators=[validate_pincode]
    )

    username = models.CharField(
        max_length=100,
        validators=[validate_username]
    )

    password = models.CharField(
        max_length=100,
        validators=[validate_password]
    )

    image = CloudinaryField(
        'buysel',
        folder="premium_agents"
    )

    created_at = models.DateTimeField(
        default=timezone.now
    )

    duration_days = models.PositiveIntegerField(
        default=365,
        db_index=True
    )

    # ------------------------
    def is_expired(self):
        try:
            return int(self.duration_days) <= 0
        except (TypeError, ValueError):
            return False

    # ------------------------
    def clean(self):
        if self.name and len(self.name.strip()) < 3:
            raise ValidationError("Name must be at least 3 characters long.")

        if self.speacialised and len(self.speacialised.strip()) < 3:
            raise ValidationError("Specialisation must be valid.")

    # ------------------------
    def save(self, *args, **kwargs):
        self.full_clean()  # enforce validation

        if self.pk and self.is_expired():
            expired = ExpiredPremium.objects.create(
                name=self.name,
                speacialised=self.speacialised,
                phone=self.phone,
                whatsapp=self.whatsapp,
                email=self.email,
                location=self.location,
                city=self.city,
                pincode=self.pincode,
                username=self.username,
                password=self.password,
                image=self.image,
                created_at=self.created_at,
                duration_days=self.duration_days,
            )

            for img in self.images.all():
                PremiumImage.objects.create(
                    expired_premium=expired,
                    image=img.image
                )

            super().delete()
            return

        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.name} (Active)"

class ExpiredPremium(models.Model):

    name = models.CharField(max_length=100)

    speacialised = models.CharField(max_length=100)

    phone = models.CharField(
        max_length=15,
        validators=[validate_phone_number]
    )

    whatsapp = models.CharField(
        max_length=15,
        blank=True,
        null=True,
        validators=[validate_phone_number]
    )

    email = models.EmailField(
        max_length=100,
        blank=True,
        null=True
    )

    location = models.CharField(max_length=200)
    city = models.CharField(max_length=100)

    pincode = models.CharField(
        max_length=6,
        validators=[validate_pincode]
    )

    username = models.CharField(
        max_length=100,
        validators=[validate_username]
    )

    password = models.CharField(max_length=100,validators=[validate_password])

    image = CloudinaryField(
        'buysel',
        folder="premium_agents"
    )

    created_at = models.DateTimeField()
    duration_days = models.PositiveIntegerField()

    # ------------------------
    def is_active_again(self):
        try:
            return int(self.duration_days) > 0
        except (TypeError, ValueError):
            return False

    # ------------------------
    def clean(self):
        if self.name and len(self.name.strip()) < 3:
            raise ValidationError("Name must be at least 3 characters long.")

        if self.speacialised and len(self.speacialised.strip()) < 3:
            raise ValidationError("Specialisation must be valid.")

    # ------------------------
    def save(self, *args, **kwargs):
        self.full_clean()  # enforce validation

        if self.pk and self.is_active_again():
            active = Premium.objects.create(
                name=self.name,
                speacialised=self.speacialised,
                phone=self.phone,
                whatsapp=self.whatsapp,
                email=self.email,
                location=self.location,
                city=self.city,
                pincode=self.pincode,
                username=self.username,
                password=self.password,
                image=self.image,
                created_at=self.created_at,
                duration_days=self.duration_days,
            )

            for img in self.images.all():
                PremiumImage.objects.create(
                    premium=active,
                    image=img.image
                )

            super().delete()
            return

        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.name} (Expired)"


# class PremiumImage(models.Model):
#     premium = models.ForeignKey(
#         Premium,
#         on_delete=models.CASCADE,
#         related_name="images",
#         null=True,
#         blank=True
#     )
#     expired_premium = models.ForeignKey(
#         ExpiredPremium,
#         on_delete=models.CASCADE,
#         related_name="images",
#         null=True,
#         blank=True
#     )

#     image = CloudinaryField("image", folder="premium/multiple")

#     def __str__(self):
#         if self.premium:
#             return f"Image for {self.premium.name}"
#         if self.expired_premium:
#             return f"Expired image for {self.expired_premium.name}"
#         return "Orphan image"


class PremiumImage(models.Model):

    premium = models.ForeignKey(
        "Premium",
        on_delete=models.CASCADE,
        related_name="images",
        null=True,
        blank=True
    )

    expired_premium = models.ForeignKey(
        "ExpiredPremium",
        on_delete=models.CASCADE,
        related_name="images",
        null=True,
        blank=True
    )

    image = CloudinaryField(
        "image",
        folder="premium/multiple"
    )

    def clean(self):
        # must belong to one side only
        if not self.premium and not self.expired_premium:
            raise ValidationError("Image must be linked to premium or expired premium.")

        if self.premium and self.expired_premium:
            raise ValidationError("Image cannot belong to both premium and expired premium.")

    def __str__(self):
        if self.premium:
            return f"Image for {self.premium.name}"
        if self.expired_premium:
            return f"Expired image for {self.expired_premium.name}"
        return "Orphan image"



class Contact(models.Model):

    name = models.CharField(
        max_length=100,
        validators=[validate_text_min_3]
    )

    email = models.CharField(
        max_length=100,
        null=True,
        blank=True,
        validators=[validate_email]
    )

    phone = models.CharField(
        max_length=14,
        validators=[validate_phone_number]
    )

    message = models.CharField(
        max_length=500,
        validators=[validate_safe_message]
    )

    created_at = models.DateTimeField(auto_now_add=True)

    def clean(self):
        if self.email and "@" not in self.email:
            raise ValidationError("Invalid email format.")

        if len(self.message.strip()) < 10:
            raise ValidationError("Message must be at least 10 characters long.")

    def __str__(self):
        return self.name
    
class Request(models.Model):

    name = models.CharField(
        max_length=100,
        validators=[validate_agent_name]
    )

    email = models.CharField(
        max_length=100,
        null=True,
        blank=True,
        validators=[validate_email]
    )

    phone = models.CharField(
        max_length=15,
        validators=[validate_phone_number]
    )

    message = models.CharField(
        max_length=1000,
        null=True,
        blank=True,
        validators=[validate_safe_message]
    )

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

class Blogadmin(models.Model):

    username = models.CharField(
        max_length=100,
        validators=[validate_username]
    )

    password = models.CharField(
        max_length=100,
        validators=[validate_password]
    )

    def __str__(self):
        return self.username



class Budget(models.Model):

    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False
    )

    value = models.CharField(
        max_length=100,
        validators=[validate_budget]
    )

    created_at = models.DateTimeField(auto_now_add=True,null=True,blank=True)

    def __str__(self):
        return self.value
    
# class Budget(models.Model):

#     value = models.CharField(
#         max_length=100,
#         validators=[validate_budget]
#     )

#     def __str__(self):
#         return self.value

class UserCreate(models.Model):

    USER_ROLES = (
        ("user", "User"),
        ("owner", "Owner"),
    )

    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
        db_index=True
    )

    name = models.CharField(
        max_length=100,
        validators=[validate_username]
    )

    email = models.EmailField(unique=True)

    mobile = models.CharField(
        max_length=12,
        blank=True,
        null=True,
        validators=[validate_phone_number]
    )

    password = models.CharField(
        blank=True,
        null=True,
        max_length=128,
        validators=[validate_password]
    )

    role = models.CharField(
        max_length=10,
        choices=USER_ROLES,
        default="user"
    )

    otp = models.CharField(
        max_length=6,
        null=True,
        blank=True
    )

    otp_created_at = models.DateTimeField(
        null=True,
        blank=True
    )

    reset_token = models.UUIDField(
        null=True,
        blank=True,
        unique=True
    )

    is_verified = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True)

    paid_property_count = models.PositiveIntegerField(default=0)

    last_plan_expiry = models.DateTimeField(
        null=True,
        blank=True
    )

    user_plans = models.ManyToManyField(
        "Userplan",
        blank=True,
        related_name="users"
    )

    @property
    def is_authenticated(self):
        return True

    def generate_otp(self):
        return str(random.randint(100000, 999999))

    def update_role(self):

        has_property = self.properties.exists()

        has_plan = self.user_plans.exists()

        if has_property or has_plan:
            self.role = "owner"
        else:
            self.role = "user"

    def clean(self):

        if self.email:
            self.email = self.email.lower().strip()

    def save(self, *args, **kwargs):

        self.full_clean()

        has_property = (
            self.properties.exists()
            if self.pk else False
        )

        has_plan = (
            self.user_plans.exists()
            if self.pk else False
        )

        # AUTO ROLE
        if has_property or has_plan:
            self.role = "owner"
        else:
            self.role = "user"

        super().save(*args, **kwargs)

        # CREATE PROFILE
        profile, created = UserProfile.objects.get_or_create(
            user=self
        )

        # LATEST USER PLAN
        if self.user_plans.exists():

            latest_plan = self.user_plans.last()

            profile.user_plan = latest_plan

        else:

            profile.user_plan = None

        # PAID STATUS
        profile.is_paid_user = bool(
            profile.user_plan
        )

        # ROLE
        profile.user_role = self.role

        profile.save()

    def __str__(self):

        return f"{self.email} - {self.role}"    


class PasswordResetToken(models.Model):

    user = models.ForeignKey(
        "UserCreate",
        on_delete=models.CASCADE,
        related_name="reset_tokens"
    )

    # Secure UUID token
    token = models.UUIDField(
        default=uuid.uuid4,
        unique=True,
        editable=False
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    expires_at = models.DateTimeField(
        null=True,
        blank=True
    )

    def clean(self):
        if self.user and self.user.email:
            validate_email(self.user.email)


        if self.expires_at and self.expires_at < timezone.now():
            raise ValidationError("Expiry time cannot be in the past.")

    
    def save(self, *args, **kwargs):

        self.full_clean()

        if not self.expires_at:
            self.expires_at = timezone.now() + timedelta(minutes=10)

        super().save(*args, **kwargs)

    def is_expired(self):
        return timezone.now() > self.expires_at

    def __str__(self):
        return f"{self.user.email} - reset token"

class UserProfile(models.Model):

    AUTH_PROVIDERS = (
        ('mobile', 'Mobile'),
        ('google', 'Google'),
        ('facebook', 'Facebook'),
    )

    USER_ROLES = (
        ("user", "User"),
        ("owner", "Owner"),
    )

    user = models.OneToOneField(
        "UserCreate",
        on_delete=models.CASCADE,
        related_name="profile"
    )

    custom_user_id = models.CharField(
        max_length=30,
        unique=True,
        blank=True
    )

    username = models.CharField(
        max_length=150,
        unique=True,
        blank=True
    )

    full_name = models.CharField(
        max_length=150,
        blank=True
    )

    mobile = models.CharField(
        max_length=15,
        blank=True,
        validators=[validate_phone_number]
    )

    city = models.CharField(
        max_length=200,
        blank=True,
        default=""
    )

    alternate_mobile = models.CharField(
        max_length=15,
        blank=True,
        validators=[validate_phone_number]
    )

    image = CloudinaryField(
        "image",
        folder="buysel/profile_images",
        blank=True,
        null=True
    )

    user_role = models.CharField(
        max_length=10,
        choices=USER_ROLES,
        default="user"
    )

    user_plan = models.ForeignKey(
        "Userplan",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="user_profiles"
    )

    is_paid_user = models.BooleanField(
        default=False
    )

    # =====================================================
    # PROPERTY USAGE TRACKING
    # NEVER REDUCE THESE COUNTS
    # =====================================================

    total_property_used = models.IntegerField(
        default=0
    )

    residential_property_used = models.IntegerField(
        default=0
    )

    commercial_property_used = models.IntegerField(
        default=0
    )

    # =====================================================

    plan_start_date = models.DateTimeField(
        null=True,
        blank=True
    )

    plan_expiry_date = models.DateTimeField(
        null=True,
        blank=True
    )

    auth_provider = models.CharField(
        max_length=20,
        choices=AUTH_PROVIDERS,
        default="mobile"
    )

    is_active = models.BooleanField(
        default=True
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    # =====================================================
    # CLEAN
    # =====================================================

    def clean(self):

        for field in [
            self.username,
            self.full_name,
            self.city
        ]:

            if field and "<script" in field.lower():

                raise ValidationError(
                    "Invalid content detected."
                )

    # =====================================================
    # GENERATE CUSTOM ID
    # =====================================================

    def generate_custom_user_id(self):

        base = (
            self.username or "user"
        )[:4].lower()

        nums = ''.join(
            random.choices(
                string.digits,
                k=4
            )
        )

        return f"buysel{base}{nums}"

    # =====================================================
    # ACTIVE PLAN
    # =====================================================

    @property
    def has_active_plan(self):

        if not self.plan_expiry_date:
            return False

        return (
            timezone.now()
            <= self.plan_expiry_date
        )

    # =====================================================
    # CURRENT PLAN TYPE
    # =====================================================

    @property
    def current_plan_type(self):

        if self.user_plan:
            return "plan"

        return None

    # =====================================================
    # USER ROLE UPDATE
    # =====================================================

    def update_user_role(self):

        user = self.user

        has_property = user.properties.exists()

        has_plan = (
            self.user_plan is not None
        )

        if has_property or has_plan:

            self.user_role = "owner"

            if user.role != "owner":

                user.role = "owner"

                user.save(
                    update_fields=["role"]
                )

        else:

            self.user_role = "user"

            if user.role != "user":

                user.role = "user"

                user.save(
                    update_fields=["role"]
                )

    # =====================================================
    # ACTIVATE PLAN
    # =====================================================

    def activate_user_plan(self, plan):

        self.user_plan = plan

        self.is_paid_user = True

        self.plan_start_date = timezone.now()

        self.plan_expiry_date = (
            timezone.now()
            + timedelta(days=int(plan.validity))
        )

        self.save()

    # =====================================================
    # CHECK PLAN EXPIRY
    # =====================================================

    def check_plan_expiry(self):

        if (
            self.plan_expiry_date
            and timezone.now()
            > self.plan_expiry_date
        ):

            self.user_plan = None

            self.is_paid_user = False

            self.plan_start_date = None

            self.plan_expiry_date = None

            self.save()

    # =====================================================
    # SAVE
    # =====================================================

    def save(self, *args, **kwargs):

        self.full_clean()

        # =================================================
        # USERNAME
        # =================================================

        if (
            not self.username
            and self.user.email
        ):

            base = slugify(
                self.user.email.split("@")[0]
            )

            username = base

            count = 1

            while UserProfile.objects.filter(
                username=username
            ).exclude(pk=self.pk).exists():

                username = f"{base}{count}"

                count += 1

            self.username = username

        # =================================================
        # CUSTOM USER ID
        # =================================================

        if not self.custom_user_id:

            cid = self.generate_custom_user_id()

            while UserProfile.objects.filter(
                custom_user_id=cid
            ).exists():

                cid = self.generate_custom_user_id()

            self.custom_user_id = cid

        # =================================================
        # FULL NAME
        # =================================================

        if not self.full_name:

            self.full_name = self.user.name

        # =================================================
        # PAID USER
        # =================================================

        self.is_paid_user = bool(
            self.user_plan
        )

        # =================================================
        # USER ROLE
        # =================================================

        has_property = self.user.properties.exists()

        has_plan = (
            self.user_plan is not None
        )

        if has_property or has_plan:

            self.user_role = "owner"

        else:

            self.user_role = "user"

        # =================================================
        # SAFETY FOR OLD USERS
        # =================================================

        if self.total_property_used is None:
            self.total_property_used = 0

        if self.residential_property_used is None:
            self.residential_property_used = 0

        if self.commercial_property_used is None:
            self.commercial_property_used = 0

        super().save(*args, **kwargs)

        self.update_user_role()

    # =====================================================
    # INITIALS
    # =====================================================

    @property
    def initials(self):

        name = (
            self.full_name
            or self.user.name
            or self.username
            or "User"
        ).strip()

        words = name.split()

        if len(words) >= 2:

            return (
                words[0][0]
                + words[1][0]
            ).upper()

        return name[:2].upper()

    # =====================================================
    # PROFILE IMAGE
    # =====================================================

    @property
    def profile_image_url(self):

        if self.image:

            try:

                img = str(self.image)

                if (
                    img
                    and "Vector_te4oj7"
                    not in img
                ):

                    return self.image.url

            except:
                pass

        return (
            "https://ui-avatars.com/api/"
            f"?name={self.initials}"
            "&background=8bc83f"
            "&color=ffffff"
            "&size=256"
            "&bold=true"
        )

    # =====================================================
    # PROFILE COMPLETE
    # =====================================================

    @property
    def is_profile_complete(self):

        return all([
            self.username,
            self.full_name,
            self.mobile,
            self.city
        ])
    
    @property
    def active_subscription(self):

        subscriptions = self.user.subscriptions.filter(
            is_active=True
        ).select_related("plan")

        if not subscriptions.exists():
            return None

        return max(
            subscriptions,
            key=lambda x: (
                int(
                    re.findall(
                        r"\d+",
                        str(x.plan.property_listing_limit)
                    )[0]
                )
                if re.findall(
                    r"\d+",
                    str(x.plan.property_listing_limit)
                )
                else 999999
            )
        )

    @property
    def active_plan(self):

        sub = self.active_subscription

        if not sub:
            return None

        return sub.plan

    @property
    def remaining_property_limit(self):

        plan = self.active_plan

        if not plan:
            return 0

        nums = re.findall(
            r"\d+",
            str(plan.property_listing_limit)
        )

        limit = (
            int(nums[0])
            if nums
            else 999999
        )

        return max(
            limit - self.total_property_used,
            0
        )

    @property
    def remaining_residential_limit(self):

        plan = self.active_plan

        if not plan:
            return 0

        nums = re.findall(
            r"\d+",
            str(plan.property_listing_limit)
        )

        limit = (
            int(nums[0])
            if nums
            else 999999
        )

        return max(
            limit - self.residential_property_used,
            0
        )

    @property
    def remaining_commercial_limit(self):

        plan = self.active_plan

        if not plan:
            return 0

        nums = re.findall(
            r"\d+",
            str(plan.property_listing_limit)
        )

        limit = (
            int(nums[0])
            if nums
            else 999999
        )

        return max(
            limit - self.commercial_property_used,
            0
        )

    # =====================================================
    # STRING
    # =====================================================

    def __str__(self):

        return self.username

class Purpose(models.Model):
    name = models.CharField(
        max_length=50,
        unique=True,
        validators=[validate_safe_text]
    )

    def save(self, *args, **kwargs):
        self.full_clean()  
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name


from django.db import models
from cloudinary.models import CloudinaryField
from .validators import validate_safe_text


class Amenities(models.Model):
    name = models.CharField(
        max_length=100,
        validators=[validate_safe_text]
    )

    icon = CloudinaryField(
        "image",
        folder="buysel/amenities",
        blank=True,
        null=True
    )

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name


class Category(models.Model):
    name = models.CharField(
        max_length=50,
        unique=True,
        validators=[validate_safe_text]
    )

    icon = CloudinaryField(
        "icon",
        folder="category"
    )

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name


class Subcategory(models.Model):
    name = models.CharField(
        max_length=255,
        validators=[validate_safe_text]
    )

    category = models.ForeignKey(
        Category,
        on_delete=models.CASCADE
    )

    image = CloudinaryField(
        "icon",
        folder="subcategory"
    )

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name


class SubcategoryField(models.Model):

    FIELD_TYPES = (
        ("text", "Text"),
        ("number", "Number"),
        ("boolean", "Yes/No"),
        ("select", "Select"),
        ("multi_select", "Multi Select"),
        ("countable", "Countable"),
    )

    FIELD_UI = (
        ("dropdown", "Dropdown"),
        ("button_group", "Button Group"),
        ("checkbox", "Checkbox"),
    )

    subcategory = models.ForeignKey(
        Subcategory,
        on_delete=models.CASCADE
    )

    field_name = models.CharField(
        max_length=255,
        validators=[validate_safe_text]
    )

    field_type = models.CharField(
        max_length=50,
        choices=FIELD_TYPES
    )

    field_ui = models.CharField(
        max_length=50,
        choices=FIELD_UI,
        blank=True,
        null=True
    )

    required = models.BooleanField(default=False)

    icon = CloudinaryField(
        'icon',
        blank=True,
        null=True
    )

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)

    def __str__(self):
        return self.field_name


class FieldOption(models.Model):
    field = models.ForeignKey(
        SubcategoryField,
        on_delete=models.CASCADE,
        related_name="options"
    )

    name = models.CharField(
        max_length=100,
        validators=[validate_safe_text]
    )

    icon = CloudinaryField(
        'icon',
        blank=True,
        null=True
    )

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.field.field_name} - {self.name}"

class Subscription(models.Model):

    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False
    )

    plan_type = models.CharField(
        max_length=20,
        default="owner"
    )

    agent = models.ForeignKey(
        'agents.AgentUserProfile',
        on_delete=models.CASCADE,
        related_name='subscriptions'
    )

    plan_name = models.CharField(
        max_length=100
    )

    property_limit = models.IntegerField(
        default=0
    )

    used_listings = models.IntegerField(
        default=0
    )

    edit_limit = models.PositiveIntegerField(
        default=0
    )

    edit_used = models.PositiveIntegerField(
        default=0
    )

    featured_limit = models.PositiveIntegerField(
        default=0
    )

    featured_used = models.PositiveIntegerField(
        default=0
    )

    start_date = models.DateField(
        auto_now_add=True
    )

    end_date = models.DateField()

    is_active = models.BooleanField(
        default=True
    )

    def clean(self):

        # today = timezone.now().date()

        # if self.end_date <= today:

        #     raise ValidationError(
        #         "End date must be after today."
        #     )

        if self.used_listings > self.property_limit:

            raise ValidationError(
                "Used listings cannot exceed property limit."
            )
    def save(self, *args, **kwargs):

        self.plan_type = self.plan_type.lower()

        if self.end_date < timezone.now().date():
            self.is_active = False
        else:
            self.is_active = True

        self.full_clean()

        super().save(*args, **kwargs)

        # Sync Agent Profile after every subscription change
        self.agent.sync_subscription()
        
    # def save(self, *args, **kwargs):

    #     self.plan_type = "owner"

    #     if self.end_date < timezone.now().date():

    #         self.is_active = False

    #     self.full_clean()

    #     super().save(*args, **kwargs)

    def __str__(self):

        return (
            f"{self.agent} - "
            f"{self.plan_name}"
        )

# class Userupgrade(models.Model):

#     name = models.CharField(max_length=255)

#     validity = models.PositiveIntegerField(
#         help_text="Plan validity in days"
#     )

#     # Example: 2 Residential / 1 Commercial
#     listing = models.CharField(
#         max_length=255,
#         help_text="Example: 2 Residential / 1 Commercial"
#     )

#     enquiries = models.PositiveIntegerField()

#     edit = models.PositiveIntegerField(
#         help_text="Number of edit options allowed"
#     )

#     genuine = models.CharField(
#         max_length=255,
#         help_text="Matching genuine clients"
#     )

#     meta = models.PositiveIntegerField(
#         help_text="Meta ads promotion count"
#     )

#     bulk = models.PositiveIntegerField(
#         help_text="Bulk WhatsApp message count"
#     )

#     poster = models.PositiveIntegerField(
#         help_text="Poster creation count"
#     )

#     social_media = models.CharField(
#         max_length=255,
#         help_text="Social media marketing duration"
#     )

#     lead_follow = models.CharField(
#         max_length=255,
#         help_text="Lead followup support"
#     )

#     best = models.CharField(
#         max_length=255,
#         help_text="Best suited for"
#     )

#     created = models.DateTimeField(auto_now_add=True)

#     def __str__(self):
#         return self.name



# class Userplan(models.Model):
#     id = models.UUIDField(
#         primary_key=True,
#         default=uuid.uuid4,
#         editable=False
#     )

#     plan_type = models.CharField(
#         max_length=50,
#         default="owner_upgrade_plan",
#         editable=False
#     )

#     name = models.CharField(
#         max_length=255,
#         validators=[validate_safe_text]
#     )

#     validity = models.PositiveIntegerField(
#         help_text="Plan validity in days"
#     )

#     listing = models.CharField(
#         max_length=255,
#         help_text="Example: 2 Residential / 1 Commercial",
#         validators=[validate_safe_text]
#     )

#     enquiries = models.PositiveIntegerField()

#     edit = models.PositiveIntegerField(
#         help_text="Number of edit options allowed"
#     )

#     genuine = models.CharField(
#         max_length=255,
#         help_text="Matching genuine clients",
#         validators=[validate_safe_text]
#     )

#     meta = models.PositiveIntegerField(
#         help_text="Meta ads promotion count"
#     )

#     bulk = models.PositiveIntegerField(
#         help_text="Bulk WhatsApp message count"
#     )

#     poster = models.PositiveIntegerField(
#         help_text="Poster creation count"
#     )

#     social_media = models.CharField(
#         max_length=255,
#         help_text="Social media marketing duration",
#         validators=[validate_safe_text]
#     )

#     lead_follow = models.CharField(
#         max_length=255,
#         help_text="Lead followup support",
#         validators=[validate_safe_text]
#     )

#     best = models.CharField(
#         max_length=255,blank=True,null=True,
#         help_text="Best suited for",
#         validators=[validate_safe_text]
#     )

#     created = models.DateTimeField(
#         auto_now_add=True
#     )


#     def clean(self):

#         if self.validity <= 0:

#             raise ValidationError({
#                 "validity": "Validity must be greater than 0."
#             })

#         numeric_fields = {
#             "enquiries": self.enquiries,
#             "edit": self.edit,
#             "meta": self.meta,
#             "bulk": self.bulk,
#             "poster": self.poster
#         }

#         for field_name, value in numeric_fields.items():

#             if value < 0:

#                 raise ValidationError({
#                     field_name: f"{field_name} cannot be negative."
#                 })


#     def save(self, *args, **kwargs):

#         # always fixed
#         self.plan_type = "owner_plan"

#         self.full_clean()

#         super().save(*args, **kwargs)

    
#     def __str__(self):

#         return self.name

import uuid

from django.db import models
from django.core.exceptions import ValidationError

from .validators import validate_safe_text


class Userplan(models.Model):

    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False
    )

    # =====================================
    # PLAN TYPE
    # =====================================

    plan_type = models.CharField(
        max_length=50,
        default="owner_plan",
        editable=False
    )

    # =====================================
    # BASIC
    # =====================================

    name = models.CharField(
        max_length=255,
        validators=[validate_safe_text]
    )

    validity = models.CharField(
        max_length=255,
        default="30 Days",
        validators=[validate_safe_text],
        help_text="Plan validity"
    )

    price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0
    )

    # =====================================
    # PROPERTY LISTING
    # =====================================

    property_listing_limit = models.CharField(
        max_length=255,
        default="No",
        validators=[validate_safe_text],
        db_column="total_property_listing",
        help_text="Total property listings"
    )

    listing_type = models.TextField(
        default="",
        validators=[validate_safe_text],
        db_column="listing",
        help_text="Residential / Commercial listing"
    )

    # =====================================
    # ENQUIRIES
    # =====================================

    enquiry_limit = models.CharField(
        max_length=255,
        default="No",
        validators=[validate_safe_text],
        db_column="enquiries"
    )

    # =====================================
    # EDIT OPTION
    # =====================================

    property_edit_option = models.CharField(
        max_length=255,
        default="No",
        validators=[validate_safe_text],
        db_column="edit"
    )

    # =====================================
    # PROPERTY VISIBILITY
    # =====================================

    property_visibility = models.TextField(
        default="",
        validators=[validate_safe_text]
    )

    # =====================================
    # PRIORITY SEARCH
    # =====================================

    priority_search = models.TextField(
        default="",
        validators=[validate_safe_text],
        db_column="top_priority"
    )

    # =====================================
    # META ADS
    # =====================================

    meta_ads_promotion = models.TextField(
        default="",
        validators=[validate_safe_text],
        db_column="meta"
    )

    # =====================================
    # BULK WHATSAPP
    # =====================================

    bulk_whatsapp_message = models.TextField(
        default="",
        validators=[validate_safe_text],
        db_column="bulk"
    )

    # =====================================
    # POSTER CREATION
    # =====================================

    poster_creation = models.CharField(
        max_length=255,
        default="",
        validators=[validate_safe_text],
        db_column="poster"
    )

    # =====================================
    # SOCIAL MEDIA MARKETING
    # =====================================

    social_media_marketing = models.TextField(
        default="",
        validators=[validate_safe_text],
        db_column="social_media"
    )

    # =====================================
    # LEAD FOLLOW SUPPORT
    # =====================================

    lead_follow_support = models.TextField(
        default="",
        validators=[validate_safe_text],
        db_column="lead_follow"
    )

    # =====================================
    # BEST FOR
    # =====================================

    best_suited_for = models.TextField(
        blank=True,
        null=True,
        default="",
        validators=[validate_safe_text],
        db_column="best"
    )

    # =====================================
    # CREATED
    # =====================================

    created = models.DateTimeField(
        auto_now_add=True
    )

    # =====================================
    # VALIDATION
    # =====================================

    def clean(self):

        if self.price < 0:

            raise ValidationError({
                "price": "Price cannot be negative."
            })

        if not self.name.strip():

            raise ValidationError({
                "name": "Plan name is required."
            })

    # =====================================
    # SAVE
    # =====================================

    def save(self, *args, **kwargs):

        self.plan_type = "owner_plan"

        self.full_clean()

        super().save(*args, **kwargs)

    # =====================================
    # STRING
    # =====================================

    def __str__(self):

        return self.name

class Promotion(models.Model):
    name = models.CharField(
        max_length=255,
        validators=[validate_safe_text]
    )

    purpose = models.CharField(
        max_length=255,
        validators=[validate_safe_text]
    )

    feature = models.CharField(
        max_length=255,
        validators=[validate_safe_text]
    )

    amount = models.PositiveIntegerField()

    def total_amount(self):
        extra_total = sum(extra.amount for extra in self.extras.all())
        return self.amount + extra_total

    def clean(self):
        if self.amount <= 0:
            raise ValidationError("Amount must be greater than 0.")

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name


class PromotionExtra(models.Model):
    promotion = models.ForeignKey(
        Promotion,
        on_delete=models.CASCADE,
        related_name="extras"
    )

    name = models.CharField(
        max_length=255,
        validators=[validate_safe_text]
    )

    amount = models.PositiveIntegerField()

    def clean(self):
        if self.amount <= 0:
            raise ValidationError("Extra amount must be greater than 0.")

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.name} - {self.amount}"


class Advertisement(models.Model):
    name = models.CharField(
        max_length=255,
        validators=[validate_safe_text]
    )

    feature = models.CharField(
        max_length=255,
        validators=[validate_safe_text]
    )

    amount = models.PositiveIntegerField()

    def clean(self):
        if self.amount <= 0:
            raise ValidationError("Amount must be greater than 0.")

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name

class PremiumPlan(models.Model):

    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False
    )

    plan_type = models.CharField(
        max_length=50,
        default="premium",
        editable=False
    )

    name = models.CharField(
        max_length=255,
        unique=True,
        validators=[validate_safe_text]
    )

    validity = models.PositiveIntegerField(
        help_text="Plan validity in days"
    )

    total_listing = models.PositiveIntegerField()

    residential_limit = models.PositiveIntegerField(
        default=5
    )

    commercial_limit = models.PositiveIntegerField(
        default=5
    )

    edit = models.CharField(
        max_length=255,
        blank=True,
        null=True,
        validators=[validate_safe_text]
    )

    enquiries = models.CharField(
        max_length=255,
        blank=True,
        null=True,
        validators=[validate_safe_text]
    )

    priority_search = models.CharField(
        max_length=255,
        blank=True,
        null=True,
        validators=[validate_safe_text]
    )

    meta_ads = models.CharField(
        max_length=255,
        blank=True,
        null=True,
        validators=[validate_safe_text]
    )

    bulk_whatsapp = models.CharField(
        max_length=255,
        blank=True,
        null=True,
        validators=[validate_safe_text]
    )

    poster = models.CharField(
        max_length=255,
        blank=True,
        null=True,
        validators=[validate_safe_text]
    )

    social_media = models.CharField(
        max_length=255,
        blank=True,
        null=True,
        validators=[validate_safe_text]
    )

    lead_follow = models.CharField(
        max_length=255,
        blank=True,
        null=True,
        validators=[validate_safe_text]
    )

    lead_management = models.CharField(
        max_length=255,
        blank=True,
        null=True,
        validators=[validate_safe_text]
    )

    price = models.PositiveIntegerField()

    created = models.DateTimeField(
        auto_now_add=True
    )

    def clean(self):

        if self.validity <= 0:

            raise ValidationError({
                "validity": "Validity must be greater than 0."
            })

        if self.total_listing < 0:

            raise ValidationError({
                "total_listing": "Total listing cannot be negative."
            })

        if self.price <= 0:

            raise ValidationError({
                "price": "Price must be greater than 0."
            })

    def save(self, *args, **kwargs):
        self.plan_type = "premium"

        self.full_clean()

        super().save(*args, **kwargs)

    def __str__(self):

        return self.name

class ElitePlan(models.Model):
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False
    )

    plan_type = models.CharField(
        max_length=50,
        default="elite",
        editable=False
    )


    name = models.CharField(
        max_length=255,
        validators=[validate_safe_text]
    )

    plan_validity_days = models.PositiveIntegerField(
        help_text="Plan validity in days"
    )

    total_property_listings = models.PositiveIntegerField(
        help_text="Total number of property listings allowed"
    )

    # sale_listings_limit = models.PositiveIntegerField(
    #     default=10,
    #     help_text="Number of sale listings allowed"
    # )

    featured_listings_limit = models.PositiveIntegerField(
        default=10,
        help_text="Number of featured listings allowed"
    )

    edit = models.CharField(
        max_length=100,
        blank=True,
        null=True,
        validators=[validate_safe_text],
        help_text="Edit permission for listings"
    )

    priority_search = models.CharField(
        max_length=255,
        default="Not included",
        validators=[validate_safe_text]
    )

    meta_ads_promotion = models.CharField(
        max_length=255,
        default="Not included",
        validators=[validate_safe_text]
    )

    bulk_whatsapp_messages = models.CharField(
        max_length=255,
        default="Not included",
        validators=[validate_safe_text]
    )

    poster_creation = models.CharField(
        max_length=255,
        default="Not included",
        validators=[validate_safe_text]
    )

    social_media_marketing = models.CharField(
        max_length=255,
        default="Not included",
        validators=[validate_safe_text]
    )

    lead_followup_support = models.CharField(
        max_length=255,
        default="Not included",
        validators=[validate_safe_text]
    )

    lead_management = models.CharField(
        max_length=255,
        default="Not included",
        validators=[validate_safe_text]
    )

    price = models.PositiveIntegerField(
        help_text="Plan price"
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )


    def clean(self):

        if self.plan_validity_days <= 0:

            raise ValidationError({
                "plan_validity_days":
                "Plan validity must be greater than 0."
            })

        if self.total_property_listings <= 0:

            raise ValidationError({
                "total_property_listings":
                "Total listings must be greater than 0."
            })

        if self.featured_listings_limit < 0:

            raise ValidationError({
                "featured_listings_limit":
                "featured listings cannot be negative."
            })

        if self.price <= 0:

            raise ValidationError({
                "price":
                "Price must be greater than 0."
            })

    def save(self, *args, **kwargs):

        self.plan_type = "elite"

        self.full_clean()

        super().save(*args, **kwargs)

    def __str__(self):

        return self.name

class AgentPlan(models.Model):

    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False
    )

    plan_type = models.CharField(
        max_length=50,
        default="basic",
        editable=False
    )

    name = models.CharField(
        max_length=255,
        validators=[validate_safe_text]
    )

    validity = models.PositiveIntegerField(
        help_text="Plan validity in days"
    )

    # ❌ REMOVE THESE (do NOT use anymore in code)
    # edit = models.CharField(...)
    # enquiries = models.CharField(...)

    # ✅ NEW FIELD ADDED SAFELY
    agent_badge = models.CharField(
        max_length=255,
        null=True,
        blank=True,
        validators=[validate_safe_text],
        help_text="Badge shown for agent plan (e.g. Verified, Premium, Elite)"
    )

    priority_search = models.CharField(
        max_length=255,
        null=True,
        blank=True,
        validators=[validate_safe_text]
    )

    meta_ads = models.CharField(
        max_length=255,
        null=True,
        blank=True,
        validators=[validate_safe_text]
    )

    bulk_whatsapp = models.CharField(
        max_length=255,
        null=True,
        blank=True,
        validators=[validate_safe_text]
    )

    poster = models.CharField(
        max_length=255,
        null=True,
        blank=True,
        validators=[validate_safe_text]
    )

    social_media = models.CharField(
        max_length=255,
        null=True,
        blank=True,
        validators=[validate_safe_text]
    )

    price = models.PositiveIntegerField()

    created = models.DateTimeField(auto_now_add=True)

    def clean(self):

        if self.validity <= 0:
            raise ValidationError({
                "validity": "Validity must be greater than 0."
            })

        if self.price <= 0:
            raise ValidationError({
                "price": "Price must be greater than 0."
            })

    def save(self, *args, **kwargs):

        self.plan_type = "basic"

        self.full_clean()

        super().save(*args, **kwargs)

    def __str__(self):
        return self.name

class AdvertisementPackage(models.Model):
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False
    )

    plan_type = models.CharField(
        max_length=50,
        default="advertisement",
        editable=False
    )

    AD_FORMAT_CHOICES = [
        ("banner", "Banner"),
        ("slider", "Slider"),
    ]

    PACKAGE_TYPE_CHOICES = [
        ("basic", "Basic"),
        ("pro", "Pro"),
    ]

    name = models.CharField(
        max_length=255,
        validators=[validate_safe_text]
    )

    ad_format = models.CharField(
        max_length=20,
        choices=AD_FORMAT_CHOICES
    )

    package_type = models.CharField(
        max_length=50,
        choices=PACKAGE_TYPE_CHOICES
    )

    price_per_day = models.DecimalField(
        max_digits=10,
        decimal_places=2
    )

    ads_per_day = models.PositiveIntegerField(
        default=1
    )

    display_seconds = models.PositiveIntegerField()

    features = models.JSONField(
        default=list,
        blank=True
    )

    description = models.TextField(
        blank=True,
        null=True,
        validators=[validate_safe_text]
    )

    def clean(self):

        if self.price_per_day <= 0:

            raise ValidationError({
                "price_per_day":
                "Price per day must be greater than 0."
            })

        if self.ads_per_day <= 0:

            raise ValidationError({
                "ads_per_day":
                "Ads per day must be at least 1."
            })

        if self.display_seconds <= 0:

            raise ValidationError({
                "display_seconds":
                "Display seconds must be greater than 0."
            })

        if self.features:

            if not isinstance(self.features, list):

                raise ValidationError({
                    "features":
                    "Features must be a list."
                })

            for item in self.features:

                validate_safe_text(item)


    def save(self, *args, **kwargs):

        self.plan_type = "advertisement"

        self.full_clean()

        super().save(*args, **kwargs)

    def __str__(self):

        return (
            f"{self.name} - ₹{self.price_per_day}"
        )



class ReelPackage(models.Model):

    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False
    )

    plan_type = models.CharField(
        max_length=50,
        default="reel",
        editable=False
    )

    REEL_TYPE_CHOICES = [

        (
            "short_reel",
            "Short Reel (15-30 sec)"
        ),

        (
            "cinematic_reel",
            "Cinematic Reel (30-60 sec)"
        ),
    ]

    REEL_FORMAT_CHOICES = [
        ("instagram", "Instagram Reel"),
        ("youtube_shorts", "YouTube Shorts"),
        ("tiktok", "TikTok Style"),
    ]

    name = models.CharField(
        max_length=255,
        validators=[validate_safe_text]
    )

    reel_type = models.CharField(
        max_length=50,
        choices=REEL_TYPE_CHOICES
    )

    reel_format = models.TextField(
        blank=True,
        null=True,
        validators=[validate_safe_text]
    )

    price_per_day = models.DecimalField(
        max_digits=10,
        decimal_places=2
    )

    duration = models.CharField(
        max_length=50,
        validators=[validate_safe_text]
    )

    description = models.TextField(
        blank=True,
        null=True,
        validators=[validate_safe_text]
    )

    def clean(self):

        if self.price_per_day <= 0:

            raise ValidationError({
                "price_per_day":
                "Price must be greater than 0."
            })

        if (
            not self.duration
            or len(self.duration.strip()) < 2
        ):

            raise ValidationError({
                "duration":
                "Duration must be valid."
            })

    def save(self, *args, **kwargs):

        self.plan_type = "reel"

        self.full_clean()

        super().save(*args, **kwargs)

    def __str__(self):

        return (
            f"{self.name} - ₹{self.price_per_day}"
        )

# class UserAdd(models.Model):
#     user_id = models.CharField(max_length=20, unique=True, blank=True)

#     name = models.CharField(max_length=255)
#     mobile = models.CharField(max_length=255, blank=True, null=True)
#     email = models.CharField(max_length=255, blank=True, null=True)

#     user_plans = models.ManyToManyField(Userplan, blank=True)

#     upgrade_plan = models.ForeignKey(
#         Userupgrade, on_delete=models.SET_NULL, null=True, blank=True
#     )

#     created = models.DateTimeField(auto_now_add=True)
#     is_active = models.BooleanField(default=True)

#     def generate_user_id(self):
#         while True:
#             random_part = ''.join(random.choices(string.digits, k=6))
#             user_id = f"buysel{random_part}"
#             if not UserAdd.objects.filter(user_id=user_id).exists():
#                 return user_id

#     def save(self, *args, **kwargs):
#         if not self.user_id:
#             self.user_id = self.generate_user_id()
#         super().save(*args, **kwargs)

#     def clean(self):
#         from django.core.exceptions import ValidationError

#         if self.pk:
#             if self.user_plans.count() > 2:
#                 raise ValidationError("User can have maximum 2 plans only")

#     def __str__(self):
#         return f"{self.user_id} - {self.name}"

def generate_global_property_uuid():
    from agents.models import AgentProperty
    from developer.models import Property

    while True:

        new_uuid = uuid.uuid4()

        exists = (
            Property.objects.filter(id=new_uuid).exists()
            or
            AgentProperty.objects.filter(id=new_uuid).exists()
        )

        if not exists:
            return new_uuid
        
class Property(models.Model):

    id=models.UUIDField(
        primary_key=True,
        default=generate_global_property_uuid,
        editable=False
    )

    category=models.ForeignKey(
        "Category",
        on_delete=models.CASCADE
    )

    subcategory=models.ForeignKey(
        "Subcategory",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="properties"
    )

    purpose=models.ForeignKey(
        "Purpose",
        on_delete=models.CASCADE
    )

    property_code=models.CharField(
        max_length=20,
        unique=True,
        null=True,
        blank=True,
        db_index=True
    )

    label=models.CharField(
        max_length=255,
        validators=[validate_safe_text]
    )

    land_area=models.CharField(
        max_length=255,
        null=True,
        blank=True,
        validators=[validate_safe_text]
    )

    sq_ft=models.CharField(
        max_length=10,
        null=True,
        blank=True,
        validators=[validate_safe_text]
    )

    description=models.TextField(
        validators=[validate_safe_message]
    )

    amenities=models.ManyToManyField(
        "Amenities",
        blank=True,
        related_name="properties"
    )

    image=CloudinaryField(
        "image",
        folder="properties/main",
        null=True,
        blank=True
    )

    screenshot=CloudinaryField(
        "image",
        folder="properties/screenshots",
        null=True,
        blank=True
    )

    perprice=models.CharField(
        max_length=50,
        blank=True,
        null=True,
        validators=[validate_safe_text]
    )

    price=models.CharField(
        max_length=50,
        validators=[validate_safe_text]
    )

    deposit=models.CharField(
        max_length=255,
        blank=True,
        null=True,
        default="",
        validators=[validate_safe_text]
    )

    user=models.ForeignKey(
        "UserCreate",
        null=True,
        blank=True,
        on_delete=models.CASCADE,
        related_name="properties"
    )

    owner=models.CharField(
        max_length=255,
        blank=True,
        null=True,
        validators=[validate_safe_text]
    )

    package=models.ForeignKey(
        "Userplan",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="properties"
    )
    subscription = models.ForeignKey(
        "UserPlanSubscription",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="properties"
    )

    single_property_package = models.ForeignKey(
        "SinglePropertyPackage",
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )

    single_property_edit_limit = models.PositiveIntegerField(
        default=0
    )

    single_property_edit_used = models.PositiveIntegerField(
        default=0
    )

    whatsapp=models.CharField(
        max_length=255,
        validators=[validate_phone_number]
    )

    phone=models.CharField(
        max_length=255,
        validators=[validate_phone_number]
    )

    location=models.URLField(
        null=True,
        blank=True,
        max_length=3000
    )

    city=models.CharField(
        max_length=255,
        validators=[validate_safe_text]
    )

    pincode=models.CharField(
        max_length=10,
        validators=[validate_pincode]
    )

    district=models.CharField(
        max_length=255,
        blank=True,null=True,
        validators=[validate_safe_text]
    )

    taluk=models.CharField(
        max_length=255,
        null=True,
        blank=True,
        validators=[validate_safe_text]
    )

    village=models.CharField(
        max_length=255,
        null=True,
        blank=True,
        validators=[validate_safe_text]
    )

    state=models.CharField(
        max_length=255,
        null=True,
        blank=True,
        validators=[validate_safe_text]
    )

    land_mark=models.JSONField(
        blank=True,
        null=True,
        default=list
    )

    selling_points=models.JSONField(
        blank=True,
        null=True,
        default=list
    )

    paid=models.CharField(
        max_length=50,
        default="no"
    )

    added_by=models.CharField(
        max_length=255,
        blank=True,
        null=True,
        validators=[validate_safe_text]
    )

    market_staff=models.CharField(
        max_length=255,
        blank=True,
        null=True,
        validators=[validate_safe_text]
    )

    message=models.CharField(
        max_length=2055,
        blank=True,
        null=True,
        validators=[validate_safe_message]
    )

    note=models.TextField(
        blank=True,
        null=True,
        validators=[validate_safe_message]
    )

    is_featured=models.BooleanField(
        default=False,
        db_index=True
    )

    created_at=models.DateTimeField(
        default=timezone.now
    )

    updated_at=models.DateTimeField(
        auto_now=True
    )

    duration_days=models.PositiveIntegerField(
        default=30,
        db_index=True
    )

    expiry_date=models.DateTimeField(
        null=True,
        blank=True
    )

    def clean(self):

        if self.selling_points:

            if not isinstance(self.selling_points,list):

                raise ValidationError({
                    "selling_points":"Selling points must be list"
                })

            if len(self.selling_points)>6:

                raise ValidationError({
                    "selling_points":"Maximum 6 allowed"
                })

            cleaned=[]

            for point in self.selling_points:

                point=str(point).strip()

                validate_safe_text(point)

                if point:
                    cleaned.append(point)

            self.selling_points=cleaned

        if self.land_mark:

            if not isinstance(self.land_mark,list):

                raise ValidationError({
                    "land_mark":"Landmark must be list"
                })

            if len(self.land_mark)>3:

                raise ValidationError({
                    "land_mark":"Maximum 3 allowed"
                })

            cleaned=[]

            for item in self.land_mark:

                if not isinstance(item,dict):

                    raise ValidationError({
                        "land_mark":"Invalid landmark format"
                    })

                name=str(
                    item.get("name","")
                ).strip()

                distance=str(
                    item.get("distance","")
                ).strip()

                validate_safe_text(name)
                validate_safe_text(distance)

                if name and distance:

                    cleaned.append({
                        "name":name,
                        "distance":distance
                    })

            self.land_mark=cleaned

    def generate_property_code(self):

        state_code=(
            self.state[:2]
            if self.state else "NA"
        ).upper()

        purpose_code=(
            self.purpose.name[0].upper()
            if self.purpose and self.purpose.name
            else "X"
        )

        prefix=f"{state_code}-{purpose_code}"

        for _ in range(5):

            with transaction.atomic():

                last=(
                    Property.objects
                    .select_for_update()
                    .filter(
                        property_code__startswith=prefix
                    )
                    .order_by("-created_at")
                    .first()
                )

                if last and last.property_code:

                    try:

                        last_number=int(
                            last.property_code.split("-")[-1]
                        )

                        new_number=last_number+1

                    except Exception:

                        new_number=1

                else:

                    new_number=1

                new_code=f"{prefix}-{new_number}"

                if not Property.objects.filter(
                    property_code=new_code
                ).exists():

                    return new_code

        return f"{prefix}-{str(uuid.uuid4())[:6]}"

    def save(self,*args,**kwargs):

        is_new=self._state.adding

        self.full_clean()

        if self.user and not self.owner:
            self.owner=self.user.name

        if not self.property_code:

            self.property_code=(
                self.generate_property_code()
            )

        super().save(*args,**kwargs)

        if is_new and self.user:

            self.user.role="owner"

            self.user.save(
                update_fields=["role"]
            )

            validity=None

            if getattr(
                self.user,
                "upgrade_plan",
                None
            ):

                validity=(
                    self.user.upgrade_plan.validity
                )

            elif self.package:

                validity=self.package.validity

            # if validity:

            #     self.duration_days=validity

            #     self.expiry_date=(
            #         self.created_at
            #         + timedelta(days=validity)
            #     )
            import re

            if validity:

                validity_str = str(validity)

                numbers = re.findall(r"\d+", validity_str)

                validity_days = int(numbers[0]) if numbers else 30

                self.duration_days = validity_days

                self.expiry_date = (
                    self.created_at +
                    timedelta(days=validity_days)
                )

                super().save(
                    update_fields=[
                        "duration_days",
                        "expiry_date"
                    ]
                )

                # super().save(
                #     update_fields=[
                #         "duration_days",
                #         "expiry_date"
                #     ]
                # )

    def __str__(self):

        return (
            f"{self.label} "
            f"({self.property_code})"
        )

class PropertyFeature(models.Model):

    property=models.ForeignKey(
        Property,
        on_delete=models.CASCADE,
        related_name="property_features"
    )

    field=models.ForeignKey(
        "SubcategoryField",
        on_delete=models.CASCADE
    )

    value=models.CharField(
        max_length=255,
        validators=[validate_safe_text]
    )

    icon=CloudinaryField(
        "icon",
        blank=True,
        null=True
    )

    created_at=models.DateTimeField(
        auto_now_add=True
    )

    def clean(self):

        if not self.value:

            raise ValidationError({
                "value":
                "Value cannot be empty"
            })

    def save(self,*args,**kwargs):

        # if (
        #     self.field
        #     and self.field.icon
        #     and not self.icon
        # ):

        #     self.icon=self.field.icon

        self.full_clean()

        super().save(*args,**kwargs)

        # feature_data=[]

        # for item in self.property.property_features.all():

        #     feature_data.append({
        #         "id":item.id,
        #         "field_id":item.field.id,
        #         "field_name":item.field.field_name,
        #         "value":item.value,
        #         "icon":(
        #             item.icon.url
        #             if item.icon else None
        #         )
        #     })

        # self.property.features=feature_data

        # self.property.save(
        #     update_fields=["features"]
        # )

    def __str__(self):

        return (
            f"{self.property.label} - "
            f"{self.field.field_name}"
        )

class PropertyImage(models.Model):

    property=models.ForeignKey(
        Property,
        on_delete=models.CASCADE,
        related_name="images",
        null=True,
        blank=True
    )

    expired_property=models.ForeignKey(
        "ExpiredProperty",
        on_delete=models.CASCADE,
        related_name="images",
        null=True,
        blank=True
    )

    image=CloudinaryField(
        "image",
        folder="properties/multiple"
    )

    created_at=models.DateTimeField(
        default=timezone.now
    )

    def clean(self):

        if (
            not self.property
            and not self.expired_property
        ):

            raise ValidationError(
                "Image must be linked"
            )

        if (
            self.property
            and self.expired_property
        ):

            raise ValidationError(
                "Only one relation allowed"
            )

        # =================================================
        # MAXIMUM 10 IMAGES
        # =================================================

        if self.property:

            total_images=PropertyImage.objects.filter(
                property=self.property
            ).exclude(
                id=self.id
            ).count()

            if total_images>=10:

                raise ValidationError({
                    "image":
                    "Maximum 10 images allowed"
                })

    def save(self,*args,**kwargs):

        # self.full_clean()
        self.clean()

        super().save(*args,**kwargs)

    def __str__(self):

        if self.property:

            return (
                f"Image for "
                f"{self.property.label}"
            )

        if self.expired_property:

            return (
                f"Expired image for "
                f"{self.expired_property.label}"
            )

        return "Property Image"

class ExpiredProperty(models.Model):

    category = models.ForeignKey("Category", on_delete=models.CASCADE)
    subcategory = models.ForeignKey("Subcategory", on_delete=models.SET_NULL, null=True, blank=True, related_name="expired_properties")
    purpose = models.ForeignKey("Purpose", on_delete=models.CASCADE)

    property_code = models.CharField(max_length=20, unique=True, null=True, blank=True, db_index=True)

    label = models.CharField(max_length=255, validators=[validate_safe_text])
    land_area = models.CharField(max_length=255, validators=[validate_safe_text])

    sq_ft = models.CharField(max_length=10, null=True, blank=True, validators=[validate_safe_text])

    description = models.CharField(max_length=10000, validators=[validate_safe_message])

    amenities = models.ManyToManyField("Amenities", blank=True, related_name="expired_properties")

    image = CloudinaryField('image', folder="propertice")

    perprice = models.CharField(max_length=50, blank=True, null=True, validators=[validate_safe_text])
    price = models.CharField(max_length=50, validators=[validate_safe_text])

    owner = models.CharField(max_length=255, validators=[validate_safe_text])

    whatsapp = models.CharField(max_length=255, validators=[validate_phone_number])
    phone = models.CharField(max_length=255, validators=[validate_phone_number])

    location = models.URLField(max_length=3000)

    city = models.CharField(max_length=255, validators=[validate_safe_text])
    pincode = models.CharField(max_length=10, validators=[validate_pincode])
    district = models.CharField(max_length=255, validators=[validate_safe_text])

    taluk = models.CharField(max_length=255, null=True, blank=True, validators=[validate_safe_text])
    village = models.CharField(max_length=255, null=True, blank=True, validators=[validate_safe_text])
    state = models.CharField(max_length=255, null=True, blank=True, validators=[validate_safe_text])

    land_mark = models.CharField(max_length=255, blank=True, null=True, validators=[validate_safe_text])

    paid = models.CharField(max_length=255, validators=[validate_safe_text])

    added_by = models.CharField(max_length=255, blank=True, null=True, validators=[validate_safe_text])
    market_staff = models.CharField(max_length=255, blank=True, null=True, validators=[validate_safe_text])

    created_at = models.DateTimeField()
    duration_days = models.PositiveIntegerField()
    note = models.TextField(validators=[validate_safe_message])

    screenshot = CloudinaryField('image', folder="propertice/screenshots", blank=True, null=True)

   
    def is_active_again(self):
        return self.duration_days > 0

    def clean(self):


        if self.duration_days < 0:
            raise ValidationError("Duration cannot be negative.")

        if self.property_code:
            self.property_code = self.property_code.strip().upper()

    def save(self, *args, **kwargs):

        self.full_clean() 

        if self.pk and self.is_active_again():

            active_prop = Property.objects.create(
                category=self.category,
                subcategory=self.subcategory,
                purpose=self.purpose,
                property_code=self.property_code,
                label=self.label,
                land_area=self.land_area,
                sq_ft=self.sq_ft,
                description=self.description,
                image=self.image,
                perprice=self.perprice,
                price=self.price,
                owner=self.owner,
                whatsapp=self.whatsapp,
                phone=self.phone,
                location=self.location,
                city=self.city,
                pincode=self.pincode,
                district=self.district,
                taluk=self.taluk,
                village=self.village,
                state=self.state,
                land_mark=self.land_mark,
                paid=self.paid,
                added_by=self.added_by,
                market_staff=self.market_staff,
                created_at=self.created_at,
                duration_days=self.duration_days,
                note=self.note,
                screenshot=self.screenshot,
            )

            active_prop.amenities.set(self.amenities.all())

            for img in self.images.all():
                PropertyImage.objects.create(
                    property=active_prop,
                    image=img.image
                )

            super().delete()

        else:
            super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.label} ({self.property_code})"

class Agents(models.Model):
    agentsname = models.CharField(max_length=100)
    agentsspeacialised = models.CharField(max_length=100)
    agentsphone = models.CharField(max_length=100)
    agentswhatsapp = models.CharField(max_length=100, blank=True, null=True)
    agentsemail = models.EmailField(max_length=100, blank=True, null=True)
    agentslocation = models.CharField(max_length=200)
    agentscity = models.CharField(max_length=200)
    agentspincode = models.CharField(max_length=100)
    agentsimage = CloudinaryField('buysel', folder="agents")

    plan = models.ForeignKey(
        AgentPlan,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="agents"
    )

    created_at = models.DateTimeField(auto_now_add=True)
    duration_days = models.PositiveIntegerField(default=365, null=True, blank=True)

    def is_expired(self):
        if not self.created_at or not self.duration_days:
            return False
        expiry_date = self.created_at + timedelta(days=int(self.duration_days))
        return timezone.now() > expiry_date

    def clean(self):

        validate_agent_name(self.agentsname)
        validate_safe_text(self.agentsspeacialised)
        validate_phone_number(self.agentsphone)

        if self.agentswhatsapp:
            validate_phone_number(self.agentswhatsapp)

        if self.agentsemail:
            validate_email(self.agentsemail)

        validate_safe_text(self.agentslocation)
        validate_safe_text(self.agentscity)
        validate_pincode(self.agentspincode)

        if self.duration_days is not None and self.duration_days < 0:
            raise ValidationError("Duration cannot be negative.")

    
    def save(self, *args, **kwargs):

        self.full_clean()  

        if self.plan:
            self.duration_days = self.plan.validity

        if self.pk and self.is_expired():

            expired = ExpireAgents.objects.create(
                agentsname=self.agentsname,
                agentsspeacialised=self.agentsspeacialised,
                agentsphone=self.agentsphone,
                agentswhatsapp=self.agentswhatsapp,
                agentsemail=self.agentsemail,
                agentslocation=self.agentslocation,
                agentscity=self.agentscity,
                agentspincode=self.agentspincode,
                agentsimage=self.agentsimage,
                created_at=self.created_at,
                duration_days=self.duration_days,
            )

            for img in self.images.all():
                img.expired_agents = expired
                img.agents = None
                img.save()

            super(Agents, self).delete()
        else:
            super(Agents, self).save(*args, **kwargs)



class ExpireAgents(models.Model):
    agentsname = models.CharField(max_length=100)
    agentsspeacialised = models.CharField(max_length=100)
    agentsphone = models.CharField(max_length=100)
    agentswhatsapp = models.CharField(max_length=100, blank=True, null=True)
    agentsemail = models.CharField(max_length=100, blank=True, null=True)
    agentslocation = models.CharField(max_length=200)
    agentscity = models.CharField(max_length=200)
    agentspincode = models.CharField(max_length=100)
    agentsimage = CloudinaryField('buysel', folder="agents")

    created_at = models.DateTimeField()
    duration_days = models.PositiveIntegerField(default=365, null=True, blank=True)

   
    def is_active_again(self):
        try:
            days = int(self.duration_days or 0)
        except (ValueError, TypeError):
            days = 0

        expiry_date = self.created_at + timedelta(days=days)
        return timezone.now() <= expiry_date

    def clean(self):

        validate_agent_name(self.agentsname)
        validate_safe_text(self.agentsspeacialised)
        validate_phone_number(self.agentsphone)

        if self.agentswhatsapp:
            validate_phone_number(self.agentswhatsapp)

        if self.agentsemail:
            validate_email(self.agentsemail)

        validate_safe_text(self.agentslocation)
        validate_safe_text(self.agentscity)
        validate_pincode(self.agentspincode)

        if self.duration_days is not None and self.duration_days < 0:
            raise ValidationError("Duration cannot be negative.")

    def save(self, *args, **kwargs):

        self.full_clean()  

        if self.pk and self.is_active_again():

            active_agent = Agents.objects.create(
                agentsname=self.agentsname,
                agentsspeacialised=self.agentsspeacialised,
                agentsphone=self.agentsphone,
                agentswhatsapp=self.agentswhatsapp,
                agentsemail=self.agentsemail,
                agentslocation=self.agentslocation,
                agentscity=self.agentscity,
                agentspincode=self.agentspincode,
                agentsimage=self.agentsimage,
                created_at=self.created_at,
                duration_days=self.duration_days,
            )

            for img in self.images.all():
                img.agents = active_agent
                img.expired_agents = None
                img.save()

            super(ExpireAgents, self).delete()
        else:
            super(ExpireAgents, self).save(*args, **kwargs)

    def __str__(self):
        return f"{self.agentsname} (Expired)"



class AgentsImage(models.Model):
    agents = models.ForeignKey("Agents", on_delete=models.CASCADE, related_name="images", null=True, blank=True)
    expired_agents = models.ForeignKey("ExpireAgents", on_delete=models.CASCADE, related_name="images", null=True, blank=True)
    image = CloudinaryField("image", folder="agents/multiple")

   
    def clean(self):
        if not self.agents and not self.expired_agents:
            raise ValidationError("Image must be linked to Agents or ExpireAgents.")

        if self.agents and self.expired_agents:
            raise ValidationError("Image cannot be linked to both.")

    def save(self, *args, **kwargs):
        self.full_clean() 
        super().save(*args, **kwargs)

    def __str__(self):
        if self.agents:
            return f"Image for {self.agents}"
        elif self.expired_agents:
            return f"Expired image for {self.expired_agents}"
        return "Orphan image"


class PropertyEnquiry(models.Model):

    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False
    )

    user = models.ForeignKey(
        UserCreate,
        on_delete=models.CASCADE,
        related_name="enquiries"
    )

    property = models.ForeignKey(
        Property,
        on_delete=models.CASCADE,
        null=True,
        blank=True
    )

    name = models.CharField(
        max_length=150
    )

    phone = models.CharField(
        max_length=15
    )

    email = models.EmailField()

    message = models.TextField(
        blank=True
    )

    created_at = models.DateTimeField(
        default=timezone.now
    )

    def clean(self):

        validate_agent_name(self.name)
        validate_phone_number(self.phone)
        validate_email(self.email)

        if self.message:
            validate_safe_message(self.message)

        if not self.property:
            raise ValidationError("Property must be selected.")

    def save(self, *args, **kwargs):
        self.full_clean()  
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.user}"


class PropertyView(models.Model):

    user = models.ForeignKey(
        UserCreate,
        on_delete=models.CASCADE,
        related_name="views"
    )

    property = models.ForeignKey(
        Property,
        on_delete=models.CASCADE,
        related_name="views"
    )

    viewed_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ["user", "property"]  # ✅ ONE VIEW PER USER

    def clean(self):
        if not self.user:
            raise ValidationError("User is required.")
        if not self.property:
            raise ValidationError("Property is required.")
 
    def save(self, *args, **kwargs):
        self.full_clean()  
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.user} viewed {self.property}"



class SliderAd(models.Model):
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False
    )
    image = CloudinaryField('image', folder='slider_banners')
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def clean(self):
        if not self.image:
            raise ValidationError("Banner image is required.")


    def save(self, *args, **kwargs):
        self.full_clean()  
        super().save(*args, **kwargs)


    def __str__(self):
        return f"Banner {self.id}"
    

from django.core.exceptions import ValidationError

def validate_png(image):
    if not image.name.lower().endswith('.png'):
        raise ValidationError("Only PNG images are allowed.")


class BannerAd(models.Model):
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False
    )

    image = CloudinaryField(
        'image',
        folder='hero_images',
        validators=[validate_png]
    )
    is_active = models.BooleanField(default=True)  
    created_at = models.DateTimeField(auto_now_add=True)

    def clean(self):
        if not self.image:
            raise ValidationError("Hero image is required.")

        validate_png(self.image)

    def save(self, *args, **kwargs):
        self.full_clean() 
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Hero Image {self.id}"

import uuid

from django.db import models
from django.utils import timezone

from developer.models import UserCreate
from agents.models import AgentUserProfile, PendingAgentRegistration, PendingAgentRegistration

from developer.models import (
    Userplan,
    PremiumPlan,
    ElitePlan,
    AgentPlan
)


class Payment(models.Model):

    PAYMENT_STATUS = (
        ("created", "Created"),
        ("success", "Success"),
        ("failed", "Failed"),
    )

    PLAN_TYPES = (
        ("user_plan", "User Plan"),
        ("premium", "Premium"),
        ("elite", "Elite"),
        ("agent", "Agent"),
        ("single_property", "Single Property"),
        ("short_reel", "Short Reel"),
        ("cinematic_reel", "Cinematic Reel"),
    )

    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False
    )

    user = models.ForeignKey(
        UserCreate,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name="payments"
    )

    agent = models.ForeignKey(
        AgentUserProfile,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name="payments"
    )

    pending_registration = models.ForeignKey(
        PendingAgentRegistration,
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )

    single_property_package = models.ForeignKey(
        "SinglePropertyPackage",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="payments"
    )

    reel_package = models.ForeignKey(
        ReelPackage,
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )

    plan_type = models.CharField(
        max_length=50,
        choices=PLAN_TYPES
    )

    user_plan = models.ForeignKey(
        Userplan,
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )

    premium_plan = models.ForeignKey(
        PremiumPlan,
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )

    elite_plan = models.ForeignKey(
        ElitePlan,
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )

    agent_plan = models.ForeignKey(
        AgentPlan,
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )

    amount = models.DecimalField(
        max_digits=10,
        decimal_places=2
    )

    razorpay_order_id = models.CharField(
        max_length=255,
        unique=True
    )

    razorpay_payment_id = models.CharField(
        max_length=255,
        null=True,
        blank=True
    )

    razorpay_signature = models.TextField(
        null=True,
        blank=True
    )

    payment_status = models.CharField(
        max_length=20,
        choices=PAYMENT_STATUS,
        default="created"
    )

    paid_at = models.DateTimeField(
        null=True,
        blank=True
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):

        if self.user:
            return f"{self.user.email} - {self.payment_status}"

        if self.agent:
            return f"{self.agent.email} - {self.payment_status}"

        return str(self.id)


class UserPlanSubscription(models.Model):
   
    uuid = models.UUIDField(
        default=uuid.uuid4,
        null=True, blank=True,
        unique=True,
        editable=False,
        db_index=True
    )

    user = models.ForeignKey(
        UserCreate,
        on_delete=models.CASCADE,
        related_name="subscriptions"
    )

    plan = models.ForeignKey(
        Userplan,
        on_delete=models.CASCADE
    )

    is_primary = models.BooleanField(
        default=False
    )

    purchased_at = models.DateTimeField(
        auto_now_add=True
    )

    expiry_date = models.DateTimeField(
        null=True,
        blank=True
    )

    is_active = models.BooleanField(
        default=True
    )

    edit_used = models.PositiveIntegerField(
        default=0
    )

    class Meta:
        ordering = ["-purchased_at"]

    def __str__(self):

        return (
            f"{self.user.email} - "
            f"{self.plan.name}"
        )

    # =====================================================
    # CHECK EXPIRY
    # =====================================================

    def check_expiry(self):

        if (
            self.is_active
            and self.expiry_date
            and timezone.now() > self.expiry_date
        ):

            self.is_active = False

            self.save(
                update_fields=["is_active"]
            )

    # =====================================================
    # EXPIRED
    # =====================================================

    @property
    def expired(self):

        if not self.expiry_date:
            return False

        return timezone.now() > self.expiry_date
    
    # ==========================================
    # PROPERTY LIMIT
    # ==========================================

    @property
    def property_limit(self):

        raw = str(
            self.plan.property_listing_limit
        ).strip()

        return raw

    # ==========================================
    # EDIT LIMIT
    # ==========================================

    @property
    def edit_limit(self):

        return str(
            self.plan.property_edit_option
        ).strip()


    # ==========================================
    # NO EDIT
    # ==========================================

    @property
    def has_no_edit(self):

        value = str(
            self.plan.property_edit_option
        ).lower().strip()

        return value == "no"


    # ==========================================
    # UNLIMITED EDIT
    # ==========================================

    @property
    def is_unlimited_edit(self):

        value = str(
            self.plan.property_edit_option
        ).lower().strip()

        return "unlimited" in value


    # ==========================================
    # EDIT LIMIT COUNT
    # ==========================================

    @property
    def edit_limit_count(self):

        if self.has_no_edit:
            return 0

        if self.is_unlimited_edit:
            return None

        nums = re.findall(
            r"\d+",
            str(self.plan.property_edit_option)
        )

        return (
            int(nums[0])
            if nums
            else 0
        )


    # ==========================================
    # REMAINING EDIT
    # ==========================================

    @property
    def remaining_edit(self):

        if self.has_no_edit:
            return 0

        if self.is_unlimited_edit:
            return "Unlimited"

        return max(
            self.edit_limit_count -
            self.edit_used,
            0
        )
    # =====================================================
    # ACTIVE SUBSCRIPTION
    # HIGHEST PLAN WINS
    # =====================================================

    @property
    def active_subscription(self):

        subscriptions = (
            self.user.subscriptions.filter(
                is_active=True,
                expiry_date__gt=timezone.now()
            )
            .select_related("plan")
        )

        if not subscriptions.exists():

            return None

        def get_limit(sub):

            nums = re.findall(
                r"\d+",
                str(sub.plan.property_listing_limit)
            )

            return (
                int(nums[0])
                if nums
                else 999999
            )

        return max(
            subscriptions,
            key=get_limit
        )

    # =====================================================
    # ACTIVE PLAN
    # =====================================================

    @property
    def active_plan(self):

        subscription = (
            self.active_subscription
        )

        if not subscription:
            return None

        return subscription.plan

    # =====================================================
    # PLAN LIMIT
    # =====================================================

    @property
    def active_plan_limit(self):

        plan = self.active_plan

        if not plan:

            return 2

        nums = re.findall(
            r"\d+",
            str(plan.property_listing_limit)
        )

        return (
            int(nums[0])
            if nums
            else 999999
        )

    # =====================================================
    # USER PROFILE
    # =====================================================

    @property
    def profile(self):

        return getattr(
            self.user,
            "profile",
            None
        )

    # =====================================================
    # REMAINING PROPERTY LIMIT
    # =====================================================

    @property
    def remaining_property_limit(self):

        profile = self.profile

        if not profile:
            return 0

        limit = self.active_plan_limit

        return max(
            limit -
            profile.total_property_used,
            0
        )

    # =====================================================
    # REMAINING RESIDENTIAL LIMIT
    # =====================================================

    @property
    def remaining_residential_limit(self):

        profile = self.profile

        if not profile:
            return 0

        limit = self.active_plan_limit

        return max(
            limit -
            profile.residential_property_used,
            0
        )

    # =====================================================
    # REMAINING COMMERCIAL LIMIT
    # =====================================================

    @property
    def remaining_commercial_limit(self):

        profile = self.profile

        if not profile:
            return 0

        limit = self.active_plan_limit

        return max(
            limit -
            profile.commercial_property_used,
            0
        )

    # =====================================================
    # USER HAS ACTIVE PLAN
    # =====================================================

    @property
    def has_active_plan(self):

        return (
            self.active_subscription
            is not None
        )


class SinglePropertyPackage(models.Model):

    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False
    )

    name = models.CharField(
        max_length=255,
        unique=True
    )

    price = models.DecimalField(
        max_digits=10,
        decimal_places=2
    )

    property_listing_limit = models.PositiveIntegerField(
        default=1
    )

    residential_commercial_listing = models.CharField(
        max_length=255,
        default="Any Property"
    )

    enquiry_limit = models.PositiveIntegerField(
        default=1
    )

    edit_limit = models.PositiveIntegerField(
        default=2
    )

    matching_clients = models.CharField(
        max_length=255,
        default="All Verified Users"
    )

    property_visibility = models.CharField(
        max_length=255,
        default="Middle Priority + Standard Visibility"
    )

    top_priority_search = models.BooleanField(
        default=True
    )

    meta_ads_days = models.PositiveIntegerField(
        default=7
    )

    whatsapp_bulk_limit = models.PositiveIntegerField(
        default=2
    )

    offline_agent_share_limit = models.PositiveIntegerField(
        default=5
    )

    poster_creation_limit = models.PositiveIntegerField(
        default=1
    )

    social_media_marketing_weeks = models.PositiveIntegerField(
        default=1
    )

    lead_followup_support = models.BooleanField(
        default=False
    )

    best_suited_for = models.CharField(
        max_length=255,
        default="Single Property Rental Owners"
    )

    is_active = models.BooleanField(
        default=True,
        db_index=True
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    updated_at = models.DateTimeField(
        auto_now=True
    )

    class Meta:

        ordering = ["price"]

        verbose_name = "Single Property Package"

        verbose_name_plural = "Single Property Packages"

    def __str__(self):

        return self.name

class ReelPurchaseNotification(models.Model):

    NOTIFICATION_CHOICES = (

        ("reel_purchase", "Reel Purchase"),

    )

    title = models.CharField(max_length=255)

    message = models.TextField()

    notification_type = models.CharField(
        max_length=50,
        choices=NOTIFICATION_CHOICES
    )

    payment = models.ForeignKey(
        Payment,
        on_delete=models.CASCADE,
        null=True,
        blank=True
    )

    agent = models.ForeignKey(
        AgentUserProfile,
        on_delete=models.CASCADE,
        null=True,
        blank=True
    )

    is_read = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

