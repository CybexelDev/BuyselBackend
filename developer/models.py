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
    image = CloudinaryField('image', folder="propertice")  # Main image
    perprice = models.CharField(max_length=10, blank=True, null=True)
    price = models.DecimalField(max_digits=12, decimal_places=2)
    owner = models.CharField(max_length=100)
    whatsapp = models.CharField(max_length=100)
    phone = models.CharField(max_length=100)

    # Store Google Maps link (embed/share)
    location = models.URLField(max_length=1000, help_text="Paste Google Maps share OR embed link")

    city = models.CharField(max_length=100)
    pincode = models.CharField(max_length=10)
    district = models.CharField(max_length=100)
    land_mark = models.CharField(max_length=100, blank=True, null=True)
    paid = models.CharField(max_length=100)
    added_by = models.CharField(max_length=100, blank=True, null=True)

    created_at = models.DateTimeField(auto_now_add=True)
    duration_days = models.PositiveIntegerField(default=30)

    def is_expired(self):
        expiry_date = self.created_at + timedelta(days=self.duration_days)
        return timezone.now() > expiry_date

    @property
    def map_embed(self):
        """Generate iframe embed from Google Maps link."""
        if "embed" in self.location:
            # Already an embed link
            return f'<iframe src="{self.location}" width="600" height="450" style="border:0;" allowfullscreen="" loading="lazy" referrerpolicy="no-referrer-when-downgrade"></iframe>'
        else:
            # Convert share/place link into embed
            return f'<iframe src="https://www.google.com/maps/embed/v1/place?key=YOUR_GOOGLE_API_KEY&q={self.location}" width="600" height="450" style="border:0;" allowfullscreen="" loading="lazy" referrerpolicy="no-referrer-when-downgrade"></iframe>'

    def save(self, *args, **kwargs):
        if self.pk and self.is_expired():
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
            # Move images
            for img in self.images.all():
                PropertyImage.objects.create(expired_property=expired_prop, image=img.image)
            super().delete()
        else:
            super().save(*args, **kwargs)

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
    price = models.DecimalField(max_digits=12, decimal_places=2)
    owner = models.CharField(max_length=100)
    whatsapp = models.CharField(max_length=100)
    phone = models.CharField(max_length=100)

    location = models.URLField(max_length=1000)

    city = models.CharField(max_length=100)
    pincode = models.CharField(max_length=10)
    district = models.CharField(max_length=100)
    land_mark = models.CharField(max_length=100, blank=True, null=True)
    paid = models.CharField(max_length=100)
    added_by = models.CharField(max_length=100, blank=True, null=True)

    created_at = models.DateTimeField()
    duration_days = models.PositiveIntegerField()

    def is_active_again(self):
        expiry_date = self.created_at + timedelta(days=self.duration_days)
        return timezone.now() <= expiry_date

    @property
    def map_embed(self):
        if "embed" in self.location:
            return f'<iframe src="{self.location}" width="600" height="450" style="border:0;" allowfullscreen="" loading="lazy" referrerpolicy="no-referrer-when-downgrade"></iframe>'
        else:
            return f'<iframe src="https://www.google.com/maps/embed/v1/place?key=YOUR_GOOGLE_API_KEY&q={self.location}" width="600" height="450" style="border:0;" allowfullscreen="" loading="lazy" referrerpolicy="no-referrer-when-downgrade"></iframe>'

    def save(self, *args, **kwargs):
        if self.pk and self.is_active_again():
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
            for img in self.images.all():
                PropertyImage.objects.create(property=active_prop, image=img.image)
            super().delete()
        else:
            super().save(*args, **kwargs)

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

    created_at = models.DateTimeField(auto_now_add=True)
    duration_days = models.PositiveIntegerField(default=365, null=True, blank=True)

    def is_expired(self):
        try:
            days = int(self.duration_days or 0)
        except (ValueError, TypeError):
            days = 0
        expiry_date = self.created_at + timedelta(days=days)
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

            # Move related images (no duplicates)
            for img in self.images.all():
                img.expired_premium = expired
                img.premium = None
                img.save()

            super(Premium, self).delete()
        else:
            super(Premium, self).save(*args, **kwargs)

    def __str__(self):
        return f"{self.name} ({'Expired' if self.is_expired() else 'Active'})"


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

    created_at = models.DateTimeField(auto_now_add=True)
    duration_days = models.PositiveIntegerField(default=365, null=True, blank=True)

    def is_active_again(self):
        try:
            days = int(self.duration_days or 0)
        except (ValueError, TypeError):
            days = 0
        expiry_date = self.created_at + timedelta(days=days)
        return timezone.now() <= expiry_date

    def save(self, *args, **kwargs):
        """If duration is updated and property is active again, move it back"""
        if self.pk and self.is_active_again():
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
                image=self.image,
                created_at=self.created_at,
                duration_days=self.duration_days,
            )

            # Move related images (no duplicates)
            for img in self.images.all():
                img.premium = active_premium
                img.expired_premium = None
                img.save()

            super(ExpiredPremium, self).delete()
        else:
            super(ExpiredPremium, self).save(*args, **kwargs)

    def __str__(self):
        return f"{self.name} (Expired)"


class PremiumImage(models.Model):
    premium = models.ForeignKey("Premium", on_delete=models.CASCADE, related_name="images", null=True, blank=True)
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
                created_at=self.created_at,
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

    created_at = models.DateTimeField(auto_now_add=True)
    duration_days = models.PositiveIntegerField(default=365, null=True, blank=True)

    def is_active_again(self):
        try:
            days = int(self.duration_days or 0)
        except (ValueError, TypeError):
            days = 0
        expiry_date = self.created_at + timedelta(days=days)
        return timezone.now() <= expiry_date

    def save(self, *args, **kwargs):
        """If duration is updated and agent is active again, move it back"""
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





