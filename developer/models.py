from django.db import models,transaction
import uuid
from cloudinary.models import CloudinaryField
import cloudinary.uploader
from playwright.sync_api import sync_playwright
import time
from django.db.models.signals import post_save
from django.dispatch import receiver

# Create your models here.
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







# class CustomUser(AbstractUser):
#     rate_limit = models.IntegerField(default=0)
#     last_failed_login = models.DateTimeField(null=True, blank=True)
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




# class AgentForm(models.Model):
#     name = models.CharField(max_length=100)
#     email = models.CharField(max_length=50, null=True, blank= True)
#     address = models.TextField()
#     phone_number = models.CharField(max_length=12)
#     category = models.CharField(max_length=100)
#     image = CloudinaryField('image', folder="agentreg")
#     created_at = models.DateTimeField(auto_now_add=True)

#     def __str__(self):
#         return self.name

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
    
# class Propertylist(models.Model):
#     categories = models.CharField(max_length=100)
#     purposes = models.CharField(max_length=100)
#     label = models.CharField(max_length=100)
#     land_area = models.CharField(max_length=100, null=True, blank= True)
#     description = models.CharField(max_length=500)
#     sq_ft = models.CharField(max_length=100)
#     amenities = models.CharField(max_length=500, null=True, blank= True)
#     owner = models.CharField(max_length=100)
#     locations = models.CharField(max_length=100)
#     price = models.CharField(max_length=50)
#     about_the_property = models.TextField()
#     pin_code = models.CharField(max_length=8)
#     land_mark = models.CharField(max_length=100)
#     phone = models.CharField(max_length=15)
#     image = models.ImageField(upload_to='property-image')
#     total_price = models.CharField(max_length=15)
#     duration = models.CharField(max_length=100)
#     whatsapp = models.CharField(max_length=15)
#     city = models.CharField(max_length=100)
#     District =models.CharField(max_length=100)
#     taluk = models.CharField(max_length=100, null=True, blank=True)
#     village = models.CharField(max_length=100, null=True, blank=True)
#     state = models.CharField(max_length=100, null=True, blank=True)
#     created_at = models.DateTimeField(auto_now_add=True)

#     def __str__(self):
#         return self.categories



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






# class ItemImage(models.Model):
#     house = models.ForeignKey('House', null=True, blank=True, on_delete=models.CASCADE, related_name='images')
#     land = models.ForeignKey('Land', null=True, blank=True, on_delete=models.CASCADE, related_name='images')
#     commercial = models.ForeignKey('Commercial', null=True, blank=True, on_delete=models.CASCADE, related_name='images')
#     offplan = models.ForeignKey('OffPlan', null=True, blank=True, on_delete=models.CASCADE, related_name='images')
#     image = models.ImageField(upload_to='item-images/')

#     def __str__(self):
#         return f"Image for {self.house or self.land or self.commercial or self.offplan}"


# class Blog(models.Model):
#     category = models.ForeignKey(
#         "Category",
#         on_delete=models.CASCADE,
#         related_name="blogs",blank=True,null=True
#     )
#     blog_head = models.CharField(max_length=100)
#     # modal_head = models.CharField(max_length=100)
#     date = models.DateField()
#     card_paragraph = models.TextField()
#     # modal_paragraph = models.TextField()
#     image = CloudinaryField('image', folder="blog")
   


#     def __str__(self):
#         return self.blog_head

class Blog(models.Model):

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





# from django.db import models
# from cloudinary.models import CloudinaryField
# from django.utils import timezone
# from datetime import timedelta

# from django.db import models
# from django.utils import timezone
# from cloudinary.models import CloudinaryField

# class Premium(models.Model):
#     name = models.CharField(max_length=100)
#     speacialised = models.CharField(max_length=100)
#     phone = models.CharField(max_length=100)
#     whatsapp = models.CharField(max_length=100, blank=True, null=True)
#     email = models.CharField(max_length=100, blank=True, null=True)
#     location = models.CharField(max_length=200)
#     city = models.CharField(max_length=100)
#     pincode = models.CharField(max_length=100)

#     username = models.CharField(max_length=100)
#     password = models.CharField(max_length=100)

#     image = CloudinaryField('buysel', folder="premium_agents")

#     created_at = models.DateTimeField(default=timezone.now)
#     duration_days = models.PositiveIntegerField(default=365, db_index=True)

#     # ------------------------
#     def is_expired(self):
#         try:
#             return int(self.duration_days) <= 0
#         except (TypeError, ValueError):
#             return False

#     # ------------------------
#     def save(self, *args, **kwargs):
#         if self.pk and self.is_expired():
#             expired = ExpiredPremium.objects.create(
#                 name=self.name,
#                 speacialised=self.speacialised,
#                 phone=self.phone,
#                 whatsapp=self.whatsapp,
#                 email=self.email,
#                 location=self.location,
#                 city=self.city,
#                 pincode=self.pincode,
#                 username=self.username,
#                 password=self.password,
#                 image=self.image,
#                 created_at=self.created_at,  #  SAME DATE
#                 duration_days=self.duration_days,
#             )

#             for img in self.images.all():
#                 PremiumImage.objects.create(
#                     expired_premium=expired,
#                     image=img.image
#                 )

#             super().delete()
#             return

#         super().save(*args, **kwargs)

#     def __str__(self):
#         return f"{self.name} (Active)"


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


# class ExpiredPremium(models.Model):
#     name = models.CharField(max_length=100)
#     speacialised = models.CharField(max_length=100)
#     phone = models.CharField(max_length=100)
#     whatsapp = models.CharField(max_length=100, blank=True, null=True)
#     email = models.CharField(max_length=100, blank=True, null=True)
#     location = models.CharField(max_length=200)
#     city = models.CharField(max_length=100)
#     pincode = models.CharField(max_length=100)

#     username = models.CharField(max_length=100)
#     password = models.CharField(max_length=100)

#     image = CloudinaryField('buysel', folder="premium_agents")

#     created_at = models.DateTimeField()  #  preserved
#     duration_days = models.PositiveIntegerField()

#     # ------------------------
#     def is_active_again(self):
#         try:
#             return int(self.duration_days) > 0
#         except (TypeError, ValueError):
#             return False

#     # ------------------------
#     def save(self, *args, **kwargs):
#         if self.pk and self.is_active_again():
#             active = Premium.objects.create(
#                 name=self.name,
#                 speacialised=self.speacialised,
#                 phone=self.phone,
#                 whatsapp=self.whatsapp,
#                 email=self.email,
#                 location=self.location,
#                 city=self.city,
#                 pincode=self.pincode,
#                 username=self.username,
#                 password=self.password,
#                 image=self.image,
#                 created_at=self.created_at,  # ✅ SAME DATE
#                 duration_days=self.duration_days,
#             )

#             for img in self.images.all():
#                 PremiumImage.objects.create(
#                     premium=active,
#                     image=img.image
#                 )

#             super().delete()
#             return

#         super().save(*args, **kwargs)

#     def __str__(self):
#         return f"{self.name} (Expired)"


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





# class Contact(models.Model):
#     name =models.CharField(max_length=100)
#     email = models.CharField(max_length=100, null=True, blank=True)
#     phone = models.CharField(max_length=14)
#     message = models.CharField(max_length=500)
#     created_at = models.DateTimeField(auto_now_add=True)

#     def __str__(self):
#         return self.name


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
    


# class Request(models.Model):
#     name = models.CharField(max_length=100)
#     email =  models.CharField(max_length=100, null=True, blank=True)
#     phone = models.CharField(max_length=15)
#     message = models.CharField(max_length=1000, null=True, blank=True)
#     created_at = models.DateTimeField(auto_now_add=True)

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


# class Blogadmin(models.Model):
#     username = models.CharField(max_length=100)
#     password = models.CharField(max_length=100)

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


# class Budget(models.Model):
#     value = models.CharField(max_length=100)

#     def __str__(self):
#         return self.value

class Budget(models.Model):

    value = models.CharField(
        max_length=100,
        validators=[validate_budget]
    )

    def __str__(self):
        return self.value

# import uuid

# class UserCreate(models.Model):
#     id = models.UUIDField(
#         primary_key=True,
#         default=uuid.uuid4,
#         editable=False,
#         db_index=True
#     )
#     name = models.CharField(max_length=100)
#     email = models.EmailField(unique=True)
#     mobile = models.CharField(max_length=12, blank=True, null=True)
#     password = models.CharField(max_length=128)

#     otp = models.CharField(max_length=6, null=True, blank=True)
#     otp_created_at = models.DateTimeField(null=True, blank=True)

#     reset_token = models.UUIDField(
#         null=True,
#         blank=True,
#         unique=True
#     )

#     is_verified = models.BooleanField(default=False)
#     created_at = models.DateTimeField(auto_now_add=True)

#     paid_property_count = models.PositiveIntegerField(default=0)
#     last_plan_expiry = models.DateTimeField(null=True, blank=True)

#     user_plans = models.ManyToManyField(
#         "Userplan",
#         blank=True,
#         related_name="users"
#     )

#     upgrade_plan = models.ForeignKey(
#         "Userupgrade",
#         on_delete=models.SET_NULL,
#         null=True,
#         blank=True,
#         related_name="users"
#     )

#     # ✅ ADD THIS
#     @property
#     def is_authenticated(self):
#         return True

#     def generate_otp(self):
#         return str(random.randint(100000, 999999))

#     def __str__(self):
#         return f'{self.email} - {self.id}'


class UserCreate(models.Model):

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

    email = models.EmailField(
        unique=True
    )

    mobile = models.CharField(
        max_length=12,
        blank=True,
        null=True,
        validators=[validate_phone_number]
    )

    password = models.CharField(
        max_length=128,
        validators=[validate_password]
    )

    otp = models.CharField(max_length=6, null=True, blank=True)
    otp_created_at = models.DateTimeField(null=True, blank=True)

    reset_token = models.UUIDField(
        null=True,
        blank=True,
        unique=True
    )

    is_verified = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    paid_property_count = models.PositiveIntegerField(default=0)
    last_plan_expiry = models.DateTimeField(null=True, blank=True)

    user_plans = models.ManyToManyField(
        "Userplan",
        blank=True,
        related_name="users"
    )

    upgrade_plan = models.ForeignKey(
        "Userupgrade",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="users"
    )

    @property
    def is_authenticated(self):
        return True

    def generate_otp(self):
        return str(random.randint(100000, 999999))

    def clean(self):
        if self.email:
            self.email = self.email.lower().strip()


    def save(self, *args, **kwargs):
        self.full_clean()  # ✅ enforce validation
        super().save(*args, **kwargs)


    def __str__(self):
        return f"{self.email} - {self.id}"

# class PasswordResetToken(models.Model):

#     user = models.ForeignKey(
#         "UserCreate",
#         on_delete=models.CASCADE,
#         related_name="reset_tokens"
#     )

#     # UUID token
#     token = models.UUIDField(
#         default=uuid.uuid4,
#         unique=True,
#         editable=False
#     )

#     created_at = models.DateTimeField(
#         auto_now_add=True
#     )

#     expires_at = models.DateTimeField()

#     def save(self, *args, **kwargs):

#         # expires after 10 minutes
#         if not self.expires_at:
#             self.expires_at = timezone.now() + timedelta(minutes=10)

#         super().save(*args, **kwargs)

#     def __str__(self):
#         return f"{self.user.email} reset token"


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


# import random
# import string

# from django.db import models
# from django.utils.text import slugify
# from cloudinary.models import CloudinaryField


# class UserProfile(models.Model):

#     AUTH_PROVIDERS = (
#         ('mobile', 'Mobile'),
#         ('google', 'Google'),
#         ('facebook', 'Facebook'),
#     )

#     user = models.OneToOneField(
#         UserCreate,
#         on_delete=models.CASCADE,
#         related_name="profile"
#     )

#     custom_user_id = models.CharField(
#         max_length=30,
#         unique=True,
#         blank=True
#     )

#     username = models.CharField(
#         max_length=150,
#         unique=True,
#         blank=True
#     )

#     full_name = models.CharField(
#         max_length=150,
#         blank=True
#     )

#     mobile = models.CharField(
#         max_length=15,
#         blank=True
#     )

#     city = models.CharField(
#         max_length=200,
#         blank=True,
#         default=""
#     )

#     alternate_mobile = models.CharField(
#         max_length=15,
#         blank=True
#     )

#     # no default placeholder
#     image = CloudinaryField(
#         "image",
#         folder="buysel/profile_images",
#         blank=True,
#         null=True
#     )

#     auth_provider = models.CharField(
#         max_length=20,
#         choices=AUTH_PROVIDERS,
#         default="mobile"
#     )

#     is_active = models.BooleanField(default=True)

#     created_at = models.DateTimeField(
#         auto_now_add=True
#     )


#     # --------------------------
#     # USER ID
#     # --------------------------
#     def generate_custom_user_id(self):
#         base = (self.username or "user")[:4].lower()
#         nums = ''.join(
#             random.choices(
#                 string.digits,
#                 k=4
#             )
#         )
#         return f"buysel{base}{nums}"


#     def save(self, *args, **kwargs):

#         if not self.username and self.user.email:

#             base = slugify(
#                 self.user.email.split("@")[0]
#             )

#             username = base
#             count = 1

#             while UserProfile.objects.filter(
#                 username=username
#             ).exclude(
#                 pk=self.pk
#             ).exists():

#                 username = f"{base}{count}"
#                 count += 1

#             self.username = username


#         if not self.custom_user_id:

#             cid = self.generate_custom_user_id()

#             while UserProfile.objects.filter(
#                 custom_user_id=cid
#             ).exists():

#                 cid = self.generate_custom_user_id()

#             self.custom_user_id = cid


#         if not self.full_name:
#             self.full_name = self.user.name

#         super().save(*args, **kwargs)



#     # --------------------------
#     # INITIALS
#     # --------------------------
#     @property
#     def initials(self):

#         name = (
#             self.full_name
#             or self.user.name
#             or self.username
#             or "User"
#         ).strip()

#         words = name.split()

#         if len(words) >= 2:
#             return (
#                 words[0][0] +
#                 words[1][0]
#             ).upper()

#         return name[:2].upper()



#     # --------------------------
#     # PROFILE IMAGE OR AVATAR
#     # --------------------------
#     @property
#     def profile_image_url(self):

#         if self.image:

#             try:
#                 img = str(self.image)

#                 # ignore old default vector
#                 if (
#                     img and
#                     "Vector_te4oj7" not in img
#                 ):
#                     return self.image.url

#             except:
#                 pass


#         # fallback initials avatar
#         return (
#             "https://ui-avatars.com/api/"
#             f"?name={self.initials}"
#             "&background=8bc83f"
#             "&color=ffffff"
#             "&size=256"
#             "&bold=true"
#         )


#     @property
#     def is_profile_complete(self):
#         return all([
#             self.username,
#             self.full_name,
#             self.mobile,
#             self.city
#         ])


#     def __str__(self):
#         return self.username


class UserProfile(models.Model):

    AUTH_PROVIDERS = (
        ('mobile', 'Mobile'),
        ('google', 'Google'),
        ('facebook', 'Facebook'),
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

    auth_provider = models.CharField(
        max_length=20,
        choices=AUTH_PROVIDERS,
        default="mobile"
    )

    is_active = models.BooleanField(default=True)

    created_at = models.DateTimeField(auto_now_add=True)

    def clean(self):

        for field in [self.username, self.full_name, self.city]:
            if field and "<script" in field.lower():
                raise ValidationError("Invalid content detected.")

    def generate_custom_user_id(self):
        base = (self.username or "user")[:4].lower()
        nums = ''.join(random.choices(string.digits, k=4))
        return f"buysel{base}{nums}"

   
    def save(self, *args, **kwargs):

        self.full_clean()

        if not self.username and self.user.email:

            base = slugify(self.user.email.split("@")[0])
            username = base
            count = 1

            while UserProfile.objects.filter(
                username=username
            ).exclude(pk=self.pk).exists():
                username = f"{base}{count}"
                count += 1

            self.username = username

        if not self.custom_user_id:

            cid = self.generate_custom_user_id()

            while UserProfile.objects.filter(
                custom_user_id=cid
            ).exists():
                cid = self.generate_custom_user_id()

            self.custom_user_id = cid

        if not self.full_name:
            self.full_name = self.user.name

        super().save(*args, **kwargs)

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
            return (words[0][0] + words[1][0]).upper()

        return name[:2].upper()

    @property
    def profile_image_url(self):

        if self.image:
            try:
                img = str(self.image)
                if img and "Vector_te4oj7" not in img:
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

    @property
    def is_profile_complete(self):
        return all([
            self.username,
            self.full_name,
            self.mobile,
            self.city
        ])

    def __str__(self):
        return self.username

# class Purpose(models.Model):
#     name = models.CharField(max_length=50, unique=True)

#     def __str__(self):
#         return self.name

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
    

# class Amenities(models.Model):
#     name = models.CharField(max_length=100)
#     icon = CloudinaryField("image", folder="buysel/amenities", blank=True, null=True)

#     def __str__(self):
#         return self.name

# class Category(models.Model):
#     name = models.CharField(max_length=50, unique=True)
#     icon = CloudinaryField("icon", folder="category")

#     def __str__(self):
#         return self.name

# class Subcategory(models.Model):
#     name = models.CharField(max_length=255)
#     category = models.ForeignKey(Category, on_delete=models.CASCADE)
#     image = CloudinaryField("icon", folder="subcategory")

#     def __str__(self):
#         return self.name

# class SubcategoryField(models.Model):
#     FIELD_TYPES = (
#     ("text", "Text"),
#     ("number", "Number"),
#     ("boolean", "Yes/No"),
#     ("select", "Select"),
#     ("multi_select", "Multi Select"),
#     ("countable", "Countable"),   # ✅ NEW
#     )

#     FIELD_UI = (
#         ("dropdown", "Dropdown"),
#         ("button_group", "Button Group"),
#         ("checkbox", "Checkbox"),
#     )

#     subcategory = models.ForeignKey(Subcategory, on_delete=models.CASCADE)
#     field_name = models.CharField(max_length=255)

#     field_type = models.CharField(max_length=50, choices=FIELD_TYPES)
#     field_ui = models.CharField(max_length=50, choices=FIELD_UI, blank=True, null=True)

#     required = models.BooleanField(default=False)

#     icon = CloudinaryField('icon', blank=True, null=True)

#     def __str__(self):
#         return self.field_name

# class FieldOption(models.Model):
#     field = models.ForeignKey(
#         SubcategoryField,
#         on_delete=models.CASCADE,
#         related_name="options"
#     )

#     name = models.CharField(max_length=100)
#     icon = CloudinaryField('icon', blank=True, null=True)

#     def __str__(self):
#         return f"{self.field.field_name} - {self.name}"


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






# class Userplan(models.Model):
#     name = models.CharField(max_length=255)


#     residential_limit = models.PositiveIntegerField(null=True, blank=True)
#     commercial_limit = models.PositiveIntegerField(null=True, blank=True)
#     validity = models.PositiveIntegerField()
#     amount = models.DecimalField(max_digits=10, decimal_places=2)

#     # New fields as CharField
#     edit_option = models.CharField(max_length=100, blank=True, null=True)
#     matching_clients = models.CharField(max_length=100, blank=True, null=True)
#     top_priority_search = models.CharField(max_length=100, blank=True, null=True)
#     meta_ads_promotion = models.CharField(max_length=100, blank=True, null=True)
#     bulk_whatsapp = models.CharField(max_length=100, blank=True, null=True)
#     offline_agent_share = models.CharField(max_length=100, blank=True, null=True)
#     poster_creation = models.CharField(max_length=100, blank=True, null=True)
#     social_media_marketing = models.CharField(max_length=100, blank=True, null=True)
#     lead_followup_support = models.CharField(max_length=100, blank=True, null=True)

#     created = models.DateTimeField(auto_now_add=True)

#     def __str__(self):
#         return self.name



# class Subscription(models.Model):
#     agent = models.OneToOneField(
#         'agents.AgentUserProfile',   # ✅ FIXED APP NAME
#         on_delete=models.CASCADE,
#         related_name='subscription'
#     )

#     plan_name = models.CharField(max_length=100)
#     property_limit = models.IntegerField(default=0)
#     used_listings = models.IntegerField(default=0)
#     start_date = models.DateField(auto_now_add=True)
#     end_date = models.DateField()
#     is_active = models.BooleanField(default=True)

class Userplan(models.Model):
    name = models.CharField(
        max_length=255,
        validators=[validate_safe_text]
    )

    residential_limit = models.PositiveIntegerField(null=True, blank=True)
    commercial_limit = models.PositiveIntegerField(null=True, blank=True)

    validity = models.PositiveIntegerField()  

    amount = models.DecimalField(
        max_digits=10,
        decimal_places=2
    )

    edit_option = models.CharField(max_length=100, blank=True, null=True, validators=[validate_safe_text])
    matching_clients = models.CharField(max_length=100, blank=True, null=True, validators=[validate_safe_text])
    top_priority_search = models.CharField(max_length=100, blank=True, null=True, validators=[validate_safe_text])
    meta_ads_promotion = models.CharField(max_length=100, blank=True, null=True, validators=[validate_safe_text])
    bulk_whatsapp = models.CharField(max_length=100, blank=True, null=True, validators=[validate_safe_text])
    offline_agent_share = models.CharField(max_length=100, blank=True, null=True, validators=[validate_safe_text])
    poster_creation = models.CharField(max_length=100, blank=True, null=True, validators=[validate_safe_text])
    social_media_marketing = models.CharField(max_length=100, blank=True, null=True, validators=[validate_safe_text])
    lead_followup_support = models.CharField(max_length=100, blank=True, null=True, validators=[validate_safe_text])

    created = models.DateTimeField(auto_now_add=True)

    def clean(self):
        if self.validity <= 0:
            raise ValidationError("Validity must be greater than 0 days.")

        if self.amount <= 0:
            raise ValidationError("Amount must be greater than 0.")

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name


class Subscription(models.Model):
    agent = models.OneToOneField(
        'agents.AgentUserProfile',
        on_delete=models.CASCADE,
        related_name='subscription'
    )

    plan_name = models.CharField(
        max_length=100,
        validators=[validate_safe_text]
    )

    property_limit = models.IntegerField(default=0)
    used_listings = models.IntegerField(default=0)

    start_date = models.DateField(auto_now_add=True)
    end_date = models.DateField()

    is_active = models.BooleanField(default=True)

    def clean(self):
        if self.end_date <= self.start_date:
            raise ValidationError("End date must be after start date.")

        if self.used_listings > self.property_limit:
            raise ValidationError("Used listings cannot exceed property limit.")

    def save(self, *args, **kwargs):
        self.full_clean()

        if self.end_date < timezone.now().date():
            self.is_active = False

        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.agent} - {self.plan_name}"



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


class Userupgrade(models.Model):

    name = models.CharField(
        max_length=255,
        validators=[validate_safe_text]
    )

    validity = models.PositiveIntegerField(
        help_text="Plan validity in days"
    )

    listing = models.CharField(
        max_length=255,
        help_text="Example: 2 Residential / 1 Commercial",
        validators=[validate_safe_text]
    )

    enquiries = models.PositiveIntegerField()

    edit = models.PositiveIntegerField(
        help_text="Number of edit options allowed"
    )

    genuine = models.CharField(
        max_length=255,
        help_text="Matching genuine clients",
        validators=[validate_safe_text]
    )

    meta = models.PositiveIntegerField(
        help_text="Meta ads promotion count"
    )

    bulk = models.PositiveIntegerField(
        help_text="Bulk WhatsApp message count"
    )

    poster = models.PositiveIntegerField(
        help_text="Poster creation count"
    )

    social_media = models.CharField(
        max_length=255,
        help_text="Social media marketing duration",
        validators=[validate_safe_text]
    )

    lead_follow = models.CharField(
        max_length=255,
        help_text="Lead followup support",
        validators=[validate_safe_text]
    )

    best = models.CharField(
        max_length=255,
        help_text="Best suited for",
        validators=[validate_safe_text]
    )

    created = models.DateTimeField(auto_now_add=True)

    def clean(self):
        if self.validity <= 0:
            raise ValidationError("Validity must be greater than 0.")

        numeric_fields = [
            self.enquiries,
            self.edit,
            self.meta,
            self.bulk,
            self.poster
        ]

        for field in numeric_fields:
            if field < 0:
                raise ValidationError("Numeric values cannot be negative.")

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name


# class Promotion(models.Model):
#     name = models.CharField(max_length=255)
#     purpose = models.CharField(max_length=255)
#     feature = models.CharField(max_length=255)
#     amount = models.PositiveIntegerField()

#     def total_amount(self):
#         extra_total = sum(extra.amount for extra in self.extras.all())
#         return self.amount + extra_total

#     def __str__(self):
#         return self.name

# class PromotionExtra(models.Model):
#     promotion = models.ForeignKey(
#         Promotion,
#         on_delete=models.CASCADE,
#         related_name="extras"
#     )

#     name = models.CharField(max_length=255)
#     amount = models.PositiveIntegerField()

#     def __str__(self):
#         return f"{self.name} - {self.amount}"


# class Advertisement(models.Model):
#     name = models.CharField(max_length=255)
#     feature = models.CharField(max_length=255)
#     amount = models.PositiveIntegerField()

#     def __str__(self):
#         return self.name
# class PremiumPlan(models.Model):
#     name = models.CharField(max_length=255, unique=True)
#     validity = models.PositiveIntegerField(help_text="Plan validity in days")

#     total_listing = models.PositiveIntegerField()
#     residential_limit = models.PositiveIntegerField(default=5)
#     commercial_limit = models.PositiveIntegerField(default=5)

#     edit = models.CharField(max_length=255, blank=True, null=True)
#     enquiries = models.CharField(max_length=255, blank=True, null=True)
#     priority_search = models.CharField(max_length=255, blank=True, null=True)
#     meta_ads = models.CharField(max_length=255, blank=True, null=True)
#     Bulk_whatsapp = models.CharField(max_length=255, blank=True, null=True)
#     Poster = models.CharField(max_length=255, blank=True, null=True)
#     social_media = models.CharField(max_length=255, blank=True, null=True)
#     lead_follow = models.CharField(max_length=255, blank=True, null=True)
#     lead_management = models.CharField(max_length=255, blank=True, null=True)

#     price = models.PositiveIntegerField()
#     created = models.DateTimeField(auto_now_add=True)

#     def __str__(self):
#         return self.name

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
    name = models.CharField(
        max_length=255,
        unique=True,
        validators=[validate_safe_text]
    )

    validity = models.PositiveIntegerField(
        help_text="Plan validity in days"
    )

    total_listing = models.PositiveIntegerField()

    residential_limit = models.PositiveIntegerField(default=5)
    commercial_limit = models.PositiveIntegerField(default=5)

    edit = models.CharField(max_length=255, blank=True, null=True, validators=[validate_safe_text])
    enquiries = models.CharField(max_length=255, blank=True, null=True, validators=[validate_safe_text])
    priority_search = models.CharField(max_length=255, blank=True, null=True, validators=[validate_safe_text])
    meta_ads = models.CharField(max_length=255, blank=True, null=True, validators=[validate_safe_text])
    Bulk_whatsapp = models.CharField(max_length=255, blank=True, null=True, validators=[validate_safe_text])
    Poster = models.CharField(max_length=255, blank=True, null=True, validators=[validate_safe_text])
    social_media = models.CharField(max_length=255, blank=True, null=True, validators=[validate_safe_text])
    lead_follow = models.CharField(max_length=255, blank=True, null=True, validators=[validate_safe_text])
    lead_management = models.CharField(max_length=255, blank=True, null=True, validators=[validate_safe_text])

    price = models.PositiveIntegerField()

    created = models.DateTimeField(auto_now_add=True)

    def clean(self):
        if self.validity <= 0:
            raise ValidationError("Validity must be greater than 0.")

        if self.total_listing < 0:
            raise ValidationError("Total listing cannot be negative.")

        if self.price <= 0:
            raise ValidationError("Price must be greater than 0.")

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name


# class ElitePlan(models.Model):
#     name = models.CharField(max_length=255)

#     # Plan validity in days
#     plan_validity_days = models.PositiveIntegerField(help_text="Plan validity in days")

#     # Property listing limits
#     total_property_listings = models.PositiveIntegerField(help_text="Total number of property listings allowed")
#     sale_listings_limit = models.PositiveIntegerField(help_text="Number of sale listings allowed", default=10)

#     # Features / Services
#     priority_search = models.CharField(
#         max_length=255,
#         default="Not included",
#         help_text="Priority search feature description"
#     )
#     meta_ads_promotion = models.CharField(
#         max_length=255,
#         default="Not included",
#         help_text="Meta Ads promotion details"
#     )
#     bulk_whatsapp_messages = models.CharField(
#         max_length=255,
#         default="Not included",
#         help_text="Bulk WhatsApp messages feature"
#     )
#     poster_creation = models.CharField(
#         max_length=255,
#         default="Not included",
#         help_text="Poster creation details"
#     )
#     social_media_marketing = models.CharField(
#         max_length=255,
#         default="Not included",
#         help_text="Social media marketing support"
#     )
#     lead_followup_support = models.CharField(
#         max_length=255,
#         default="Not included",
#         help_text="Lead follow-up support description"
#     )
#     lead_management = models.CharField(
#         max_length=255,
#         default="Not included",
#         help_text="Lead management description"
#     )

#     # Price
#     price = models.PositiveIntegerField(help_text="Plan price in currency unit")

#     # Metadata
#     created_at = models.DateTimeField(auto_now_add=True)

#     def __str__(self):
#         return self.name


# class AgentPlan(models.Model):
#     name = models.CharField(max_length=255)
#     validity = models.PositiveIntegerField(help_text="Plan validity in days")

#     edit = models.CharField(max_length=255, null=True, blank=True)
#     enquiries = models.CharField(max_length=255, null=True, blank=True)
#     priority_search = models.CharField(max_length=255, null=True, blank=True)
#     meta_ads = models.CharField(max_length=255, null=True, blank=True)
#     Bulk_whatsapp = models.CharField(max_length=255, null=True, blank=True)
#     Poster = models.CharField(max_length=255, null=True, blank=True)
#     social_media = models.CharField(max_length=255, null=True, blank=True)

#     price = models.PositiveIntegerField()
#     created = models.DateTimeField(auto_now_add=True)

#     def __str__(self):
#         return self.name


class ElitePlan(models.Model):
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

    sale_listings_limit = models.PositiveIntegerField(
        default=10,
        help_text="Number of sale listings allowed"
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

    created_at = models.DateTimeField(auto_now_add=True)

    def clean(self):
        if self.plan_validity_days <= 0:
            raise ValidationError("Plan validity must be greater than 0.")

        if self.total_property_listings <= 0:
            raise ValidationError("Total listings must be greater than 0.")

        if self.sale_listings_limit < 0:
            raise ValidationError("Sale listings cannot be negative.")

        if self.price <= 0:
            raise ValidationError("Price must be greater than 0.")

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name


class AgentPlan(models.Model):
    name = models.CharField(
        max_length=255,
        validators=[validate_safe_text]
    )

    validity = models.PositiveIntegerField(
        help_text="Plan validity in days"
    )

    edit = models.CharField(max_length=255, null=True, blank=True, validators=[validate_safe_text])
    enquiries = models.CharField(max_length=255, null=True, blank=True, validators=[validate_safe_text])
    priority_search = models.CharField(max_length=255, null=True, blank=True, validators=[validate_safe_text])
    meta_ads = models.CharField(max_length=255, null=True, blank=True, validators=[validate_safe_text])
    Bulk_whatsapp = models.CharField(max_length=255, null=True, blank=True, validators=[validate_safe_text])
    Poster = models.CharField(max_length=255, null=True, blank=True, validators=[validate_safe_text])
    social_media = models.CharField(max_length=255, null=True, blank=True, validators=[validate_safe_text])

    price = models.PositiveIntegerField()

    created = models.DateTimeField(auto_now_add=True)

    def clean(self):
        if self.validity <= 0:
            raise ValidationError("Validity must be greater than 0.")

        if self.price <= 0:
            raise ValidationError("Price must be greater than 0.")

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name







# class AdvertisementPackage(models.Model):

#     AD_FORMAT_CHOICES = [
#         ("banner", "Banner"),
#         ("slider", "Slider"),
#     ]

#     PACKAGE_TYPE_CHOICES = [
#         ("basic", "Basic"),
#         ("pro", "Pro"),
#     ]

#     name = models.CharField(max_length=255)

#     # ✅ NEW: banner / slider dropdown
#     ad_format = models.CharField(
#         max_length=20,
#         choices=AD_FORMAT_CHOICES
#     )

#     package_type = models.CharField(
#         max_length=50,
#         choices=PACKAGE_TYPE_CHOICES
#     )

#     price_per_day = models.DecimalField(max_digits=10, decimal_places=2)

#     ads_per_day = models.PositiveIntegerField(default=1)

#     display_seconds = models.PositiveIntegerField()

#     # ✅ NEW: flexible features (better than many boolean fields)
#     features = models.JSONField(default=list, blank=True)

#     description = models.TextField(blank=True, null=True)

#     def __str__(self):
#         return f"{self.name} - ₹{self.price_per_day}"
    

# class ReelPackage(models.Model):

#     REEL_TYPE_CHOICES = [
#         ("short_reel", "Short Reel (15-30 sec)"),
#         ("cinematic_reel", "Cinematic Reel (30-60 sec)"),
#     ]

#     REEL_FORMAT_CHOICES = [
#         ("instagram", "Instagram Reel"),
#         ("youtube_shorts", "YouTube Shorts"),
#         ("tiktok", "TikTok Style"),
#     ]

#     name = models.CharField(max_length=255)

#     reel_type = models.CharField(max_length=50, choices=REEL_TYPE_CHOICES)

#     # ✅ NEW FIELD (replaces includes_editing)

#     # ✅ NEW FIELD (replaces vague description)
#     reel_format = models.TextField(blank=True, null=True)
#     price_per_day = models.DecimalField(max_digits=10, decimal_places=2)

#     duration = models.CharField(max_length=50)

#     # optional extra notes
#     description = models.TextField(blank=True, null=True)

#     def __str__(self):
#         return f"{self.name} - ₹{self.price_per_day}"


class AdvertisementPackage(models.Model):

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

    ads_per_day = models.PositiveIntegerField(default=1)

    display_seconds = models.PositiveIntegerField()

    features = models.JSONField(default=list, blank=True)

    description = models.TextField(
        blank=True,
        null=True,
        validators=[validate_safe_text]
    )

    # -------------------------
    def clean(self):
        if self.price_per_day <= 0:
            raise ValidationError("Price per day must be greater than 0.")

        if self.ads_per_day <= 0:
            raise ValidationError("Ads per day must be at least 1.")

        if self.display_seconds <= 0:
            raise ValidationError("Display seconds must be greater than 0.")

        # validate JSON features (must be list of safe strings)
        if self.features:
            if not isinstance(self.features, list):
                raise ValidationError("Features must be a list.")

            for item in self.features:
                validate_safe_text(item)

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.name} - ₹{self.price_per_day}"


class ReelPackage(models.Model):

    REEL_TYPE_CHOICES = [
        ("short_reel", "Short Reel (15-30 sec)"),
        ("cinematic_reel", "Cinematic Reel (30-60 sec)"),
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
            raise ValidationError("Price must be greater than 0.")

        if not self.duration or len(self.duration.strip()) < 2:
            raise ValidationError("Duration must be valid.")

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.name} - ₹{self.price_per_day}"


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
    


# class Property(models.Model):
    
    
#     uuid = models.UUIDField(
#         default=uuid.uuid4,
#         unique=True,
#         editable=False
#     )

#     category = models.ForeignKey("Category", on_delete=models.CASCADE)

#     subcategory = models.ForeignKey(
#         "Subcategory",
#         on_delete=models.SET_NULL,
#         null=True,
#         blank=True,
#         related_name="properties"
#     )

#     purpose = models.ForeignKey("Purpose", on_delete=models.CASCADE)

#     dynamic_fields = models.JSONField(blank=True, null=True)

#     property_code = models.CharField(
#         max_length=20,
#         unique=True,
#         null=True,
#         blank=True,
#         db_index=True
#     )

#     label = models.CharField(max_length=255)
#     land_area = models.CharField(max_length=255)
#     sq_ft = models.CharField(max_length=10, null=True, blank=True)

#     description = models.TextField()

#     amenities = models.ManyToManyField(
#         "Amenities",
#         blank=True,
#         related_name="properties"
#     )

#     image = CloudinaryField('image', folder="propertice")

#     perprice = models.CharField(max_length=50, blank=True, null=True)
#     price = models.CharField(max_length=50)

#     owner = models.ForeignKey(
#         "UserCreate",
#         on_delete=models.CASCADE,
#         related_name="properties"
#     )

#     package = models.ForeignKey(
#         "Userplan",
#         on_delete=models.SET_NULL,
#         null=True,
#         blank=True,
#         related_name="properties"
#     )

#     whatsapp = models.CharField(max_length=255)
#     phone = models.CharField(max_length=255)

#     location = models.URLField(max_length=3000)

#     city = models.CharField(max_length=255)
#     pincode = models.CharField(max_length=10)
#     district = models.CharField(max_length=255)
#     taluk = models.CharField(max_length=255, null=True, blank=True)
#     village = models.CharField(max_length=255, null=True, blank=True)
#     state = models.CharField(max_length=255, null=True, blank=True)

#     # ✅ UPDATED: LANDMARKS WITH DISTANCE (MAX 3)
#     land_mark = models.JSONField(blank=True, null=True, default=list)

#     paid = models.CharField(max_length=50, default="no")

#     added_by = models.CharField(max_length=255, blank=True, null=True)
#     market_staff = models.CharField(max_length=255, blank=True, null=True)

#     created_at = models.DateTimeField(default=timezone.now)
#     updated_at = models.DateTimeField(auto_now=True)

#     # PLAN VALIDITY
#     duration_days = models.PositiveIntegerField(default=30, db_index=True)
#     expiry_date = models.DateTimeField(null=True, blank=True)

#     message = models.CharField(max_length=2055, blank=True, null=True)
#     note = models.TextField(blank=True, null=True)

#     # ✅ KEY SELLING POINTS (MAX 6)
#     key_selling_points = models.JSONField(blank=True, null=True, default=list)

#     screenshot = CloudinaryField(
#         'image',
#         folder="propertice/screenshots",
#         blank=True,
#         null=True
#     )

#     is_featured = models.BooleanField(default=False, db_index=True)

#     # -------------------------------
#     def generate_property_code(self):
#         state_code = (self.state[:2] if self.state else "NA").upper()
#         purpose_code = self.purpose.name[0].upper()

#         last = Property.objects.filter(
#             state=self.state,
#             purpose=self.purpose,
#             property_code__isnull=False
#         ).order_by("-id").first()

#         number = 1
#         if last:
#             try:
#                 number = int(last.property_code.split("-")[-1]) + 1
#             except Exception:
#                 pass

#         return f"{state_code}-{purpose_code}-{number}"

#     # -------------------------------
#     def clean(self):

#         # ✅ KEY SELLING POINTS VALIDATION
#         if self.key_selling_points:
#             if not isinstance(self.key_selling_points, list):
#                 raise ValidationError("Key selling points must be a list.")

#             if len(self.key_selling_points) > 6:
#                 raise ValidationError("Maximum 6 key selling points allowed.")

#             self.key_selling_points = [
#                 str(point).strip()
#                 for point in self.key_selling_points
#                 if str(point).strip()
#             ]

#         # ✅ LANDMARK VALIDATION
#         if self.land_mark:
#             if not isinstance(self.land_mark, list):
#                 raise ValidationError("Landmark must be a list.")

#             if len(self.land_mark) > 3:
#                 raise ValidationError("Maximum 3 landmarks allowed.")

#             cleaned_landmarks = []

#             for item in self.land_mark:

#                 if not isinstance(item, dict):
#                     raise ValidationError("Invalid landmark format.")

#                 name = str(item.get("name", "")).strip()
#                 distance = str(item.get("distance", "")).strip()

#                 if not name or not distance:
#                     continue  # skip empty rows

#                 cleaned_landmarks.append({
#                     "name": name,
#                     "distance": distance
#                 })

#             self.land_mark = cleaned_landmarks

#     # -------------------------------
#     def save(self, *args, **kwargs):
#         is_new = self.pk is None

#         # ✅ FORCE VALIDATION
#         self.full_clean()

#         if not self.property_code:
#             self.property_code = self.generate_property_code()

#         super().save(*args, **kwargs)

#         # PLAN VALIDITY (ONLY ON CREATE)
#         if is_new:
#             validity = None

#             if hasattr(self.owner, "upgrade_plan") and self.owner.upgrade_plan:
#                 validity = self.owner.upgrade_plan.validity

#             elif self.package:
#                 validity = self.package.validity

#             elif hasattr(self.owner, "plan") and self.owner.plan:
#                 validity = self.owner.plan.validity

#             if validity:
#                 self.duration_days = validity
#                 self.expiry_date = self.created_at + timedelta(days=validity)

#                 super().save(update_fields=["duration_days", "expiry_date"])

#     # -------------------------------
#     def __str__(self):
#         return f"{self.label} ({self.property_code})"

class Property(models.Model):

    uuid = models.UUIDField(
        default=uuid.uuid4,
        unique=True,
        editable=False
    )

    category = models.ForeignKey("Category", on_delete=models.CASCADE)

    subcategory = models.ForeignKey(
        "Subcategory",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="properties"
    )

    purpose = models.ForeignKey("Purpose", on_delete=models.CASCADE)

    dynamic_fields = models.JSONField(blank=True, null=True)

    property_code = models.CharField(
        max_length=20,
        unique=True,
        null=True,
        blank=True,
        db_index=True
    )

    label = models.CharField(max_length=255, validators=[validate_safe_text])
    land_area = models.CharField(max_length=255, validators=[validate_safe_text])

    sq_ft = models.CharField(
        max_length=10,
        null=True,
        blank=True,
        validators=[validate_safe_text]
    )

    description = models.TextField(validators=[validate_safe_message])

    amenities = models.ManyToManyField(
        "Amenities",
        blank=True,
        related_name="properties"
    )

    image = CloudinaryField('image', folder="propertice")

    perprice = models.CharField(
        max_length=50,
        blank=True,
        null=True,
        validators=[validate_safe_text]
    )

    price = models.CharField(
        max_length=50,
        validators=[validate_safe_text]
    )

    owner = models.ForeignKey(
        "UserCreate",
        on_delete=models.CASCADE,
        related_name="properties"
    )

    package = models.ForeignKey(
        "Userplan",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="properties"
    )

    whatsapp = models.CharField(
        max_length=255,
        validators=[validate_phone_number]
    )

    phone = models.CharField(
        max_length=255,
        validators=[validate_phone_number]
    )

    location = models.URLField(max_length=3000)

    city = models.CharField(max_length=255, validators=[validate_safe_text])
    pincode = models.CharField(max_length=10, validators=[validate_pincode])
    district = models.CharField(max_length=255, validators=[validate_safe_text])

    taluk = models.CharField(
        max_length=255,
        null=True,
        blank=True,
        validators=[validate_safe_text]
    )

    village = models.CharField(
        max_length=255,
        null=True,
        blank=True,
        validators=[validate_safe_text]
    )

    state = models.CharField(
        max_length=255,
        null=True,
        blank=True,
        validators=[validate_safe_text]
    )

    land_mark = models.JSONField(blank=True, null=True, default=list)

    paid = models.CharField(max_length=50, default="no")

    added_by = models.CharField(
        max_length=255,
        blank=True,
        null=True,
        validators=[validate_safe_text]
    )

    market_staff = models.CharField(
        max_length=255,
        blank=True,
        null=True,
        validators=[validate_safe_text]
    )

    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)

    duration_days = models.PositiveIntegerField(default=30, db_index=True)
    expiry_date = models.DateTimeField(null=True, blank=True)

    message = models.CharField(
        max_length=2055,
        blank=True,
        null=True,
        validators=[validate_safe_message]
    )

    note = models.TextField(
        blank=True,
        null=True,
        validators=[validate_safe_message]
    )

    key_selling_points = models.JSONField(blank=True, null=True, default=list)

    screenshot = CloudinaryField(
        'image',
        folder="propertice/screenshots",
        blank=True,
        null=True
    )

    is_featured = models.BooleanField(default=False, db_index=True)


    def clean(self):

        if self.key_selling_points:
            if not isinstance(self.key_selling_points, list):
                raise ValidationError("Key selling points must be a list.")

            if len(self.key_selling_points) > 6:
                raise ValidationError("Maximum 6 key selling points allowed.")

            cleaned = []
            for point in self.key_selling_points:
                point = str(point).strip()
                validate_safe_text(point)
                if point:
                    cleaned.append(point)

            self.key_selling_points = cleaned

        if self.land_mark:
            if not isinstance(self.land_mark, list):
                raise ValidationError("Landmark must be a list.")

            if len(self.land_mark) > 3:
                raise ValidationError("Maximum 3 landmarks allowed.")

            cleaned = []
            for item in self.land_mark:

                if not isinstance(item, dict):
                    raise ValidationError("Invalid landmark format.")

                name = str(item.get("name", "")).strip()
                distance = str(item.get("distance", "")).strip()

                validate_safe_text(name)
                validate_safe_text(distance)

                if name and distance:
                    cleaned.append({
                        "name": name,
                        "distance": distance
                    })

            self.land_mark = cleaned
    
    def generate_property_code(self):
        state_code = (self.state[:2] if self.state else "NA").upper()
        purpose_code = self.purpose.name[0].upper()

        last = Property.objects.filter(
            state=self.state,
            purpose=self.purpose,
            property_code__isnull=False
        ).order_by("-id").first()

        number = 1
        if last:
            try:
                number = int(last.property_code.split("-")[-1]) + 1
            except Exception:
                pass

    # return f"{state_code}-{purpose_code}-{number}"
    def save(self, *args, **kwargs):
        try:
            self.full_clean()
        except ValidationError as e:
            print("VALIDATION ERROR:", e.message_dict)
            raise

        super().save(*args, **kwargs)

    def save(self, *args, **kwargs):
        is_new = self.pk is None

        self.full_clean()  

        if not self.property_code:
            self.property_code = self.generate_property_code()

        super().save(*args, **kwargs)

        if is_new:
            validity = None

            if self.owner.upgrade_plan:
                validity = self.owner.upgrade_plan.validity
            elif self.package:
                validity = self.package.validity

            if validity:
                self.duration_days = validity
                self.expiry_date = self.created_at + timedelta(days=validity)
                super().save(update_fields=["duration_days", "expiry_date"])

    def __str__(self):
        return f"{self.label} ({self.property_code})"



# class ExpiredProperty(models.Model):
#     category = models.ForeignKey("Category", on_delete=models.CASCADE)
#     subcategory = models.ForeignKey(Subcategory,on_delete=models.SET_NULL,null=True,blank=True, related_name="expired_properties")
#     purpose = models.ForeignKey("Purpose", on_delete=models.CASCADE)

#     property_code = models.CharField(
#         max_length=20,
#         unique=True,
#         null=True,
#         blank=True,
#         db_index=True
#     )

#     label = models.CharField(max_length=255)
#     land_area = models.CharField(max_length=255)

#     sq_ft = models.CharField(max_length=10, null=True, blank=True)
#     description = models.CharField(max_length=10000)
#     amenities = models.ManyToManyField(
#         "Amenities",
#         blank=True,
#         related_name="expired_properties"
#     )
#     image = CloudinaryField('image', folder="propertice")
#     perprice = models.CharField(max_length=50, blank=True, null=True)
#     price = models.CharField(max_length=50)

#     owner = models.CharField(max_length=255)
#     whatsapp = models.CharField(max_length=255)
#     phone = models.CharField(max_length=255)

#     location = models.URLField(max_length=3000)

#     city = models.CharField(max_length=255)
#     pincode = models.CharField(max_length=10)
#     district = models.CharField(max_length=255)
#     taluk = models.CharField(max_length=255, null=True, blank=True)
#     village = models.CharField(max_length=255, null=True, blank=True)
#     state = models.CharField(max_length=255, null=True, blank=True)

#     land_mark = models.CharField(max_length=255, blank=True, null=True)
#     paid = models.CharField(max_length=255)
#     added_by = models.CharField(max_length=255, blank=True, null=True)
#     market_staff = models.CharField(max_length=255, blank=True, null=True)

#     created_at = models.DateTimeField()
#     duration_days = models.PositiveIntegerField()
#     note = models.TextField()

#     screenshot = CloudinaryField(
#         'image',
#         folder="propertice/screenshots",
#         blank=True,
#         null=True
#     )

#     # -------------------------------
#     def is_active_again(self):
#         return self.duration_days > 0

#     # -------------------------------
#     def save(self, *args, **kwargs):
#         if self.pk and self.is_active_again():
#             active_prop = Property.objects.create(
#                 category=self.category,
#                 subcategory=self.subcategory,
#                 purpose=self.purpose,
#                 property_code=self.property_code,
#                 label=self.label,
#                 land_area=self.land_area,
#                 sq_ft=self.sq_ft,
#                 description=self.description,
#                 amenities=self.amenities,
#                 image=self.image,
#                 perprice=self.perprice,
#                 price=self.price,
#                 owner=self.owner,
#                 whatsapp=self.whatsapp,
#                 phone=self.phone,
#                 location=self.location,
#                 city=self.city,
#                 pincode=self.pincode,
#                 district=self.district,
#                 taluk=self.taluk,
#                 village=self.village,
#                 state=self.state,
#                 land_mark=self.land_mark,
#                 paid=self.paid,
#                 added_by=self.added_by,
#                 market_staff=self.market_staff,
#                 created_at=self.created_at,
#                 duration_days=self.duration_days,
#                 note = self.note,
#                 screenshot=self.screenshot,
#             )

#             for img in self.images.all():
#                 PropertyImage.objects.create(
#                     property=active_prop,
#                     image=img.image
#                 )

#             super().delete()
#         else:
#             super().save(*args, **kwargs)

#     def __str__(self):
#         return f"{self.label} ({self.property_code})"

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
    

# class PropertyImage(models.Model):
#     property = models.ForeignKey(
#         Property,
#         on_delete=models.CASCADE,
#         related_name="images",
#         null=True,
#         blank=True
#     )
#     expired_property = models.ForeignKey(
#         ExpiredProperty,
#         on_delete=models.CASCADE,
#         related_name="images",
#         null=True,
#         blank=True
#     )

#     image = CloudinaryField("image", folder="propertice/multiple")

#     def __str__(self):
#         if self.property:
#             return f"Image for {self.property.label}"
#         if self.expired_property:
#             return f"Expired image for {self.expired_property.label}"
#         return "Orphan image"

class PropertyImage(models.Model):
    property = models.ForeignKey(
        Property,
        on_delete=models.CASCADE,
        related_name="images",
        null=True,
        blank=True
    )
    expired_property = models.ForeignKey(
        ExpiredProperty,
        on_delete=models.CASCADE,
        related_name="images",
        null=True,
        blank=True
    )

    image = CloudinaryField("image", folder="propertice/multiple")

   
    def clean(self):
        # Ensure at least one relation exists
        if not self.property and not self.expired_property:
            raise ValidationError(
                "Image must be linked to either Property or ExpiredProperty."
            )

        # Prevent both being set at same time
        if self.property and self.expired_property:
            raise ValidationError(
                "Image cannot be linked to both Property and ExpiredProperty."
            )

    # -------------------------------
    def save(self, *args, **kwargs):
        self.full_clean() 
        super().save(*args, **kwargs)

    # -------------------------------
    def __str__(self):
        if self.property:
            return f"Image for {self.property.label}"
        if self.expired_property:
            return f"Expired image for {self.expired_property.label}"
        return "Orphan image"



# class Agents(models.Model):
#     agentsname = models.CharField(max_length=100)
#     agentsspeacialised = models.CharField(max_length=100)
#     agentsphone = models.CharField(max_length=100)
#     agentswhatsapp = models.CharField(max_length=100, blank=True, null=True)
#     agentsemail = models.CharField(max_length=100, blank=True, null=True)
#     agentslocation = models.CharField(max_length=200)
#     agentscity = models.CharField(max_length=200)
#     agentspincode = models.CharField(max_length=100)
#     agentsimage = CloudinaryField('buysel', folder="agents")

#     #  NEW FIELD
#     plan = models.ForeignKey(
#         AgentPlan,
#         on_delete=models.SET_NULL,
#         null=True,
#         blank=True,
#         related_name="agents"
#     )

#     created_at = models.DateTimeField(auto_now_add=True)
#     duration_days = models.PositiveIntegerField(default=365, null=True, blank=True)

#     def save(self, *args, **kwargs):
#         #  AUTO SET duration from plan
#         if self.plan:
#             self.duration_days = self.plan.validity

#         #  Expiry logic (your existing logic)
#         if self.pk and self.is_expired():
#             expired = ExpireAgents.objects.create(
#                 agentsname=self.agentsname,
#                 agentsspeacialised=self.agentsspeacialised,
#                 agentsphone=self.agentsphone,
#                 agentswhatsapp=self.agentswhatsapp,
#                 agentsemail=self.agentsemail,
#                 agentslocation=self.agentslocation,
#                 agentscity=self.agentscity,
#                 agentspincode=self.agentspincode,
#                 agentsimage=self.agentsimage,
#                 created_at=self.created_at,
#                 duration_days=self.duration_days,
#             )

#             for img in self.images.all():
#                 img.expired_agents = expired
#                 img.agents = None
#                 img.save()

#             super(Agents, self).delete()
#         else:
#             super(Agents, self).save(*args, **kwargs)

# class ExpireAgents(models.Model):
#     agentsname = models.CharField(max_length=100)
#     agentsspeacialised = models.CharField(max_length=100)
#     agentsphone = models.CharField(max_length=100)
#     agentswhatsapp = models.CharField(max_length=100, blank=True, null=True)
#     agentsemail = models.CharField(max_length=100, blank=True, null=True)
#     agentslocation = models.CharField(max_length=200)
#     agentscity = models.CharField(max_length=200)
#     agentspincode = models.CharField(max_length=100)
#     agentsimage = CloudinaryField('buysel', folder="agents")

#     created_at = models.DateTimeField()  # ✅ preserve original created_at
#     duration_days = models.PositiveIntegerField(default=365, null=True, blank=True)

#     def is_active_again(self):
#         """Check if the agent should be moved back to active"""
#         try:
#             days = int(self.duration_days or 0)
#         except (ValueError, TypeError):
#             days = 0
#         expiry_date = self.created_at + timedelta(days=days)
#         return timezone.now() <= expiry_date

#     def save(self, *args, **kwargs):
#         """Move back to Agents if duration is ≥ 1 or manually updated"""
#         if self.pk and self.is_active_again():
#             active_agent = Agents.objects.create(
#                 agentsname=self.agentsname,
#                 agentsspeacialised=self.agentsspeacialised,
#                 agentsphone=self.agentsphone,
#                 agentswhatsapp=self.agentswhatsapp,
#                 agentsemail=self.agentsemail,
#                 agentslocation=self.agentslocation,
#                 agentscity=self.agentscity,
#                 agentspincode=self.agentspincode,
#                 agentsimage=self.agentsimage,
#                 created_at=self.created_at,        # ✅ preserve original created_at
#                 duration_days=self.duration_days,
#             )

#             # Move related images
#             for img in self.images.all():
#                 img.agents = active_agent
#                 img.expired_agents = None
#                 img.save()

#             super(ExpireAgents, self).delete()
#         else:
#             super(ExpireAgents, self).save(*args, **kwargs)

#     def __str__(self):
#         return f"{self.agentsname} (Expired)"

# class AgentsImage(models.Model):
#     agents = models.ForeignKey("Agents", on_delete=models.CASCADE, related_name="images", null=True, blank=True)
#     expired_agents = models.ForeignKey("ExpireAgents", on_delete=models.CASCADE, related_name="images", null=True, blank=True)
#     image = CloudinaryField("image", folder="agents/multiple")

#     def __str__(self):
#         if self.agents:
#             return f"Image for {self.agents}"
#         elif self.expired_agents:
#             return f"Expired image for {self.expired_agents}"
#         return "Orphan image"


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

  
    user = models.ForeignKey(
        UserCreate,
        on_delete=models.CASCADE,
        related_name="enquiries"
    )

    owner = models.ForeignKey(
        "UserCreate",
        on_delete=models.CASCADE,
        null=True,      # ✅ important
        blank=True,
        related_name="received_enquiries"
    )

    
    property = models.ForeignKey(
        Property,
        on_delete=models.CASCADE,
        null=True,
        blank=True
    )

  
    name = models.CharField(max_length=150)
    phone = models.CharField(max_length=15)
    email = models.EmailField()

    message = models.TextField(blank=True)

    created_at = models.DateTimeField(auto_now_add=True)


    # class Meta:
        # unique_together = ["user", "property_hash_id"]

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



class SliderBannerAd(models.Model):
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


class HeroImage(models.Model):
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

