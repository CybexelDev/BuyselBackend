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

    properties_listed = models.IntegerField(default=0)
    deals_closed = models.IntegerField(default=0)

    is_agent = models.BooleanField(default=True)
    is_active = models.BooleanField(default=True)

    agent_type = models.CharField(max_length=20, choices=AGENT_TYPES, default='basic')

    # Plans
    plan = models.ForeignKey(
        "developer.PremiumPlan",
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )

    elite_plan = models.ForeignKey(
        "developer.ElitePlan",
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )

    paid = models.BooleanField(default=False)

    # Plan Dates
    plan_start_date = models.DateTimeField(null=True, blank=True)
    plan_expiry_date = models.DateTimeField(null=True, blank=True)

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

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email']

    def __str__(self):
        return self.username

    # ================= PASSWORD =================
    def set_password(self, raw_password):
        self.password = make_password(raw_password)

    def check_password(self, raw_password):
        return check_password(raw_password, self.password)

    @property
    def is_authenticated(self):
        return True if self.pk else False

    # ================= PLAN ACTIVATION =================
    def activate_premium_plan(self, plan):
        self.plan = plan
        self.elite_plan = None
        self.agent_type = "premium"
        self.plan_start_date = timezone.now()
        self.plan_expiry_date = timezone.now() + timedelta(days=plan.validity)
        self.paid = True
        self.save()

    def activate_elite_plan(self, plan):
        self.elite_plan = plan
        self.plan = None
        self.agent_type = "elite"
        self.plan_start_date = timezone.now()
        self.plan_expiry_date = timezone.now() + timedelta(days=plan.plan_validity_days)
        self.paid = True
        self.save()

    # ================= PLAN CHECK =================
    def is_plan_active(self):
        if self.plan_expiry_date:
            if timezone.now() > self.plan_expiry_date:
                self.check_and_downgrade_plan()
                return False
            return True
        return False

    # ================= AUTO DOWNGRADE =================
    def check_and_downgrade_plan(self):
        self.agent_type = "basic"
        self.plan = None
        self.elite_plan = None
        self.paid = False
        self.plan_start_date = None
        self.plan_expiry_date = None
        self.save()

    # ================= GET LIMITS =================
    def get_plan_limits(self):
        if not self.is_plan_active():
            return 0, 0, 0

        if self.plan:
            return (
                self.plan.total_listing,
                self.plan.residential_limit,
                self.plan.commercial_limit
            )

        if self.elite_plan:
            return (
                self.elite_plan.total_property_listings,
                999999,
                999999
            )

        return 0, 0, 0

    # ================= SAVE =================
    def save(self, *args, **kwargs):

        # Hash password if not hashed
        if self.password and not self.password.startswith('pbkdf2_'):
            self.password = make_password(self.password)

        # Generate agent code
        if not self.agent_code:
            prefix = "buysel"
            name_part = self.username[:3].lower()
            random_number = random.randint(1000, 9999)
            code = f"{prefix}{name_part}{random_number}"

            while AgentUserProfile.objects.filter(agent_code=code).exists():
                random_number = random.randint(1000, 9999)
                code = f"{prefix}{name_part}{random_number}"

            self.agent_code = code

        # Avatar fallback
        if not self.profile_image and not self.avatar_url:
            name = self.username
            self.avatar_url = f"https://ui-avatars.com/api/?name={name}&background=random&color=fff&size=256"

        super().save(*args, **kwargs)

    # ================= PROFILE IMAGE =================
    def get_profile_image(self):
        if self.profile_image:
            return self.profile_image.url
        return self.avatar_url
    




class AgentReview(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    agent = models.ForeignKey(
        AgentUserProfile,
        on_delete=models.CASCADE,
        related_name="reviews"
    )

    user_name = models.CharField(max_length=150)
    user_image = models.URLField(null=True, blank=True)

    rating = models.FloatField()  # 1 to 5
    review = models.TextField()

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.agent.username} - {self.rating}"
class PendingAgentRegistration(models.Model):

    AGENT_TYPES = [
        ('basic', 'Basic Agent'),
        ('premium', 'Premium Agent'),
        ('elite', 'Elite Agent'),
    ]

    STATUS_CHOICES = [
        ("pending", "Pending"),
        ("approved", "Approved"),
        ("rejected", "Rejected"),
    ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    # Basic Details
    full_name = models.CharField(max_length=150)
    email = models.EmailField(unique=True)
    phone_number = models.CharField(max_length=15)
    password = models.CharField(max_length=128)

    city = models.CharField(max_length=100)
    pin_code = models.CharField(max_length=10)
    address = models.TextField()

    # Agent Type
    agent_type = models.CharField(max_length=20, choices=AGENT_TYPES)

    # Plans
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

    created_at = models.DateTimeField(auto_now_add=True)

    # Status
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')

    # ✅ PLAN NAME HELPER
    def get_plan_name(self):
        if self.agent_type == "premium" and self.premium_plan:
            return self.premium_plan.name
        elif self.agent_type == "elite" and self.elite_plan:
            return self.elite_plan.name
        return "Basic"

    # ✅ PLAN OBJECT HELPER (optional advanced use)
    def get_plan(self):
        if self.agent_type == "premium":
            return self.premium_plan
        elif self.agent_type == "elite":
            return self.elite_plan
        return None

    def save(self, *args, **kwargs):

        # ✅ Hash password
        if self.password and not self.password.startswith('pbkdf2_'):
            self.password = make_password(self.password)

        super().save(*args, **kwargs)

        # ✅ Create Agent after approval
        if self.status == 'approved':
            if not AgentUserProfile.objects.filter(email=self.email).exists():

                # Generate unique username
                base_username = self.email.split("@")[0]
                username = base_username
                counter = 1

                while AgentUserProfile.objects.filter(username=username).exists():
                    username = f"{base_username}{counter}"
                    counter += 1

                # Create Agent
                agent = AgentUserProfile.objects.create(
                    username=username,
                    email=self.email,
                    phone_number=self.phone_number,
                    whatsapp_number=self.phone_number,
                    city=self.city,
                    pin_code=int(self.pin_code) if self.pin_code else 0,
                    address=self.address,
                    agent_type=self.agent_type,
                    is_agent=True,
                    password=self.password
                )

                # ✅ Assign Plan
                if self.agent_type == "premium" and self.premium_plan:
                    agent.activate_premium_plan(self.premium_plan)

                elif self.agent_type == "elite" and self.elite_plan:
                    agent.activate_elite_plan(self.elite_plan)

                    
class AgentContact(models.Model):
    agent = models.ForeignKey(
        AgentUserProfile,
        on_delete=models.CASCADE,
        related_name='contacts'
    )

    user = models.ForeignKey(
        UserCreate,
        on_delete=models.CASCADE,
        related_name='sent_contacts',
        null=True,
        blank=True
    )

    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    contact_number = models.CharField(max_length=15)
    email = models.EmailField()
    message = models.TextField()

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.first_name} -> {self.agent.username}"





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
    

class AgentProperty(models.Model):
    agent = models.ForeignKey(
        "agents.AgentUserProfile",
        on_delete=models.CASCADE,
        to_field="id"
    )

    category = models.ForeignKey(
        "developer.Category",
        on_delete=models.CASCADE,
        related_name="agent_properties"
    )

    subcategory = models.ForeignKey(
        "developer.Subcategory",
        on_delete=models.CASCADE,
        related_name="agent_properties",
        null=True,
        blank=True
    )

    purpose = models.ForeignKey(
        "developer.Purpose",
        on_delete=models.CASCADE,
        related_name="agent_properties"
    )

    label = models.CharField(max_length=255)
    land_area = models.CharField(max_length=255)
    sq_ft = models.FloatField(null=True, blank=True)
    description = models.TextField()

    amenities = models.ManyToManyField(
        "developer.Amenities",
        blank=True,
        related_name="agent_properties"
    )

    image = CloudinaryField('image', folder="agent_properties", null=True, blank=True)
    screenshot = CloudinaryField(
        'image',
        folder="agents_properties/screenshots",
        blank=True,
        null=True
    )

    perprice = models.CharField(max_length=50, blank=True, null=True)
    price = models.CharField(max_length=50)

    whatsapp = models.CharField(max_length=255, blank=True, null=True)
    phone = models.CharField(max_length=255, blank=True, null=True)

    location = models.TextField()
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

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.label} - {self.city}"
class AgentPropertyFieldValue(models.Model):
    property = models.ForeignKey(
        "AgentProperty",
        on_delete=models.CASCADE,
        related_name="field_values"
    )

    field = models.ForeignKey(
        "developer.SubcategoryField",
        on_delete=models.CASCADE
    )

    value = models.CharField(max_length=255)

    def __str__(self):
        return f"{self.property.label} - {self.field.field_name}"
class AgentPropertyImage(models.Model):
        property = models.ForeignKey(
            "AgentProperty",
            on_delete=models.CASCADE,
            related_name="images"
        )

        image = CloudinaryField("image", folder="Agentproperties/multiple")

        def __str__(self):
            return f"Image for {self.property.label}"

class AgentPropertySellingPoint(models.Model):
    property = models.ForeignKey(
        "AgentProperty",  # string reference instead of direct class
        on_delete=models.CASCADE,
        related_name="selling_points"
    )
    point = models.CharField(max_length=255)

    def __str__(self):
        return self.point


class AgentPropertyLandmark(models.Model):
    property = models.ForeignKey(
        "AgentProperty",  # string reference
        on_delete=models.CASCADE,
        related_name="landmarks"
    )
    name = models.CharField(max_length=255)
    distance = models.CharField(max_length=50, blank=True, null=True)

    def __str__(self):
        return self.name