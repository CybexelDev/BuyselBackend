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







class CustomUser(AbstractUser):
    rate_limit = models.IntegerField(default=0)
    last_failed_login = models.DateTimeField(null=True, blank=True)





class AgentForm(models.Model):
    name = models.CharField(max_length=100)
    email = models.CharField(max_length=50, null=True, blank= True)
    address = models.TextField()
    phone_number = models.CharField(max_length=12)
    category = models.CharField(max_length=100)
    image = CloudinaryField('image', folder="agentreg")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name
    
class Propertylist(models.Model):
    categories = models.CharField(max_length=100)
    purposes = models.CharField(max_length=100)
    label = models.CharField(max_length=100)
    land_area = models.CharField(max_length=100, null=True, blank= True)
    description = models.CharField(max_length=500)
    sq_ft = models.CharField(max_length=100)
    amenities = models.CharField(max_length=500, null=True, blank= True)
    owner = models.CharField(max_length=100)
    locations = models.CharField(max_length=100)
    price = models.CharField(max_length=50)
    about_the_property = models.TextField()
    pin_code = models.CharField(max_length=8)
    land_mark = models.CharField(max_length=100)
    phone = models.CharField(max_length=15)
    image = models.ImageField(upload_to='property-image')
    total_price = models.CharField(max_length=15)
    duration = models.CharField(max_length=100)
    whatsapp = models.CharField(max_length=15)
    city = models.CharField(max_length=100)
    District =models.CharField(max_length=100)
    taluk = models.CharField(max_length=100, null=True, blank=True)
    village = models.CharField(max_length=100, null=True, blank=True)
    state = models.CharField(max_length=100, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

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

class Blog(models.Model):
    blog_head = models.CharField(max_length=100)
    modal_head = models.CharField(max_length=100)
    date = models.DateField()
    card_paragraph = models.TextField()
    modal_paragraph = models.TextField()
    image = CloudinaryField('image', folder="blog")
   


    def __str__(self):
        return self.blog_head



class Purpose(models.Model):
    name = models.CharField(max_length=100)    

    def __str__(self):
        return self.name








from django.db import models
from cloudinary.models import CloudinaryField
from django.utils import timezone
from datetime import timedelta

from django.db import models
from django.utils import timezone
from cloudinary.models import CloudinaryField

class Premium(models.Model):
    name = models.CharField(max_length=100)
    speacialised = models.CharField(max_length=100)
    phone = models.CharField(max_length=100)
    whatsapp = models.CharField(max_length=100, blank=True, null=True)
    email = models.CharField(max_length=100, blank=True, null=True)
    location = models.CharField(max_length=200)
    city = models.CharField(max_length=100)
    pincode = models.CharField(max_length=100)

    username = models.CharField(max_length=100)
    password = models.CharField(max_length=100)

    image = CloudinaryField('buysel', folder="premium_agents")

    created_at = models.DateTimeField(default=timezone.now)
    duration_days = models.PositiveIntegerField(default=365, db_index=True)

    # ------------------------
    def is_expired(self):
        try:
            return int(self.duration_days) <= 0
        except (TypeError, ValueError):
            return False

    # ------------------------
    def save(self, *args, **kwargs):
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
                created_at=self.created_at,  # ✅ SAME DATE
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
    phone = models.CharField(max_length=100)
    whatsapp = models.CharField(max_length=100, blank=True, null=True)
    email = models.CharField(max_length=100, blank=True, null=True)
    location = models.CharField(max_length=200)
    city = models.CharField(max_length=100)
    pincode = models.CharField(max_length=100)

    username = models.CharField(max_length=100)
    password = models.CharField(max_length=100)

    image = CloudinaryField('buysel', folder="premium_agents")

    created_at = models.DateTimeField()  # ✅ preserved
    duration_days = models.PositiveIntegerField()

    # ------------------------
    def is_active_again(self):
        try:
            return int(self.duration_days) > 0
        except (TypeError, ValueError):
            return False

    # ------------------------
    def save(self, *args, **kwargs):
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
                created_at=self.created_at,  # ✅ SAME DATE
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


class PremiumImage(models.Model):
    premium = models.ForeignKey(
        Premium,
        on_delete=models.CASCADE,
        related_name="images",
        null=True,
        blank=True
    )
    expired_premium = models.ForeignKey(
        ExpiredPremium,
        on_delete=models.CASCADE,
        related_name="images",
        null=True,
        blank=True
    )

    image = CloudinaryField("image", folder="premium/multiple")

    def __str__(self):
        if self.premium:
            return f"Image for {self.premium.name}"
        if self.expired_premium:
            return f"Expired image for {self.expired_premium.name}"
        return "Orphan image"



class Agents(models.Model):
    agentsname = models.CharField(max_length=100)
    agentsspeacialised = models.CharField(max_length=100)
    agentsphone = models.CharField(max_length=100)
    agentswhatsapp = models.CharField(max_length=100, blank=True, null=True)
    agentsemail = models.CharField(max_length=100, blank=True, null=True)
    agentslocation = models.CharField(max_length=200)
    agentscity = models.CharField(max_length=200)
    agentspincode = models.CharField(max_length=100)
    agentsimage = CloudinaryField('buysel', folder="agents")

    created_at = models.DateTimeField(auto_now_add=True)
    duration_days = models.PositiveIntegerField(default=365, null=True, blank=True)

    def is_expired(self):
        """Check if the agent's duration has ended"""
        try:
            days = int(self.duration_days or 0)
        except (ValueError, TypeError):
            days = 0
        expiry_date = self.created_at + timedelta(days=days)
        return timezone.now() > expiry_date

    def save(self, *args, **kwargs):
        """Move to ExpireAgents if expired"""
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
                created_at=self.created_at,        # ✅ preserve original created_at
                duration_days=self.duration_days,
            )

            # Move related images
            for img in self.images.all():
                img.expired_agents = expired
                img.agents = None
                img.save()

            super(Agents, self).delete()
        else:
            super(Agents, self).save(*args, **kwargs)

    def __str__(self):
        return f"{self.agentsname} ({'Expired' if self.is_expired() else 'Active'})"


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

    created_at = models.DateTimeField()  # ✅ preserve original created_at
    duration_days = models.PositiveIntegerField(default=365, null=True, blank=True)

    def is_active_again(self):
        """Check if the agent should be moved back to active"""
        try:
            days = int(self.duration_days or 0)
        except (ValueError, TypeError):
            days = 0
        expiry_date = self.created_at + timedelta(days=days)
        return timezone.now() <= expiry_date

    def save(self, *args, **kwargs):
        """Move back to Agents if duration is ≥ 1 or manually updated"""
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
                created_at=self.created_at,        # ✅ preserve original created_at
                duration_days=self.duration_days,
            )

            # Move related images
            for img in self.images.all():
                img.agents = active_agent
                img.expired_agents = None
                img.save()

            super(ExpireAgents, self).delete()
        else:
            super(ExpireAgents, self).save(*args, **kwargs)

    def __str__(self):
        return f"{self.agentsname} (Expired)"


# -------------------------------
# AGENTS IMAGES
# -------------------------------
class AgentsImage(models.Model):
    agents = models.ForeignKey("Agents", on_delete=models.CASCADE, related_name="images", null=True, blank=True)
    expired_agents = models.ForeignKey("ExpireAgents", on_delete=models.CASCADE, related_name="images", null=True, blank=True)
    image = CloudinaryField("image", folder="agents/multiple")

    def __str__(self):
        if self.agents:
            return f"Image for {self.agents}"
        elif self.expired_agents:
            return f"Expired image for {self.expired_agents}"
        return "Orphan image"

class Contact(models.Model):
    name =models.CharField(max_length=100)
    email = models.CharField(max_length=100, null=True, blank=True)
    phone = models.CharField(max_length=14)
    message = models.CharField(max_length=500)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class Request(models.Model):
    name = models.CharField(max_length=100)
    email =  models.CharField(max_length=100, null=True, blank=True)
    phone = models.CharField(max_length=15)
    message = models.CharField(max_length=1000, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)


class Blogadmin(models.Model):
    username = models.CharField(max_length=100)
    password = models.CharField(max_length=100)


class Budget(models.Model):
    value = models.CharField(max_length=100)

    def __str__(self):
        return self.value

import uuid

class UserCreate(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    mobile = models.CharField(max_length=12, blank=True, null=True)
    password = models.CharField(max_length=128)

    otp = models.CharField(max_length=6, null=True, blank=True)
    otp_created_at = models.DateTimeField(null=True, blank=True)

    reset_token = models.UUIDField(
        null=True,
        blank=True,
        unique=True
    )

    is_verified = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    # ✅ ADD THIS
    @property
    def is_authenticated(self):
        return True

    def generate_otp(self):
        return str(random.randint(100000, 999999))

    def __str__(self):
        return self.email


class PasswordResetToken(models.Model):

    user = models.ForeignKey(
        "UserCreate",
        on_delete=models.CASCADE,
        related_name="reset_tokens"
    )

    # UUID token
    token = models.UUIDField(
        default=uuid.uuid4,
        unique=True,
        editable=False
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    expires_at = models.DateTimeField()

    def save(self, *args, **kwargs):

        # expires after 10 minutes
        if not self.expires_at:
            self.expires_at = timezone.now() + timedelta(minutes=10)

        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.user.email} reset token"


import random
import string
from django.utils.text import slugify

class UserProfile(models.Model):

    AUTH_PROVIDERS = (
        ('mobile', 'Mobile'),
        ('google', 'Google'),
        ('facebook', 'Facebook'),
    )

    user = models.OneToOneField(
        UserCreate,
        on_delete=models.CASCADE,
        related_name="profile"
    )

    # 🔥 NEW custom public user id
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
        blank=True
    )

    alternate_mobile = models.CharField(
        max_length=15,
        blank=True
    )

    image = CloudinaryField(
        "image",
        folder="buysel/profile_images",
        blank=True,
        null=True,
        default="Vector_te4oj7"
    )

    auth_provider = models.CharField(
        max_length=20,
        choices=AUTH_PROVIDERS,
        default='mobile'
    )

    is_active = models.BooleanField(default=True)

    created_at = models.DateTimeField(auto_now_add=True)

    def generate_custom_user_id(self):
        base_username = (self.username or "user")[:4].lower()
        random_numbers = ''.join(random.choices(string.digits, k=4))
        return f"buysel{base_username}{random_numbers}"

    def save(self, *args, **kwargs):

        # ✅ Generate username from email if not provided
        if not self.username and self.user.email:
            base = slugify(self.user.email.split("@")[0])
            username = base
            counter = 1

            while UserProfile.objects.filter(username=username).exclude(pk=self.pk).exists():
                username = f"{base}{counter}"
                counter += 1

            self.username = username

        # ✅ Generate custom_user_id if not set
        if not self.custom_user_id:
            custom_id = self.generate_custom_user_id()
            while UserProfile.objects.filter(custom_user_id=custom_id).exists():
                custom_id = self.generate_custom_user_id()
            self.custom_user_id = custom_id

        # ✅ Auto fill full name from user if empty
        if not self.full_name:
            self.full_name = self.user.name

        super().save(*args, **kwargs)

    @property
    def is_profile_complete(self):
        return all([
            self.username,
            self.full_name,
            self.mobile,
            self.image
        ])

    def __str__(self):
        return self.username



class Amenities(models.Model):
    name = models.CharField(max_length=100)
    icon = CloudinaryField("image", folder="buysel/amenities", blank=True, null=True)

    def __str__(self):
        return self.name

class Category(models.Model):
    name = models.CharField(max_length=100)
    icon = CloudinaryField("icon", folder="category")

    def __str__(self):
        return self.name

class Subcategory(models.Model):
    name = models.CharField(max_length=255)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    image = CloudinaryField("icon", folder="subcategory")

    def __str__(self):
        return self.name

class SubcategoryField(models.Model):

    FIELD_TYPES = (
        ("text", "Text"),
        ("number", "Number"),
        ("boolean", "Yes/No"),
        ("select", "Dropdown"),
    )

    subcategory = models.ForeignKey(
        Subcategory,
        on_delete=models.CASCADE,
        related_name="fields"
    )
    icon = CloudinaryField("icons", folder="subcategoryfields", blank=True, null=True)
    field_name = models.CharField(max_length=255)
    field_type = models.CharField(max_length=20, choices=FIELD_TYPES)
    required = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.subcategory.name} - {self.field_name}"




class Property(models.Model):
    category = models.ForeignKey("Category", on_delete=models.CASCADE)
    subcategory = models.ForeignKey(Subcategory,on_delete=models.SET_NULL, null=True,blank=True,related_name="properties")
    purpose = models.ForeignKey("Purpose", on_delete=models.CASCADE)
    dynamic_fields = models.JSONField(blank=True, null=True)
    property_code = models.CharField(max_length=20,unique=True,null=True,blank=True,db_index=True)
    label = models.CharField(max_length=255)
    land_area = models.CharField(max_length=255)

    sq_ft = models.CharField(max_length=10, null=True, blank=True)
    description =models.TextField()
    amenities = models.ManyToManyField(
        "Amenities",
        blank=True,
        related_name="properties"
    )
    image = CloudinaryField('image', folder="propertice")
    perprice = models.CharField(max_length=50, blank=True, null=True)
    price = models.CharField(max_length=50)

    owner = models.CharField(max_length=255)
    whatsapp = models.CharField(max_length=255)
    phone = models.CharField(max_length=255)

    location = models.URLField(max_length=3000)

    city = models.CharField(max_length=255)
    pincode = models.CharField(max_length=10)
    district = models.CharField(max_length=255)
    taluk = models.CharField(max_length=255, null=True, blank=True)
    village = models.CharField(max_length=255, null=True, blank=True)
    state = models.CharField(max_length=255, null=True, blank=True)

    land_mark = models.CharField(max_length=255, blank=True, null=True)
    paid = models.CharField(max_length=255)
    added_by = models.CharField(max_length=255, blank=True, null=True)
    market_staff = models.CharField(max_length=255, blank=True, null=True)

    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)

    duration_days = models.PositiveIntegerField(default=30, db_index=True)
    message =  models.CharField(max_length=2055, blank=True, null=True)
    note = models.TextField()


    screenshot = CloudinaryField(
        'image',
        folder="propertice/screenshots",
        blank=True,
        null=True
    )
    is_featured = models.BooleanField(
        default=False,
        db_index=True
    )


    # -------------------------------
    def is_expired(self):
        return self.duration_days <= 0

    # -------------------------------
    # PROPERTY CODE GENERATOR
    # -------------------------------
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
            except ValueError:
                pass

        return f"{state_code}-{purpose_code}-{number}"

    # -------------------------------
    def save(self, *args, **kwargs):
        # ✅ Generate code for new & old records
        if not self.property_code:
            self.property_code = self.generate_property_code()

        # ✅ Expiry handling
        if self.pk and self.is_expired():
            expired_prop = ExpiredProperty.objects.create(
                category=self.category,
                subcategory=self.subcategory,
                purpose=self.purpose,
                property_code=self.property_code,
                label=self.label,
                land_area=self.land_area,
                sq_ft=self.sq_ft,
                description=self.description,
                amenities=self.amenities,
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
                note = self.note,
                screenshot=self.screenshot,
            )

            for img in self.images.all():
                PropertyImage.objects.create(
                    expired_property=expired_prop,
                    image=img.image
                )

            super().delete()
        else:
            super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.label} ({self.property_code})"


class ExpiredProperty(models.Model):
    category = models.ForeignKey("Category", on_delete=models.CASCADE)
    subcategory = models.ForeignKey(Subcategory,on_delete=models.SET_NULL,null=True,blank=True, related_name="expired_properties")
    purpose = models.ForeignKey("Purpose", on_delete=models.CASCADE)

    property_code = models.CharField(
        max_length=20,
        unique=True,
        null=True,
        blank=True,
        db_index=True
    )

    label = models.CharField(max_length=255)
    land_area = models.CharField(max_length=255)

    sq_ft = models.CharField(max_length=10, null=True, blank=True)
    description = models.CharField(max_length=10000)
    amenities = models.ManyToManyField(
        "Amenities",
        blank=True,
        related_name="expired_properties"
    )
    image = CloudinaryField('image', folder="propertice")
    perprice = models.CharField(max_length=50, blank=True, null=True)
    price = models.CharField(max_length=50)

    owner = models.CharField(max_length=255)
    whatsapp = models.CharField(max_length=255)
    phone = models.CharField(max_length=255)

    location = models.URLField(max_length=3000)

    city = models.CharField(max_length=255)
    pincode = models.CharField(max_length=10)
    district = models.CharField(max_length=255)
    taluk = models.CharField(max_length=255, null=True, blank=True)
    village = models.CharField(max_length=255, null=True, blank=True)
    state = models.CharField(max_length=255, null=True, blank=True)

    land_mark = models.CharField(max_length=255, blank=True, null=True)
    paid = models.CharField(max_length=255)
    added_by = models.CharField(max_length=255, blank=True, null=True)
    market_staff = models.CharField(max_length=255, blank=True, null=True)

    created_at = models.DateTimeField()
    duration_days = models.PositiveIntegerField()
    note = models.TextField()

    screenshot = CloudinaryField(
        'image',
        folder="propertice/screenshots",
        blank=True,
        null=True
    )

    # -------------------------------
    def is_active_again(self):
        return self.duration_days > 0

    # -------------------------------
    def save(self, *args, **kwargs):
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
                amenities=self.amenities,
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
                note = self.note,
                screenshot=self.screenshot,
            )

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

    def __str__(self):
        if self.property:
            return f"Image for {self.property.label}"
        if self.expired_property:
            return f"Expired image for {self.expired_property.label}"
        return "Orphan image"





class UserAdd(models.Model):
    user_id = models.CharField(max_length=20, unique=True, blank=True)

    name = models.CharField(max_length=255)
    mobile = models.CharField(max_length=255, blank=True, null=True)
    email = models.CharField(max_length=255, blank=True, null=True)

    created = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):

        if not self.user_id:
            last_user = UserAdd.objects.order_by('-id').first()

            if last_user:
                last_id = int(last_user.user_id.replace('USR', ''))
                new_id = last_id + 1
            else:
                new_id = 1

            self.user_id = f"USR{new_id:04d}"

        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.user_id} - {self.name}"


class Userplan(models.Model):
    name = models.CharField(max_length=255)
    purpose = models.ManyToManyField(Purpose)
    category = models.ManyToManyField(Category)
    validity = models.PositiveIntegerField()
    amount = models.CharField(max_length=255)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name



class Userupgrade(models.Model):

    name = models.CharField(max_length=255)

    validity = models.PositiveIntegerField(
        help_text="Plan validity in days"
    )

    # Example: 2 Residential / 1 Commercial
    listing = models.CharField(
        max_length=255,
        help_text="Example: 2 Residential / 1 Commercial"
    )

    enquiries = models.PositiveIntegerField()

    edit = models.PositiveIntegerField(
        help_text="Number of edit options allowed"
    )

    genuine = models.CharField(
        max_length=255,
        help_text="Matching genuine clients"
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
        help_text="Social media marketing duration"
    )

    lead_follow = models.CharField(
        max_length=255,
        help_text="Lead followup support"
    )

    best = models.CharField(
        max_length=255,
        help_text="Best suited for"
    )

    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

class Promotion(models.Model):
    name = models.CharField(max_length=255)
    purpose = models.CharField(max_length=255)
    feature = models.CharField(max_length=255)
    amount = models.PositiveIntegerField()

    def total_amount(self):
        extra_total = sum(extra.amount for extra in self.extras.all())
        return self.amount + extra_total

    def __str__(self):
        return self.name

class PromotionExtra(models.Model):
    promotion = models.ForeignKey(
        Promotion,
        on_delete=models.CASCADE,
        related_name="extras"
    )

    name = models.CharField(max_length=255)
    amount = models.PositiveIntegerField()

    def __str__(self):
        return f"{self.name} - {self.amount}"


class Advertisement(models.Model):
    name = models.CharField(max_length=255)
    feature = models.CharField(max_length=255)
    amount = models.PositiveIntegerField()

    def __str__(self):
        return self.name

class PremiumPlan(models.Model):
    name = models.CharField(max_length=255)
    validity = models.PositiveIntegerField(
        help_text="Plan validity in days"
    )
    total_listing = models.PositiveIntegerField()
    residential_limit = models.PositiveIntegerField(default=5)
    commercial_limit = models.PositiveIntegerField(default=5)
    edit = models.CharField(max_length = 255)
    enquiries = models.CharField(max_length = 255)
    priority_search = models.CharField(max_length = 255)
    meta_ads = models.CharField(max_length = 255)
    Bulk_whatsapp = models.CharField(max_length = 255)
    Poster = models.CharField(max_length = 255)
    social_media = models.CharField(max_length = 255)
    lead_follow = models.CharField(max_length = 255)
    lead_management = models.CharField(max_length = 255)
    price = models.PositiveIntegerField()

    created = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return self.name

class ElitePlan(models.Model):
    name = models.CharField(max_length=255)
    validity = models.PositiveIntegerField(
        help_text="Plan validity in days"
    )
    total_listing = models.PositiveIntegerField()
    sale = models.PositiveIntegerField(default=10)
    priority_search = models.CharField(max_length=255)
    meta_ads = models.CharField(max_length=255)
    Bulk_whatsapp = models.CharField(max_length=255)
    Poster = models.CharField(max_length=255)
    social_media = models.CharField(max_length=255)
    lead_follow = models.CharField(max_length=255)
    lead_management = models.CharField(max_length=255)
    price = models.PositiveIntegerField()

    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name




  