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
class CustomUser(AbstractUser):
    rate_limit = models.IntegerField(default=0)
    last_failed_login = models.DateTimeField(null=True, blank=True)





class AgentForm(models.Model):
    name = models.CharField(max_length=100)
    email = models.CharField(max_length=50, null=True, blank= True)
    address = models.TextField()
    phone_number = models.CharField(max_length=12)
    Dealings = models.CharField(max_length=100)
    image = models.ImageField(upload_to='agent-image')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name
    
class Propertylist(models.Model):
    categories = models.CharField(max_length=100)
    purposes = models.CharField(max_length=100)
    label = models.CharField(max_length=100)
    land_area = models.CharField(max_length=100, null=True, blank= True)
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

class Category(models.Model):
    name = models.CharField(max_length=100)    

    def __str__(self):
        return self.name

class Purpose(models.Model):
    name = models.CharField(max_length=100)    

    def __str__(self):
        return self.name
       





class Property(models.Model):
    category = models.ForeignKey("Category", on_delete=models.CASCADE)
    purpose = models.ForeignKey("Purpose", on_delete=models.CASCADE)
    label = models.CharField(max_length=100)
    land_area = models.CharField(max_length=100)
    sq_ft = models.CharField(max_length=10, null=True, blank=True)
    description = models.CharField(max_length=1000)
    amenities = models.CharField(max_length=100, null=True, blank=True)
    image = CloudinaryField('image', folder="propertice")  # Main/cover image
    perprice = models.CharField(max_length=10, blank=True, null=True)
    price = models.CharField(max_length=10)
    owner = models.CharField(max_length=100)
    whatsapp = models.CharField(max_length=100)
    phone = models.CharField(max_length=100)
    location = models.CharField(max_length=100)
    city = models.CharField(max_length=100)
    pincode = models.CharField(max_length=10)
    district = models.CharField(max_length=100)
    land_mark = models.CharField(max_length=100, blank=True, null=True)
    paid = models.CharField(max_length=100)
    added_by = models.CharField(max_length=100, blank=True, null=True)

    # Expiry fields
    created_at = models.DateTimeField(auto_now_add=True)  # auto set when created
    duration_days = models.PositiveIntegerField(default=30)
  # number of days active

    def is_expired(self):
        """Check if the property has expired"""
        expiry_date = self.created_at + timedelta(days=self.duration_days)
        return timezone.now() > expiry_date

    def save(self, *args, **kwargs):
        """Auto-move expired properties into ExpiredProperty table"""
        if self.pk and self.is_expired():
            # Move to expired model
            expired_prop = ExpiredProperty.objects.create(
                category=self.category,
                purpose=self.purpose,
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
                land_mark=self.land_mark,
                paid=self.paid,
                added_by=self.added_by,
                created_at=self.created_at,
                duration_days=self.duration_days,
            )

            # 🔹 Copy related PropertyImage instances
            for img in self.images.all():  # 'images' is related_name
                PropertyImage.objects.create(
                    expired_property=expired_prop,
                    image=img.image
                )

            super(Property, self).delete()  # Delete from active properties
        else:
            super(Property, self).save(*args, **kwargs)


    def __str__(self):
        return f"{self.label} ({'Expired' if self.is_expired() else 'Active'})"

 

class ExpiredProperty(models.Model):
    category = models.ForeignKey("Category", on_delete=models.CASCADE)
    purpose = models.ForeignKey("Purpose", on_delete=models.CASCADE)
    label = models.CharField(max_length=100)
    land_area = models.CharField(max_length=100)
    sq_ft = models.CharField(max_length=10, null=True, blank=True)
    description = models.CharField(max_length=1000)
    amenities = models.CharField(max_length=100, null=True, blank=True)
    image = CloudinaryField('image', folder="propertice")
    perprice = models.CharField(max_length=10, blank=True, null=True)
    price = models.CharField(max_length=10)
    owner = models.CharField(max_length=100)
    whatsapp = models.CharField(max_length=100)
    phone = models.CharField(max_length=100)
    location = models.CharField(max_length=100)
    city = models.CharField(max_length=100)
    pincode = models.CharField(max_length=10)
    district = models.CharField(max_length=100)
    land_mark = models.CharField(max_length=100, blank=True, null=True)
    paid = models.CharField(max_length=100)
    added_by = models.CharField(max_length=100, blank=True, null=True)

    # Keep expiry details
    created_at = models.DateTimeField()
    duration_days = models.PositiveIntegerField()

    def is_active_again(self):
        expiry_date = self.created_at + timedelta(days=self.duration_days)
        return timezone.now() <= expiry_date

    def save(self, *args, **kwargs):
        """If duration is updated and property is active again, move it back"""
        if self.pk and self.is_active_again():
            # Move back to Property
            active_prop = Property.objects.create(
                category=self.category,
                purpose=self.purpose,
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
                land_mark=self.land_mark,
                paid=self.paid,
                added_by=self.added_by,
                created_at=self.created_at,
                duration_days=self.duration_days,
            )

            # 🔹 Copy related PropertyImage instances
            for img in self.images.all():
                PropertyImage.objects.create(
                    property=active_prop,
                    image=img.image
                )

            super(ExpiredProperty, self).delete()  # remove from expired
        else:
            super(ExpiredProperty, self).save(*args, **kwargs)

    def __str__(self):
        return f"Expired: {self.label}"

class PropertyImage(models.Model):
    property = models.ForeignKey("Property", on_delete=models.CASCADE, related_name="images", null=True, blank=True)
    expired_property = models.ForeignKey("ExpiredProperty", on_delete=models.CASCADE, related_name="images", null=True, blank=True)

    image = CloudinaryField("image", folder="propertice/multiple")

    def __str__(self):
        if self.property:
            return f"Image for {self.property}"
        elif self.expired_property:
            return f"Expired image for {self.expired_property}"
        return "Orphan image"







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

    created_at = models.DateTimeField()
    duration_days = models.PositiveIntegerField(default=365, null=True, blank=True)

    def is_expired(self):
        expiry_date = self.created_at + timedelta(days=self.duration_days)
        return timezone.now() > expiry_date

    def save(self, *args, **kwargs):
        """Move to ExpiredPremium if expired"""
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
            # Move related images
            for img in self.images.all():
                PremiumImage.objects.create(
                    expired_premium=expired,
                    image=img.image
                )
            super(Premium, self).delete()
        else:
            super(Premium, self).save(*args, **kwargs)

    def __str__(self):
        return f"{self.name} ({'Expired' if self.is_expired() else 'Active'})"


   
class ExpiredPremium(models.Model):
    name = models.CharField(max_length=100)
    speacialised =  models.CharField(max_length=100)
    phone =  models.CharField(max_length=100)
    whatsapp =  models.CharField(max_length=100,  blank=True, null=True)
    email =  models.CharField(max_length=100, blank=True, null=True)
    location =  models.CharField(max_length=200)
    city =  models.CharField(max_length=100)
    pincode =  models.CharField(max_length=100) 
    username = models.CharField(max_length=100)
    password =  models.CharField(max_length=100)

    image = CloudinaryField('buysel', folder="premium_agents")

     # New fields for expiry
    created_at = models.DateTimeField()
    duration_days = models.PositiveIntegerField(default=365, null=True, blank=True)  # default 30 days


    def is_active_again(self):
        expiry_date = self.created_at + timedelta(days=self.duration_days)
        return timezone.now() <= expiry_date

    def save(self, *args, **kwargs):
        """If duration is updated and property is active again, move it back"""
        if self.pk and self.is_active_again():
            # Move back to Premium
            active_premium = Premium.objects.create(
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
                image=self.image,  # ✅ use the existing image value
                created_at=self.created_at,
                duration_days=self.duration_days,
            )

            # Copy related images
            for img in self.images.all():
                PremiumImage.objects.create(
                    premium=active_premium,
                    image=img.image
                )

            super(ExpiredPremium, self).delete()  # remove from expired
        else:
            super(ExpiredPremium, self).save(*args, **kwargs)

class PremiumImage(models.Model):
    premium = models.ForeignKey("premium", on_delete=models.CASCADE, related_name="images", null=True, blank=True)
    expired_premium = models.ForeignKey("ExpiredPremium", on_delete=models.CASCADE, related_name="images", null=True, blank=True)

    image = CloudinaryField("image", folder="premium/multiple")

    def __str__(self):
        if self.premium:
            return f"Image for {self.premium}"
        elif self.expired_premium:
            return f"Expired image for {self.expired_premium}"
        return "Orphan image"






class Agents(models.Model):
    agentsname = models.CharField(max_length=100)
    agentsspeacialised =  models.CharField(max_length=100)
    agentsphone =  models.CharField(max_length=100)
    agentswhatsapp =  models.CharField(max_length=100,  blank=True, null=True)
    agentsemail =  models.CharField(max_length=100, blank=True, null=True)
    agentslocation =  models.CharField(max_length=200)
    agentsimage = CloudinaryField('buysel', folder="agents")

     # New fields for expiry
    start_date = models.DateTimeField(default=timezone.now)
    duration_days = models.PositiveIntegerField(default=365, null=True, blank=True)  # default 30 days







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





