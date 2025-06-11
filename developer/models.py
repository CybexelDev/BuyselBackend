from django.db import models
import uuid
from cloudinary.models import CloudinaryField
import cloudinary.uploader
from playwright.sync_api import sync_playwright
import time
from django.db.models.signals import post_save
from django.dispatch import receiver

# Create your models here.
from django.contrib.auth.models import AbstractUser

class CustomUser(AbstractUser):
    rate_limit = models.IntegerField(default=0)
    last_failed_login = models.DateTimeField(null=True, blank=True)



class MainCategory(models.Model):
    SALE = 'Sale'
    RENT = 'Rent'
    RESELL = 'Resell'
    LEASE = 'Lease'
    CATEGORY_CHOICES = [
        (SALE, 'Sale'),
        (RENT, 'Rent'),
        (RESELL, 'Resell'),
        (LEASE, 'Lease'),
    ]

    catgory = models.CharField(max_length=50, choices=CATEGORY_CHOICES)
    
    def __str__(self):
        return self.catgory


class House(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    AVAILABLE = 'Available'
    SOLD = 'Sold'
    HOUSE_STATUS_CHOICES = [
        (AVAILABLE, 'Available'),
        (SOLD, 'Sold'),
    ]
    MALE = 'male'
    FEMALE = 'female'
    MIXED = 'mixed'
    HOUSE_GENDER_CHOICES =[ 
        (MALE ,'male'),
        (FEMALE, 'female'),
        (MIXED, 'mixed'),
    ]
    Caption = models.CharField(max_length=100)
    category = models.ForeignKey('MainCategory', on_delete=models.CASCADE)
    total_land = models.CharField(max_length=50, null=True, blank=True)
    price = models.CharField(max_length=50)
    house_area = models.CharField(max_length=50)
    address = models.TextField(max_length=500)
    description = models.TextField(max_length=500)
    furnished = models.BooleanField(default=False, verbose_name="Is Furnished?")
    land_mark = models.TextField(max_length=100)
    Bedroom = models.CharField(max_length=10)
    Bathroom = models.CharField(max_length=10)
    Kitchen = models.BooleanField(default=False)
    allowed_persons = models.IntegerField(blank=True, null=True, verbose_name="Allowed Persons")
    sequrity_deposit = models.CharField(max_length=50, null=True, blank=True)
    Time_perioud = models.CharField(max_length=50, blank=True, verbose_name="Time Period")
    gender = models.CharField(max_length=50, choices=HOUSE_GENDER_CHOICES, default=MALE)
    location = models.TextField(max_length=200, null=True, blank=True)
    username = models.CharField(max_length=50)
    contact = models.CharField(max_length=20)
    status = models.CharField(max_length=10, choices=HOUSE_STATUS_CHOICES, default=AVAILABLE)
    disabled = models.BooleanField(default=False, verbose_name="Is Disabled?")
    image = CloudinaryField('image', folder="houses") 
    screenshot = CloudinaryField('image', folder="screenshot", null=True, blank= True) 
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.Caption} - {self.username}"
    

class HouseImage(models.Model):
    house = models.ForeignKey(House, related_name='images', on_delete=models.CASCADE)
    image = CloudinaryField('image', folder="houses")   # Multiple images for the house
   
    def __str__(self):
        return f"Image for {self.house.Caption}"  # This will be the main image



class Land(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    AVAILABLE = 'Available'
    SOLD = 'Sold'
    HOUSE_STATUS_CHOICES = [
        (AVAILABLE, 'Available'),
        (SOLD, 'Sold'),
    ]
    Caption = models.CharField(max_length=100)
    category = models.ForeignKey(MainCategory, on_delete=models.CASCADE)
    total_land = models.CharField(max_length=50, null=True, blank=True)
    price = models.CharField(max_length=50)
    space_area = models.CharField(max_length=50)
    address = models.TextField(max_length=500)
    description = models.TextField(max_length=500)
    
    land_mark = models.TextField(max_length=100)
   
    sequrity_deposit = models.CharField(max_length=50, null=True, blank=True)
    Time_perioud = models.CharField(max_length=50, blank=True, verbose_name="Time Period")
    location = models.TextField(max_length=200, null=True, blank=True)
    username = models.CharField(max_length=50)
    contact = models.CharField(max_length=20)
    status = models.CharField(max_length=10, choices=HOUSE_STATUS_CHOICES, default=AVAILABLE)
    disabled = models.BooleanField(default=False)
    image = CloudinaryField('image', folder="lands") 
    screenshot = CloudinaryField('image', folder="screenshot", null=True, blank= True) 
    created_at = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return f"{self.Caption} - {self.username}"
    

    
  

class LandImage(models.Model):
    land = models.ForeignKey(Land, related_name='images', on_delete=models.CASCADE)
    image = CloudinaryField('image', folder="lands")   # Multiple images for the house

    def __str__(self):
        return f"Image for {self.land.Caption}"


class Commercial(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    AVAILABLE = 'Available'
    SOLD = 'Sold'
    HOUSE_STATUS_CHOICES = [
        (AVAILABLE, 'Available'),
        (SOLD, 'Sold'),
    ]
    Caption = models.CharField(max_length=100)
    category = models.ForeignKey(MainCategory, on_delete=models.CASCADE)
    total_land = models.CharField(max_length=50, null=True, blank=True)
    price = models.CharField(max_length=50)
    address = models.TextField(max_length=500)
    description = models.TextField(max_length=500)
    land_mark = models.TextField(max_length=100)
    
    sequrity_deposit = models.CharField(max_length=50, null=True, blank=True)
    Time_perioud = models.CharField(max_length=50, blank=True, verbose_name="Time Period")
    location = models.TextField(max_length=200, null=True, blank=True)
    username = models.CharField(max_length=50)
    contact = models.CharField(max_length=20)
    status = models.CharField(max_length=10, choices=HOUSE_STATUS_CHOICES, default=AVAILABLE)
    disabled = models.BooleanField(default=False)
    amenities = models.TextField(max_length=500)
    image = CloudinaryField('image', folder="commercial") 
    screenshot = CloudinaryField('image', folder="screenshot", null=True, blank= True) 
    created_at = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return f"{self.Caption} - {self.username}"
    
    
  

class CommercialImage(models.Model):
    commercial = models.ForeignKey(Commercial, related_name='images', on_delete=models.CASCADE)
    image = CloudinaryField('image', folder="commercial")  # Multiple images for the house

    def __str__(self):
        return f"Image for {self.commercial.Caption}"


class OffPlan(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    AVAILABLE = 'Available'
    SOLD = 'Sold'
    HOUSE_STATUS_CHOICES = [
        (AVAILABLE, 'Available'),
        (SOLD, 'Sold'),
    ]
    Caption = models.CharField(max_length=100)
    category = models.ForeignKey(MainCategory, on_delete=models.CASCADE)
    total_land = models.CharField(max_length=50, null=True, blank=True)
    price = models.CharField(max_length=50)
    address = models.TextField(max_length=500)
    description = models.TextField(max_length=500)
    rooms = models.CharField(max_length=10)
    land_mark = models.TextField(max_length=100)
    
    location = models.TextField(max_length=200, null=True, blank=True)
    username = models.CharField(max_length=50)
    contact = models.CharField(max_length=20)
    status = models.CharField(max_length=10, choices=HOUSE_STATUS_CHOICES, default=AVAILABLE)
    disabled = models.BooleanField(default=False)
    image = CloudinaryField('image', folder="offplan")  # This will be the main image
    screenshot = CloudinaryField('image', folder="screenshot", null=True, blank= True) 
    created_at = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return f"{self.Caption} - {self.username}"

   


class OffplanImage(models.Model):
    offplan = models.ForeignKey(OffPlan, related_name='images', on_delete=models.CASCADE)
    image = CloudinaryField('image', folder="offplan") 

    def __str__(self):
        return f"Image for {self.offplan.Caption}"


class AgentForm(models.Model):
    name = models.CharField(max_length=100)
    email = models.CharField(max_length=50)
    address = models.TextField()
    phone_number = models.CharField(max_length=12)
    Dealings = models.CharField(max_length=100)
    image = models.ImageField(upload_to='agent-image')

    def __str__(self):
        return self.name
    
class Propertylist(models.Model):
    property_name =models.CharField(max_length=100)
    locations = models.CharField(max_length=100)
    price = models.CharField(max_length=50)
    about_the_property = models.TextField()
    image = models.ImageField(upload_to='property-image')

    def __str__(self):
        return self.property_name

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
    image = models.ImageField(upload_to='blogs')
   


    def __str__(self):
        return self.blog_head