from django.db import models

import uuid
from cloudinary.models import CloudinaryField
import cloudinary.uploader
from playwright.sync_api import sync_playwright
import time
from developer .models import *
from django.contrib.auth.hashers import make_password, check_password

class AgentUserProfile(models.Model):
    AGENT_TYPES = [
        ('basic', 'Basic Agent'),
        ('premium', 'Premium Agent'),
        ('elite', 'Elite Agent'),
    ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    username = models.CharField(max_length=150, unique=True)
    password = models.CharField(max_length=128, null=True)

    email = models.EmailField(max_length=50, unique=True)
    phone_number = models.CharField(max_length=15)
    whatsapp_number = models.CharField(max_length=15, null=True, blank=True)

    address = models.TextField()
    city = models.CharField(max_length=100, null=True, blank=True)
    pin_code = models.IntegerField()

    profile_image = CloudinaryField('image', folder="agenthouses", null=True, blank=True)
    avatar_url = models.URLField(null=True, blank=True)

    professional_title = models.CharField(max_length=150, null=True, blank=True)
    professional_bio = models.TextField(null=True, blank=True)
    years_of_experience = models.IntegerField(null=True, blank=True)

    # Automated fields
    properties_listed = models.IntegerField(default=0)
    deals_closed = models.IntegerField(default=0)

    is_agent = models.BooleanField(default=True)
    agent_type = models.CharField(max_length=20, choices=AGENT_TYPES, default='basic')

    plan = models.ForeignKey(
        "developer.PremiumPlan",
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )
    paid = models.BooleanField(default=False)

    

    specializations = models.ManyToManyField(
        "developer.Category",
        blank=True
    )

    operating_cities = models.JSONField(null=True, blank=True)
    instagram = models.URLField(null=True, blank=True)
    facebook = models.URLField(null=True, blank=True)
    website = models.URLField(null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    agent_code = models.CharField(max_length=20, unique=True, blank=True, null=True)

    def __str__(self):
        return self.username

    def set_password(self, raw_password):
        self.password = make_password(raw_password)

    def check_password(self, raw_password):
        return check_password(raw_password, self.password)

    @property
    def is_authenticated(self):
        return True

    def save(self, *args, **kwargs):

        if not self.agent_code:
            prefix = "buysel"
            name_part = self.username[:3].lower()
            random_number = random.randint(1000, 9999)
            code = f"{prefix}{name_part}{random_number}"

            while AgentUserProfile.objects.filter(agent_code=code).exists():
                random_number = random.randint(1000, 9999)
                code = f"{prefix}{name_part}{random_number}"

            self.agent_code = code

        if not self.profile_image and not self.avatar_url:
            name = self.username
            self.avatar_url = f"https://ui-avatars.com/api/?name={name}&background=random&color=fff&size=256"

        if self.plan:
            self.paid = True

        super().save(*args, **kwargs)

    def get_profile_image(self):
        if self.profile_image:
            return self.profile_image.url
        return self.avatar_url


class AgentRegister(models.Model):

    AGENT_TYPES = [
        ('basic', 'Basic Agent'),
        ('premium', 'Premium Agent'),
        ('elite', 'Elite Agent'),
    ]

    username = models.CharField(max_length=150, unique=True)
    password = models.CharField(max_length=128)

    email = models.EmailField(max_length=50, unique=True)
    phone_number = models.CharField(max_length=15)

    address = models.TextField()
    city = models.CharField(max_length=100, null=True, blank=True)

    profile_image = CloudinaryField('image', folder="agenthouses", null=True, blank=True)
    avatar_url = models.URLField(null=True, blank=True)

    agent_type = models.CharField(max_length=20, choices=AGENT_TYPES, default='basic')

    plan = models.ForeignKey(
        "developer.PremiumPlan",
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.username

    def set_password(self, raw_password):
        from django.contrib.auth.hashers import make_password
        self.password = make_password(raw_password)

    def save(self, *args, **kwargs):

        # ✅ Default avatar logic
        if not self.profile_image and not self.avatar_url:
            name = self.username
            self.avatar_url = f"https://ui-avatars.com/api/?name={name}&length=1&background=random&color=fff&size=256"

        super().save(*args, **kwargs)



class Inbox(models.Model):
    name = models.CharField(max_length=50)
    pin_code = models.CharField(max_length=50)
    contact = models.CharField(max_length=50)
    messages_text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)  #
    is_removed = models.BooleanField(default=False)

    def __str__(self):
        return f"Enquiry from {self.messages_text}"
    

class AgentProperty(models.Model):
    # ForeignKeys from another app (properties)
    agent = models.ForeignKey("developer.Premium", on_delete=models.CASCADE, related_name="properties")
    category = models.ForeignKey(
        "developer.Category",
        on_delete=models.CASCADE,
        related_name="agent_properties"
    )
    purpose = models.ForeignKey(
        "developer.Purpose",
        on_delete=models.CASCADE,
        related_name="agent_properties"
    )

    label = models.CharField(max_length=255)
    land_area = models.CharField(max_length=255)
    sq_ft = models.CharField(max_length=50, null=True, blank=True)
    description = models.CharField(max_length=1000)
    amenities = models.CharField(max_length=500, null=True, blank=True)
    image = CloudinaryField('image', folder="properties")  # Main/cover image

    perprice = models.CharField(max_length=255, blank=True, null=True)
    price = models.CharField(max_length=255)
    whatsapp = models.CharField(max_length=255)
    phone = models.CharField(max_length=255)
    location = models.CharField(max_length=2000)
    city = models.CharField(max_length=255)
    pincode = models.CharField(max_length=50)
    district = models.CharField(max_length=255)
    land_mark = models.CharField(max_length=255, blank=True, null=True)
    owner = models.CharField(max_length=255, blank=True, null=True)
    taluk = models.CharField(max_length=255, blank=True, null=True)
    village = models.CharField(max_length=255, blank=True, null=True)
    state = models.CharField(max_length=255, blank=True, null=True)
    paid = models.BooleanField(default=False)
    notes = models.CharField(max_length=255, blank=True, null=True)

    # Expiry fields
    created_at = models.DateTimeField(auto_now_add=True)
    screenshot = CloudinaryField('image', folder="agents_propertice/screenshots", blank=True, null=True)


    def __str__(self):
        return f"{self.label} - {self.city}"

class AgentPropertyImage(models.Model):
    property = models.ForeignKey("AgentProperty", on_delete=models.CASCADE, related_name="images", null=True, blank=True)


    image = CloudinaryField("image", folder="Agentpropertice/multiple")

    def __str__(self):
        if self.property:
            return f"Image for {self.property}"
        return "Orphan image"



class ContactRequest(models.Model):
    CONTACT_METHOD_CHOICES = [
        ('email', 'Email'),
        ('phone', 'Phone'),
        ('both', 'Both'),
    ]

    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    contact_method = models.CharField(max_length=10, choices=CONTACT_METHOD_CHOICES)
    email = models.EmailField()
    phone = models.CharField(max_length=15, blank=True, null=True)
    message = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.first_name} {self.last_name} ({self.contact_method})"


