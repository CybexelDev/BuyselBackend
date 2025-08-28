from django.db import models

import uuid
from cloudinary.models import CloudinaryField
import cloudinary.uploader
from playwright.sync_api import sync_playwright
import time
# Create your models here.
class Login(models.Model):
    username = models.CharField(max_length=50)
    password = models.CharField(max_length=50)

    def __str__(self):
        return self.username

class UserProfile(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    login = models.OneToOneField(Login, on_delete=models.CASCADE)  # Link to Login model
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
    
