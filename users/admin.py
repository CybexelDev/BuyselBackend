from django.contrib import admin
from . models import *
# Register your models here.

from django.contrib import admin
from .models import Wishlist


@admin.register(Wishlist)
class WishlistAdmin(admin.ModelAdmin):
    list_display = ("id", "user", "property_uuid", "created_at")
    search_fields = ("user__email", "property_uuid")
    readonly_fields = ("id", "created_at")
    
admin.site.register(Testimonial)