from django.db import models
import uuid
from cloudinary.models import CloudinaryField
import cloudinary.uploader
from playwright.sync_api import sync_playwright
import time
from developer .models import *
from django.contrib.auth.hashers import make_password, check_password
from developer.validators import *
from django.db import transaction
from django.core.exceptions import ValidationError
from django.utils import timezone
from datetime import timedelta
import random

class AgentUserProfile(models.Model):
    AGENT_TYPES = [
        ('basic', 'Basic Agent'),
        ('premium', 'Premium Agent'),
        ('elite', 'Elite Agent'),
    ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    username = models.CharField(max_length=150, unique=True, validators=[validate_username])
    password = models.CharField(max_length=128, null=True, validators=[validate_password])

    email = models.EmailField(max_length=50, unique=True, validators=[validate_email])
    phone_number = models.CharField(max_length=15, validators=[validate_phone_number])
    whatsapp_number = models.CharField(max_length=15, null=True, blank=True, validators=[validate_phone_number])

    address = models.TextField(validators=[validate_safe_text])
    city = models.CharField(max_length=100, null=True, blank=True, validators=[validate_safe_text])
    pin_code = models.IntegerField()

    profile_image = CloudinaryField('image', folder="agenthouses", null=True, blank=True)
    avatar_url = models.URLField(null=True, blank=True)

    professional_title = models.CharField(max_length=150, null=True, blank=True, validators=[validate_safe_text])
    professional_bio = models.TextField(null=True, blank=True, validators=[validate_safe_message])
    years_of_experience = models.IntegerField(null=True, blank=True)

    properties_listed = models.IntegerField(default=0)
    deals_closed = models.IntegerField(default=0)

    is_agent = models.BooleanField(default=True)
    is_active = models.BooleanField(default=True)

    agent_type = models.CharField(max_length=20, choices=AGENT_TYPES, default='basic')

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

    reset_otp = models.CharField(
        max_length=6,
        null=True,
        blank=True
    )

    reset_otp_created_at = models.DateTimeField(
        null=True,
        blank=True
    )

    reset_token = models.UUIDField(
        null=True,
        blank=True,
        unique=True
    )

    def __str__(self):
        return self.username

    def clean(self):
        super().clean()
        validate_pincode(str(self.pin_code))

        if self.whatsapp_number:
            validate_phone_number(self.whatsapp_number)

        if self.years_of_experience is not None and self.years_of_experience < 0:
            raise ValidationError("Years of experience cannot be negative.")

        if self.properties_listed < 0:
            raise ValidationError("Properties listed cannot be negative.")

        if self.deals_closed < 0:
            raise ValidationError("Deals closed cannot be negative.")
        if self.reset_otp:
            if not self.reset_otp.isdigit():
                raise ValidationError({
                    "reset_otp": "OTP must contain only digits."
                })

            if len(self.reset_otp) != 6:
                raise ValidationError({
                    "reset_otp": "OTP must be exactly 6 digits."
                })

        if self.reset_otp and not self.reset_otp_created_at:
            raise ValidationError({
                "reset_otp_created_at": "OTP time must be set when OTP exists."
            })

        if self.reset_otp_created_at and not self.reset_otp:
            raise ValidationError({
                "reset_otp": "OTP must be set if OTP time exists."
            })
        if self.reset_otp_created_at:
            if self.reset_otp_created_at > timezone.now():
                raise ValidationError({
                    "reset_otp_created_at": "OTP time cannot be in future."
                })
        if self.reset_token:
            if not isinstance(self.reset_token, uuid.UUID):
                raise ValidationError({
                    "reset_token": "Invalid reset token."
                })

    def set_password(self, raw_password):
        self.password = make_password(raw_password)

    def check_password(self, raw_password):
        return check_password(raw_password, self.password)

    @property
    def is_authenticated(self):
        return True if self.pk else False

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

    def is_plan_active(self):
        if self.plan_expiry_date:
            if timezone.now() > self.plan_expiry_date:
                self.check_and_downgrade_plan()
                return False
            return True
        return False


    def check_and_downgrade_plan(self):
        self.agent_type = "basic"
        self.plan = None
        self.elite_plan = None
        self.paid = False
        self.plan_start_date = None
        self.plan_expiry_date = None
        self.save()

    
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

    def save(self, *args, **kwargs):

       
        self.full_clean()

        
        if self.password and not self.password.startswith('pbkdf2_'):
            self.password = make_password(self.password)

        if not self.agent_code:
            prefix = "buysel"
            name_part = (self.username[:3] if self.username else "usr").lower()

            for _ in range(5):  # retry safety
                try:
                    with transaction.atomic():

                        base_code = f"{prefix}{name_part}"

                        # Get last matching code for this prefix
                        last_agent = (
                            AgentUserProfile.objects
                            .filter(agent_code__startswith=base_code)
                            .order_by("-agent_code")
                            .first()
                        )

                        if last_agent and last_agent.agent_code:
                            try:
                                last_number = int(last_agent.agent_code.replace(base_code, ""))
                                new_number = last_number + 1
                            except:
                                new_number = 1001
                        else:
                            new_number = 1001

                        self.agent_code = f"{base_code}{new_number}"
                        break

                except Exception:
                    continue

       
        if not self.profile_image and not self.avatar_url:
            name = self.username[:1]
            self.avatar_url = f"https://ui-avatars.com/api/?name={name}&background=000000&color=ffffff&size=256"

        super().save(*args, **kwargs)

    def get_profile_image(self):
        if self.profile_image:
            return self.profile_image.url
        return self.avatar_url
    

# class AgentUserProfile(models.Model):
#     AGENT_TYPES = [
#         ('basic', 'Basic Agent'),
#         ('premium', 'Premium Agent'),
#         ('elite', 'Elite Agent'),
#     ]

#     id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

#     username = models.CharField(max_length=150, unique=True)
#     password = models.CharField(max_length=128, null=True)

#     email = models.EmailField(max_length=50, unique=True)
#     phone_number = models.CharField(max_length=15)
#     whatsapp_number = models.CharField(max_length=15, null=True, blank=True)

#     address = models.TextField()
#     city = models.CharField(max_length=100, null=True, blank=True)
#     pin_code = models.IntegerField()

#     profile_image = CloudinaryField('image', folder="agenthouses", null=True, blank=True)
#     avatar_url = models.URLField(null=True, blank=True)

#     professional_title = models.CharField(max_length=150, null=True, blank=True)
#     professional_bio = models.TextField(null=True, blank=True)
#     years_of_experience = models.IntegerField(null=True, blank=True)

#     properties_listed = models.IntegerField(default=0)
#     deals_closed = models.IntegerField(default=0)

#     is_agent = models.BooleanField(default=True)
#     is_active = models.BooleanField(default=True)

#     agent_type = models.CharField(max_length=20, choices=AGENT_TYPES, default='basic')

#     # Plans
#     plan = models.ForeignKey(
#         "developer.PremiumPlan",
#         on_delete=models.SET_NULL,
#         null=True,
#         blank=True
#     )

#     elite_plan = models.ForeignKey(
#         "developer.ElitePlan",
#         on_delete=models.SET_NULL,
#         null=True,
#         blank=True
#     )

#     paid = models.BooleanField(default=False)

#     # Plan Dates
#     plan_start_date = models.DateTimeField(null=True, blank=True)
#     plan_expiry_date = models.DateTimeField(null=True, blank=True)

#     specializations = models.ManyToManyField(
#         "developer.Category",
#         blank=True
#     )

#     operating_cities = models.JSONField(null=True, blank=True)
#     instagram = models.URLField(null=True, blank=True)
#     facebook = models.URLField(null=True, blank=True)
#     website = models.URLField(null=True, blank=True)

#     created_at = models.DateTimeField(auto_now_add=True)
#     agent_code = models.CharField(max_length=20, unique=True, blank=True, null=True)

#     USERNAME_FIELD = 'username'
#     REQUIRED_FIELDS = ['email']

#     def __str__(self):
#         return self.username

#     # ================= PASSWORD =================
#     def set_password(self, raw_password):
#         self.password = make_password(raw_password)

#     def check_password(self, raw_password):
#         return check_password(raw_password, self.password)

#     @property
#     def is_authenticated(self):
#         return True if self.pk else False

#     # ================= PLAN ACTIVATION =================
#     def activate_premium_plan(self, plan):
#         self.plan = plan
#         self.elite_plan = None
#         self.agent_type = "premium"
#         self.plan_start_date = timezone.now()
#         self.plan_expiry_date = timezone.now() + timedelta(days=plan.validity)
#         self.paid = True
#         self.save()

#     def activate_elite_plan(self, plan):
#         self.elite_plan = plan
#         self.plan = None
#         self.agent_type = "elite"
#         self.plan_start_date = timezone.now()
#         self.plan_expiry_date = timezone.now() + timedelta(days=plan.plan_validity_days)
#         self.paid = True
#         self.save()

#     # ================= PLAN CHECK =================
#     def is_plan_active(self):
#         if self.plan_expiry_date:
#             if timezone.now() > self.plan_expiry_date:
#                 self.check_and_downgrade_plan()
#                 return False
#             return True
#         return False

#     # ================= AUTO DOWNGRADE =================
#     def check_and_downgrade_plan(self):
#         self.agent_type = "basic"
#         self.plan = None
#         self.elite_plan = None
#         self.paid = False
#         self.plan_start_date = None
#         self.plan_expiry_date = None
#         self.save()

#     # ================= GET LIMITS =================
#     def get_plan_limits(self):
#         if not self.is_plan_active():
#             return 0, 0, 0

#         if self.plan:
#             return (
#                 self.plan.total_listing,
#                 self.plan.residential_limit,
#                 self.plan.commercial_limit
#             )

#         if self.elite_plan:
#             return (
#                 self.elite_plan.total_property_listings,
#                 999999,
#                 999999
#             )

#         return 0, 0, 0

#     # ================= SAVE =================
#     def save(self, *args, **kwargs):

#         # Hash password if not hashed
#         if self.password and not self.password.startswith('pbkdf2_'):
#             self.password = make_password(self.password)

#         # Generate agent code
#         if not self.agent_code:
#             prefix = "buysel"
#             name_part = self.username[:3].lower()
#             random_number = random.randint(1000, 9999)
#             code = f"{prefix}{name_part}{random_number}"

#             while AgentUserProfile.objects.filter(agent_code=code).exists():
#                 random_number = random.randint(1000, 9999)
#                 code = f"{prefix}{name_part}{random_number}"

#             self.agent_code = code

#         # Avatar fallback
#         if not self.profile_image and not self.avatar_url:
#             name = self.username[:1]  # first letter
#             self.avatar_url = f"https://ui-avatars.com/api/?name={name}&background=000000&color=ffffff&size=256"

#         super().save(*args, **kwargs)

#     # ================= PROFILE IMAGE =================
#     def get_profile_image(self):
#         if self.profile_image:
#             return self.profile_image.url
#         return self.avatar_url
    



# class AgentReview(models.Model):
#     id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    
#     agent = models.ForeignKey(
#         AgentUserProfile,
#         on_delete=models.CASCADE,
#         related_name="reviews"
#     )

#     user = models.ForeignKey(
#         "developer.UserCreate",
#         on_delete=models.CASCADE,
#         null=True,   # ✅ make optional
#         blank=True
#     )

#     rating = models.FloatField()
#     review = models.TextField()

#     likes = models.ManyToManyField(
#         "developer.UserCreate",
#         blank=True,
#         related_name="liked_reviews"
#     )

#     created_at = models.DateTimeField(auto_now_add=True)


class AgentReview(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    
    agent = models.ForeignKey(
        AgentUserProfile,
        on_delete=models.CASCADE,
        related_name="reviews"
    )

    user = models.ForeignKey(
        "developer.UserCreate",
        on_delete=models.CASCADE,
        null=True,
        blank=True
    )

    rating = models.FloatField()
    review = models.TextField(validators=[validate_safe_message])

    likes = models.ManyToManyField(
        "developer.UserCreate",
        blank=True,
        related_name="reviews"
    )

    created_at = models.DateTimeField(auto_now_add=True)

    def clean(self):
        if self.rating < 0 or self.rating > 5:
            raise ValidationError("Rating must be between 0 and 5.")

        if self.user and not self.user.id:
            raise ValidationError("Invalid user.")

    def save(self, *args, **kwargs):
        self.full_clean()  
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.agent} - {self.rating}"



# class PendingAgentRegistration(models.Model):

#     AGENT_TYPES = [
#         ('basic', 'Basic Agent'),
#         ('premium', 'Premium Agent'),
#         ('elite', 'Elite Agent'),
#     ]

#     STATUS_CHOICES = [
#         ("pending", "Pending"),
#         ("approved", "Approved"),
#         ("rejected", "Rejected"),
#     ]

#     id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

#     # Basic Details
#     full_name = models.CharField(max_length=150)
#     email = models.EmailField(unique=True)
#     phone_number = models.CharField(max_length=15)
#     password = models.CharField(max_length=128)

#     city = models.CharField(max_length=100)
#     pin_code = models.CharField(max_length=10)
#     address = models.TextField()

#     # Agent Type
#     agent_type = models.CharField(max_length=20, choices=AGENT_TYPES)

#     # Plans
#     premium_plan = models.ForeignKey(
#         PremiumPlan,
#         on_delete=models.SET_NULL,
#         null=True,
#         blank=True
#     )
#     elite_plan = models.ForeignKey(
#         ElitePlan,
#         on_delete=models.SET_NULL,
#         null=True,
#         blank=True
#     )

#     created_at = models.DateTimeField(auto_now_add=True)

#     # Status
#     status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')

#     # ✅ PLAN NAME HELPER
#     def get_plan_name(self):
#         if self.agent_type == "premium" and self.premium_plan:
#             return self.premium_plan.name
#         elif self.agent_type == "elite" and self.elite_plan:
#             return self.elite_plan.name
#         return "Basic"

#     # ✅ PLAN OBJECT HELPER (optional advanced use)
#     def get_plan(self):
#         if self.agent_type == "premium":
#             return self.premium_plan
#         elif self.agent_type == "elite":
#             return self.elite_plan
#         return None

#     def save(self, *args, **kwargs):

#         # ✅ Hash password
#         if self.password and not self.password.startswith('pbkdf2_'):
#             self.password = make_password(self.password)

#         super().save(*args, **kwargs)

#         # ✅ Create Agent after approval
#         if self.status == 'approved':
#             if not AgentUserProfile.objects.filter(email=self.email).exists():

#                 # Generate unique username
#                 base_username = self.email.split("@")[0]
#                 username = base_username
#                 counter = 1

#                 while AgentUserProfile.objects.filter(username=username).exists():
#                     username = f"{base_username}{counter}"
#                     counter += 1

#                 # Create Agent
#                 agent = AgentUserProfile.objects.create(
#                     username=username,
#                     email=self.email,
#                     phone_number=self.phone_number,
#                     whatsapp_number=self.phone_number,
#                     city=self.city,
#                     pin_code=int(self.pin_code) if self.pin_code else 0,
#                     address=self.address,
#                     agent_type=self.agent_type,
#                     is_agent=True,
#                     password=self.password
#                 )

#                 # ✅ Assign Plan
#                 if self.agent_type == "premium" and self.premium_plan:
#                     agent.activate_premium_plan(self.premium_plan)

#                 elif self.agent_type == "elite" and self.elite_plan:
#                     agent.activate_elite_plan(self.elite_plan)

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

   
    full_name = models.CharField(max_length=150, validators=[validate_agent_name])
    email = models.EmailField(unique=True, validators=[validate_email])
    phone_number = models.CharField(max_length=15, validators=[validate_phone_number])
    password = models.CharField(max_length=128, validators=[validate_password])

    city = models.CharField(max_length=100, validators=[validate_safe_text])
    pin_code = models.CharField(max_length=10, validators=[validate_pincode])
    address = models.TextField(validators=[validate_safe_message])

    
    agent_type = models.CharField(max_length=20, choices=AGENT_TYPES)

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

    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')

   
    def clean(self):

        if self.agent_type == "premium" and not self.premium_plan:
            raise ValidationError("Premium plan must be selected for premium agent.")

        if self.agent_type == "elite" and not self.elite_plan:
            raise ValidationError("Elite plan must be selected for elite agent.")

        if self.agent_type == "basic":
            if self.premium_plan or self.elite_plan:
                raise ValidationError("Basic agent should not have any plan.")

    def get_plan_name(self):
        if self.agent_type == "premium" and self.premium_plan:
            return self.premium_plan.name
        elif self.agent_type == "elite" and self.elite_plan:
            return self.elite_plan.name
        return "Basic"

    def get_plan(self):
        if self.agent_type == "premium":
            return self.premium_plan
        elif self.agent_type == "elite":
            return self.elite_plan
        return None

   
    def save(self, *args, **kwargs):

        self.full_clean()  

        # Hash password
        if self.password and not self.password.startswith('pbkdf2_'):
            self.password = make_password(self.password)

        super().save(*args, **kwargs)

    
        if self.status == 'approved':
            if not AgentUserProfile.objects.filter(email=self.email).exists():

              
                base_username = self.email.split("@")[0]
                username = base_username
                counter = 1

                while AgentUserProfile.objects.filter(username=username).exists():
                    username = f"{base_username}{counter}"
                    counter += 1

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

                if self.agent_type == "premium" and self.premium_plan:
                    agent.activate_premium_plan(self.premium_plan)

                elif self.agent_type == "elite" and self.elite_plan:
                    agent.activate_elite_plan(self.elite_plan)

    def __str__(self):
        return f"{self.full_name} ({self.status})"

                    
# class AgentContact(models.Model):
#     agent = models.ForeignKey(
#         AgentUserProfile,
#         on_delete=models.CASCADE,
#         related_name='contacts'
#     )

#     user = models.ForeignKey(
#         UserCreate,
#         on_delete=models.CASCADE,
#         related_name='sent_contacts',
#         null=True,
#         blank=True
#     )

#     first_name = models.CharField(max_length=100)
#     last_name = models.CharField(max_length=100)
#     contact_number = models.CharField(max_length=15)
#     email = models.EmailField()
#     message = models.TextField()

#     created_at = models.DateTimeField(auto_now_add=True)

#     def __str__(self):
#         return f"{self.first_name} -> {self.agent.username}"

class AgentContact(models.Model):
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False
    )

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

    first_name = models.CharField(
        max_length=100,
        validators=[validate_agent_name]
    )
    last_name = models.CharField(
        max_length=100,
        validators=[validate_name], blank=True,null=True
    )
    contact_number = models.CharField(
        max_length=15,
        validators=[validate_phone_number]
    )
    email = models.EmailField(
        validators=[validate_email]
    )
    message = models.TextField(
        validators=[validate_safe_message]
    )

    created_at = models.DateTimeField(auto_now_add=True)

   
    def clean(self):
        if self.user and self.agent and hasattr(self.agent, "email"):
            if self.user.email == self.agent.email:
                raise ValidationError("You cannot contact yourself.")

    
    def save(self, *args, **kwargs):
        self.full_clean()  
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.first_name} -> {self.agent.username}"



# class Inbox(models.Model):
#     name = models.CharField(max_length=50)
#     pin_code = models.CharField(max_length=50)
#     contact = models.CharField(max_length=50)
#     messages_text = models.TextField()
#     created_at = models.DateTimeField(auto_now_add=True)
#     is_read = models.BooleanField(default=False)  #
#     is_removed = models.BooleanField(default=False)

#     def __str__(self):
#         return f"Enquiry from {self.messages_text}"
    



# class ContactRequest(models.Model):
#     CONTACT_METHOD_CHOICES = [
#         ('email', 'Email'),
#         ('phone', 'Phone'),
#         ('both', 'Both'),
#     ]

#     first_name = models.CharField(max_length=100)
#     last_name = models.CharField(max_length=100)
#     contact_method = models.CharField(max_length=10, choices=CONTACT_METHOD_CHOICES)
#     email = models.EmailField()
#     phone = models.CharField(max_length=15, blank=True, null=True)
#     message = models.TextField(blank=True, null=True)
#     created_at = models.DateTimeField(auto_now_add=True)

#     def __str__(self):
#         return f"{self.first_name} {self.last_name} ({self.contact_method})"

class Inbox(models.Model):
    name = models.CharField(max_length=50, validators=[validate_agent_name])
    pin_code = models.CharField(max_length=50, validators=[validate_pincode])
    contact = models.CharField(max_length=50, validators=[validate_phone_number])
    messages_text = models.TextField(validators=[validate_safe_message])
    created_at = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)
    is_removed = models.BooleanField(default=False)

    # def clean(self):
    #     if not self.messages_text:
    #         raise ValidationError("Message cannot be empty.")

    def save(self, *args, **kwargs):
        self.full_clean()  
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Enquiry from {self.messages_text}"


class ContactRequest(models.Model):
    CONTACT_METHOD_CHOICES = [
        ('email', 'Email'),
        ('phone', 'Phone'),
        ('both', 'Both'),
    ]

    first_name = models.CharField(max_length=100, validators=[validate_agent_name])
    last_name = models.CharField(max_length=100, validators=[validate_agent_name])
    contact_method = models.CharField(max_length=10, choices=CONTACT_METHOD_CHOICES)
    email = models.EmailField(validators=[validate_email])
    phone = models.CharField(max_length=15, blank=True, null=True, validators=[validate_phone_number])
    message = models.TextField(blank=True, null=True, validators=[validate_safe_message])
    created_at = models.DateTimeField(auto_now_add=True)

    # def clean(self):
    #     if self.contact_method == "email" and not self.email:
    #         raise ValidationError("Email is required for email contact method.")

    #     if self.contact_method == "phone" and not self.phone:
    #         raise ValidationError("Phone is required for phone contact method.")

    #     if self.contact_method == "both":
    #         if not self.email or not self.phone:
    #             raise ValidationError("Both email and phone are required.")

    def save(self, *args, **kwargs):
        self.full_clean() 
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.first_name} {self.last_name} ({self.contact_method})"



# class AgentProperty(models.Model):

#     uuid = models.UUIDField(
#         default=uuid.uuid4,
#         editable=False,
#         db_index=True
#     )  
#     # ⚠️ DO NOT add unique=True until DB is cleaned

#     agent = models.ForeignKey(
#         AgentUserProfile,
#         on_delete=models.CASCADE,
#         related_name="properties"
#     )

#     property_hash_id = models.CharField(
#         max_length=100,
#         unique=True,
#         null=True,
#         blank=True
#     )

#     category = models.ForeignKey(
#         "developer.Category",
#         on_delete=models.CASCADE,
#         related_name="agent_properties"
#     )

#     subcategory = models.ForeignKey(
#         "developer.Subcategory",
#         on_delete=models.CASCADE,
#         related_name="agent_properties",
#         null=True,
#         blank=True
#     )

#     purpose = models.ForeignKey(
#         "developer.Purpose",
#         on_delete=models.CASCADE,
#         related_name="agent_properties"
#     )

#     label = models.CharField(max_length=255)
#     land_area = models.CharField(max_length=255)
#     sq_ft = models.FloatField(null=True, blank=True)
#     description = models.TextField()

#     amenities = models.ManyToManyField(
#         "developer.Amenities",
#         blank=True,
#         related_name="agent_properties"
#     )

#     image = CloudinaryField('image', folder="agent_properties", null=True, blank=True)

#     screenshot = CloudinaryField(
#         'image',
#         folder="agents_properties/screenshots",
#         blank=True,
#         null=True
#     )

#     perprice = models.CharField(max_length=50, blank=True, null=True)
#     price = models.CharField(max_length=50)

#     whatsapp = models.CharField(max_length=255, blank=True, null=True)
#     phone = models.CharField(max_length=255, blank=True, null=True)

#     location = models.TextField()
#     city = models.CharField(max_length=255)
#     pincode = models.CharField(max_length=50)
#     district = models.CharField(max_length=255)

#     land_mark = models.CharField(max_length=255, blank=True, null=True)

#     owner = models.CharField(max_length=255, blank=True, null=True)

#     taluk = models.CharField(max_length=255, blank=True, null=True)
#     village = models.CharField(max_length=255, blank=True, null=True)
#     state = models.CharField(max_length=255, blank=True, null=True)

#     paid = models.BooleanField(default=False)
#     notes = models.CharField(max_length=255, blank=True, null=True)

#     created_at = models.DateTimeField(auto_now_add=True)


#     def __str__(self):
#         return f"{self.label} - {self.city}"

#     # ================= SAVE LOGIC =================
#     def save(self, *args, **kwargs):
#         is_new = self.pk is None  # check if new property

#         super().save(*args, **kwargs)

#         if is_new:
#             agent = self.agent

#             # ✅ Increment property count
#             agent.properties_listed += 1
#             agent.save()

#             # ✅ Get plan limits
#             total_limit, _, _ = agent.get_plan_limits()

#             # 🔴 If no plan → block or notify
#             if total_limit == 0:
#                 Notification.objects.create(
#                     agent=agent,
#                     title="No Active Plan",
#                     message="You don’t have an active plan. Upgrade to add properties.",
#                     type="system"
#                 )
#                 return

#             # 🔔 Warning: Near limit (80%)
#             if agent.properties_listed >= int(0.8 * total_limit):
#                 if not Notification.objects.filter(
#                     agent=agent,
#                     title="Listing Limit Almost Reached"
#                 ).exists():

#                     Notification.objects.create(
#                         agent=agent,
#                         title="Listing Limit Almost Reached",
#                         message=f"You have used {agent.properties_listed}/{total_limit} listings.",
#                         type="usage"
#                     )

#             # 🔴 Limit reached
#             if agent.properties_listed >= total_limit:
#                 if not Notification.objects.filter(
#                     agent=agent,
#                     title="Listing Limit Reached"
#                 ).exists():

#                     Notification.objects.create(
#                         agent=agent,
#                         title="Listing Limit Reached",
#                         message="You have reached your property listing limit.",
#                         type="usage"
#                     )

from django.core.exceptions import ValidationError


class AgentProperty(models.Model):

    id = models.UUIDField(
        default=uuid.uuid4,
        editable=False,
        db_index=True,
        primary_key=True
    )

    agent = models.ForeignKey(
        AgentUserProfile,
        on_delete=models.CASCADE,
        related_name="properties"
    )

    property_hash_id = models.CharField(
        max_length=100,
        unique=True,
        null=True,
        blank=True
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

    label = models.CharField(
        max_length=255,
        validators=[validate_safe_text]
    )

    land_area = models.CharField(
        max_length=255,
        validators=[validate_safe_text]
    )

    sq_ft = models.FloatField(
        null=True,
        blank=True
    )

    description = models.TextField(
        validators=[validate_safe_message]
    )

    amenities = models.ManyToManyField(
        "developer.Amenities",
        blank=True,
        related_name="agent_properties"
    )

    image = CloudinaryField(
        'image',
        folder="agent_properties",
        null=True,
        blank=True
    )

    screenshot = CloudinaryField(
        'image',
        folder="agents_properties/screenshots",
        blank=True,
        null=True
    )

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

    # ✅ NEW FIELD
    deposit = models.CharField(
        max_length=50,
        blank=True,
        null=True,
        validators=[validate_safe_text]
    )

    whatsapp = models.CharField(
        max_length=255,
        blank=True,
        null=True,
        validators=[validate_phone_number]
    )

    phone = models.CharField(
        max_length=255,
        blank=True,
        null=True,
        validators=[validate_phone_number]
    )

    location = models.TextField(
        validators=[validate_safe_text]
    )

    city = models.CharField(
        max_length=255,
        validators=[validate_safe_text]
    )

    pincode = models.CharField(
        max_length=50,
        validators=[validate_pincode]
    )

    district = models.CharField(
        max_length=255,
        validators=[validate_safe_text]
    )

    land_mark = models.CharField(
        max_length=255,
        blank=True,
        null=True,
        validators=[validate_safe_text]
    )

    owner = models.CharField(
        max_length=255,
        blank=True,
        null=True,
        validators=[validate_safe_text]
    )

    taluk = models.CharField(
        max_length=255,
        blank=True,
        null=True,
        validators=[validate_safe_text]
    )

    village = models.CharField(
        max_length=255,
        blank=True,
        null=True,
        validators=[validate_safe_text]
    )

    state = models.CharField(
        max_length=255,
        blank=True,
        null=True,
        validators=[validate_safe_text]
    )

    paid = models.BooleanField(default=False)

    notes = models.CharField(
        max_length=255,
        blank=True,
        null=True,
        validators=[validate_safe_message]
    )

    created_at = models.DateTimeField(auto_now_add=True)

    def clean(self):

        purpose_name = ""

        if self.purpose:
            purpose_name = self.purpose.name.lower().strip()

        # =========================
        # SALE
        # =========================
        if purpose_name == "sale":

            if not self.price:
                raise ValidationError({
                    "price": "Price is required for sale"
                })

            if not self.perprice:
                raise ValidationError({
                    "perprice": "Per price is required for sale"
                })

        # =========================
        # RENT
        # =========================
        elif purpose_name == "rent":

            if not self.price:
                raise ValidationError({
                    "price": "Rent amount is required"
                })

            if not self.deposit:
                raise ValidationError({
                    "deposit": "Deposit is required for rent"
                })

            # remove perprice automatically
            self.perprice = None

        # =========================
        # LEASE
        # =========================
        elif purpose_name == "lease":

            if not self.price:
                raise ValidationError({
                    "price": "Price is required for lease"
                })

            # remove unwanted fields
            self.perprice = None
            self.deposit = None

    def __str__(self):
        return f"{self.label} - {self.city}"

    def save(self, *args, **kwargs):

        is_new = self.pk is None

        self.full_clean()

        super().save(*args, **kwargs)

        if is_new:

            agent = self.agent

            agent.properties_listed += 1
            agent.save()

            total_limit, _, _ = agent.get_plan_limits()

            if total_limit == 0:

                Notification.objects.create(
                    agent=agent,
                    title="No Active Plan",
                    message="You don’t have an active plan. Upgrade to add properties.",
                    type="system"
                )

                return

            if agent.properties_listed >= int(0.8 * total_limit):

                if not Notification.objects.filter(
                    agent=agent,
                    title="Listing Limit Almost Reached"
                ).exists():

                    Notification.objects.create(
                        agent=agent,
                        title="Listing Limit Almost Reached",
                        message=f"You have used {agent.properties_listed}/{total_limit} listings.",
                        type="usage"
                    )

            if agent.properties_listed >= total_limit:

                if not Notification.objects.filter(
                    agent=agent,
                    title="Listing Limit Reached"
                ).exists():

                    Notification.objects.create(
                        agent=agent,
                        title="Listing Limit Reached",
                        message="You have reached your property listing limit.",
                        type="usage"
                    )

# class AgentProperty(models.Model):

#     uuid = models.UUIDField(
#         default=uuid.uuid4,
#         editable=False,
#         db_index=True
#     )

#     agent = models.ForeignKey(
#         AgentUserProfile,
#         on_delete=models.CASCADE,
#         related_name="properties"
#     )

#     property_hash_id = models.CharField(
#         max_length=100,
#         unique=True,
#         null=True,
#         blank=True
#     )

#     category = models.ForeignKey(
#         "developer.Category",
#         on_delete=models.CASCADE,
#         related_name="agent_properties"
#     )

#     subcategory = models.ForeignKey(
#         "developer.Subcategory",
#         on_delete=models.CASCADE,
#         related_name="agent_properties",
#         null=True,
#         blank=True
#     )

#     purpose = models.ForeignKey(
#         "developer.Purpose",
#         on_delete=models.CASCADE,
#         related_name="agent_properties"
#     )

#     label = models.CharField(max_length=255, validators=[validate_safe_text])
#     land_area = models.CharField(max_length=255, validators=[validate_safe_text])
#     sq_ft = models.FloatField(null=True, blank=True)

#     description = models.TextField(validators=[validate_safe_message])

#     amenities = models.ManyToManyField(
#         "developer.Amenities",
#         blank=True,
#         related_name="agent_properties"
#     )

#     image = CloudinaryField('image', folder="agent_properties", null=True, blank=True)

#     screenshot = CloudinaryField(
#         'image',
#         folder="agents_properties/screenshots",
#         blank=True,
#         null=True
#     )

#     perprice = models.CharField(
#         max_length=50,
#         blank=True,
#         null=True,
#         validators=[validate_safe_text]
#     )

#     price = models.CharField(
#         max_length=50,
#         validators=[validate_safe_text]
#     )

#     whatsapp = models.CharField(
#         max_length=255,
#         blank=True,
#         null=True,
#         validators=[validate_phone_number]
#     )

#     phone = models.CharField(
#         max_length=255,
#         blank=True,
#         null=True,
#         validators=[validate_phone_number]
#     )

#     location = models.TextField(validators=[validate_safe_text])

#     city = models.CharField(max_length=255, validators=[validate_safe_text])

#     pincode = models.CharField(
#         max_length=50,
#         validators=[validate_pincode]
#     )

#     district = models.CharField(max_length=255, validators=[validate_safe_text])

#     land_mark = models.CharField(
#         max_length=255,
#         blank=True,
#         null=True,
#         validators=[validate_safe_text]
#     )

#     owner = models.CharField(
#         max_length=255,
#         blank=True,
#         null=True,
#         validators=[validate_safe_text]
#     )

#     taluk = models.CharField(
#         max_length=255,
#         blank=True,
#         null=True,
#         validators=[validate_safe_text]
#     )

#     village = models.CharField(
#         max_length=255,
#         blank=True,
#         null=True,
#         validators=[validate_safe_text]
#     )

#     state = models.CharField(
#         max_length=255,
#         blank=True,
#         null=True,
#         validators=[validate_safe_text]
#     )

#     paid = models.BooleanField(default=False)

#     notes = models.CharField(
#         max_length=255,
#         blank=True,
#         null=True,
#         validators=[validate_safe_message]
#     )

#     created_at = models.DateTimeField(auto_now_add=True)

#     # def clean(self):

#     #     # Phone / WhatsApp optional but validate if given
#     #     if self.phone and not self.phone.isdigit():
#     #         raise ValidationError("Phone must contain only digits.")

#     #     if self.whatsapp and not self.whatsapp.isdigit():
#     #         raise ValidationError("WhatsApp must contain only digits.")

#     #     # Ensure at least one contact method
#     #     if not self.phone and not self.whatsapp:
#     #         raise ValidationError("At least one contact number is required.")


#     def __str__(self):
#         return f"{self.label} - {self.city}"

    
#     def save(self, *args, **kwargs):
#         is_new = self.pk is None

#         self.full_clean()  

#         super().save(*args, **kwargs)

#         if is_new:
#             agent = self.agent

#             agent.properties_listed += 1
#             agent.save()

           
#             total_limit, _, _ = agent.get_plan_limits()

#             if total_limit == 0:
#                 Notification.objects.create(
#                     agent=agent,
#                     title="No Active Plan",
#                     message="You don’t have an active plan. Upgrade to add properties.",
#                     type="system"
#                 )
#                 return
#             if agent.properties_listed >= int(0.8 * total_limit):
#                 if not Notification.objects.filter(
#                     agent=agent,
#                     title="Listing Limit Almost Reached"
#                 ).exists():

#                     Notification.objects.create(
#                         agent=agent,
#                         title="Listing Limit Almost Reached",
#                         message=f"You have used {agent.properties_listed}/{total_limit} listings.",
#                         type="usage"
#                     )

#             if agent.properties_listed >= total_limit:
#                 if not Notification.objects.filter(
#                     agent=agent,
#                     title="Listing Limit Reached"
#                 ).exists():

#                     Notification.objects.create(
#                         agent=agent,
#                         title="Listing Limit Reached",
#                         message="You have reached your property listing limit.",
#                         type="usage"
#                     )


# class AgentPropertyFieldValue(models.Model):
#     property = models.ForeignKey(
#         "AgentProperty",
#         on_delete=models.CASCADE,
#         related_name="field_values"
#     )

#     field = models.ForeignKey(
#         "developer.SubcategoryField",
#         on_delete=models.CASCADE
#     )

#     value = models.CharField(max_length=255)

#     def __str__(self):
#         return f"{self.property.label} - {self.field.field_name}"



# class AgentPropertyImage(models.Model):
#         property = models.ForeignKey(
#             "AgentProperty",
#             on_delete=models.CASCADE,
#             related_name="images"
#         )

#         image = CloudinaryField("image", folder="Agentproperties/multiple")

#         def __str__(self):
#             return f"Image for {self.property.label}"


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

    value = models.CharField(
        max_length=255,
        validators=[validate_safe_text]
    )

    def clean(self):
        if not self.value:
            raise ValidationError("Value cannot be empty.")

    
    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.property.label} - {self.field.field_name}"


class AgentPropertyImage(models.Model):
    property = models.ForeignKey(
        "AgentProperty",
        on_delete=models.CASCADE,
        related_name="images"
    )

    image = CloudinaryField("image", folder="Agentproperties/multiple")

    def clean(self):
        if not self.image:
            raise ValidationError("Image is required.")

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Image for {self.property.label}"
        

# class AgentPropertySellingPoint(models.Model):
#     property = models.ForeignKey(
#         "AgentProperty",  # string reference instead of direct class
#         on_delete=models.CASCADE,
#         related_name="selling_points"
#     )
#     point = models.CharField(max_length=255)

#     def __str__(self):
#         return self.point


# class AgentPropertyLandmark(models.Model):
#     property = models.ForeignKey(
#         "AgentProperty",  # string reference
#         on_delete=models.CASCADE,
#         related_name="landmarks"
#     )
#     name = models.CharField(max_length=255)
#     distance = models.CharField(max_length=50, blank=True, null=True)

#     def __str__(self):
#         return self.name


class AgentPropertySellingPoint(models.Model):
    property = models.ForeignKey(
        "AgentProperty",
        on_delete=models.CASCADE,
        related_name="selling_points"
    )

    point = models.CharField(
        max_length=255,
        validators=[validate_safe_text]
    )
    def clean(self):
        if not self.point:
            raise ValidationError("Selling point cannot be empty.")

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)

    def __str__(self):
        return self.point


class AgentPropertyLandmark(models.Model):
    property = models.ForeignKey(
        "AgentProperty",
        on_delete=models.CASCADE,
        related_name="landmarks"
    )

    name = models.CharField(
        max_length=255,
        validators=[validate_safe_text]
    )

    distance = models.CharField(
        max_length=50,
        blank=True,
        null=True,
        validators=[validate_safe_text]
    )

    def clean(self):
        if not self.name:
            raise ValidationError("Landmark name cannot be empty.")

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name
    

# class AgentPropertyEnquiry(models.Model):

#     agent_property = models.ForeignKey(
#         "AgentProperty",
#         on_delete=models.CASCADE,
#         related_name="enquiries"
#     )

#     user = models.ForeignKey(
#         UserCreate,
#         on_delete=models.CASCADE,
#         related_name="agent_property_enquiries"  # ✅ FIXED
#     )

#     name = models.CharField(max_length=150)
#     email = models.EmailField()
#     phone = models.CharField(max_length=15)
#     message = models.TextField(blank=True)

#     created_at = models.DateTimeField(auto_now_add=True)

# class Notification(models.Model):

#     id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)  # ✅ ADD THIS

#     NOTIFICATION_TYPE = (
#         ("expiry", "Expiry"),
#         ("usage", "Usage"),
#         ("system", "System"),
#         ("property", "Property"),
#     )

#     agent = models.ForeignKey(
#         "agents.AgentUserProfile",
#         on_delete=models.CASCADE,
#         null=True,
#         blank=True,
#         related_name="notifications"
#     )

#     user = models.ForeignKey(
#         "developer.UserProfile",
#         on_delete=models.CASCADE,
#         null=True,
#         blank=True,
#         related_name="notifications"
#     )

#     title = models.CharField(max_length=255)
#     message = models.TextField()

#     type = models.CharField(max_length=20, choices=NOTIFICATION_TYPE)

#     is_read = models.BooleanField(default=False)

#     created_at = models.DateTimeField(auto_now_add=True)

#     def __str__(self):
#         if self.agent:
#             return f"Agent: {self.agent.username} - {self.title}"
#         if self.user:
#             return f"User: {self.user.username} - {self.title}"
#         return self.title

class AgentPropertyEnquiry(models.Model):
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False
    )

    property = models.ForeignKey(
        "AgentProperty",
        on_delete=models.CASCADE,
        related_name="enquiries"
    )

    user = models.ForeignKey(
        UserCreate,
        on_delete=models.CASCADE,
        related_name="agent_property_enquiries"
    )

    name = models.CharField(
        max_length=150,
        validators=[validate_agent_name]
    )

    email = models.EmailField(
        validators=[validate_email]
    )

    phone = models.CharField(
        max_length=15,
        validators=[validate_phone_number]
    )

    message = models.TextField(
        blank=True,
        validators=[validate_safe_message]
    )

    created_at = models.DateTimeField(auto_now_add=True)

    def clean(self):
        if not self.name:
            raise ValidationError("Name is required.")

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)


class Notification(models.Model):

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    NOTIFICATION_TYPE = (
        ("expiry", "Expiry"),
        ("usage", "Usage"),
        ("system", "System"),
        ("property", "Property"),
    )

    agent = models.ForeignKey(
        "agents.AgentUserProfile",
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name="notifications"
    )

    user = models.ForeignKey(
        "developer.UserProfile",
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name="notifications"
    )

    title = models.CharField(
        max_length=255,
        validators=[validate_safe_text]
    )

    message = models.TextField(
        validators=[validate_safe_message]
    )

    type = models.CharField(
        max_length=20,
        choices=NOTIFICATION_TYPE
    )

    is_read = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True)

    # def clean(self):
    #     if not self.agent and not self.user:
    #         raise ValidationError("Notification must have either an agent or a user.")

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)

    def __str__(self):
        if self.agent:
            return f"Agent: {self.agent.username} - {self.title}"
        if self.user:
            return f"User: {self.user.username} - {self.title}"
        return self.title


# class AgentContactMessage(models.Model):

#     STATUS_CHOICES = [
#         ("pending", "Pending"),
#         ("replied", "Replied"),
#     ]

#     id = models.UUIDField(
#         primary_key=True,
#         default=uuid.uuid4,
#         editable=False
#     )

#     agent = models.ForeignKey(
#         AgentUserProfile,
#         on_delete=models.CASCADE,
#         related_name="contact_messages"
#     )

#     name = models.CharField(
#         max_length=255,
#         validators=[
#             validate_agent_name,
#             validate_safe_text
#         ]
#     )

#     message = models.TextField(
#         validators=[
#             validate_safe_message
#         ]
#     )

#     status = models.CharField(
#         max_length=20,
#         choices=STATUS_CHOICES,
#         default="pending"
#     )

#     replied_at = models.DateTimeField(
#         null=True,
#         blank=True
#     )
#     created_at = models.DateTimeField(
#         auto_now_add=True
#     )

#     updated_at = models.DateTimeField(
#         auto_now=True
#     )

#     class Meta:
#         ordering = ["-created_at"]

#     def clean(self):

#         super().clean()

#         if not self.name:
#             raise ValidationError({
#                 "name": "Name is required"
#             })

#         validate_agent_name(self.name)

#         validate_safe_text(self.name)

#         if not self.message:
#             raise ValidationError({
#                 "message": "Message is required"
#             })

#         validate_safe_message(self.message)

#         if self.status not in [
#             "pending",
#             "replied"
#         ]:
#             raise ValidationError({
#                 "status": "Invalid status"
#             })

#     def save(self, *args, **kwargs):

#         self.full_clean()

#         super().save(*args, **kwargs)

#     def __str__(self):

#         return (
#             f"{self.name} - "
#             f"{self.agent.username}"
#         )



class AgentContactMessage(models.Model):

    STATUS_CHOICES = [
        ("pending", "Pending"),
        ("replied", "Replied"),
    ]

    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False
    )

    agent = models.ForeignKey(
        AgentUserProfile,
        on_delete=models.CASCADE,
        related_name="contact_messages"
    )

    agent_name = models.CharField(
        max_length=255,
        null=True,
        blank=True,
        validators=[
            validate_agent_name,
            validate_safe_text
        ]
    )

    agent_email = models.EmailField(
        null=True,
        blank=True,
        validators=[
            validate_email
        ]
    )

    agent_phone = models.CharField(
        max_length=15,
        null=True,
        blank=True,
        validators=[
            validate_phone_number
        ]
    )

    agent_whatsapp = models.CharField(
        max_length=15,
        null=True,
        blank=True,
        validators=[
            validate_phone_number
        ]
    )

    name = models.CharField(
        max_length=255,
        validators=[
            validate_agent_name,
            validate_safe_text
        ]
    )

    message = models.TextField(
        validators=[
            validate_safe_message
        ]
    )


    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default="pending"
    )

    replied_at = models.DateTimeField(
        null=True,
        blank=True
    )
    created_at = models.DateTimeField(
        auto_now_add=True
    )

    updated_at = models.DateTimeField(
        auto_now=True
    )

    class Meta:
        ordering = ["-created_at"]

    def clean(self):

        super().clean()

        if not self.name:
            raise ValidationError({
                "name": "Name is required"
            })

        if not self.message:
            raise ValidationError({
                "message": "Message is required"
            })

        if self.status not in [
            "pending",
            "replied"
        ]:
            raise ValidationError({
                "status": "Invalid status"
            })

    def save(self, *args, **kwargs):
        if self.agent:

            self.agent_name = (
                self.agent.username
            )

            self.agent_email = (
                self.agent.email
            )

            self.agent_phone = (
                self.agent.phone_number
            )

            self.agent_whatsapp = (
                self.agent.whatsapp_number
            )

        self.full_clean()

        super().save(*args, **kwargs)

    def __str__(self):

        return (
            f"{self.agent_name} - "
            f"{self.name}"
        )
    