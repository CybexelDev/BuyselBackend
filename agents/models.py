from django.db import models

import uuid
from cloudinary.models import CloudinaryField
import cloudinary.uploader
from playwright.sync_api import sync_playwright
import time
from developer .models import *


class UserProfile(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    login = models.OneToOneField(Premium, on_delete=models.CASCADE)  # Link to Login model
    phone_number = models.CharField(max_length=15)
    address = models.TextField()
    profile_image = CloudinaryField('image', folder="agenthouses") 
    pin_code = models.IntegerField()  # Specific for agent
    email = models.EmailField(max_length=50)
    is_agent = models.BooleanField(default=False)  # Flag to determine if the user is an agent
    messages = models.ManyToManyField('Inbox', related_name='agents', blank=True)  # Messages related to the user
    paid = models.BooleanField(default=False)

    def __str__(self):
        return self.login.username




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

    label = models.CharField(max_length=100)
    land_area = models.CharField(max_length=100)
    sq_ft = models.CharField(max_length=10, null=True, blank=True)
    description = models.CharField(max_length=1000)
    amenities = models.CharField(max_length=100, null=True, blank=True)
    image = CloudinaryField('image', folder="properties")  # Main/cover image

    perprice = models.CharField(max_length=10, blank=True, null=True)
    price = models.CharField(max_length=10)
    whatsapp = models.CharField(max_length=100)
    phone = models.CharField(max_length=100)
    location = models.CharField(max_length=100)
    city = models.CharField(max_length=100)
    pincode = models.CharField(max_length=10)
    district = models.CharField(max_length=100)
    land_mark = models.CharField(max_length=100, blank=True, null=True)

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


