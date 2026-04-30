# admin.py
from django.contrib import admin
from .models import *
from django.utils.html import format_html
from agents.models import *


# Define the action
def disable_selected(modeladmin, request, queryset):
    # Toggle the disabled status for all selected objects
    for obj in queryset:
        obj.disabled = not obj.disabled
        obj.save()

# Add the action to the admin panel
disable_selected.short_description = "Disable/Enable selected items"



class MainCategoryAdmin(admin.ModelAdmin):
    list_display = ('catgory',)  # 


class ScreenshotAdminMixin(admin.ModelAdmin):
    def save_model(self, request, obj, form, change):
        super().save_model(request, obj, form, change)
        
        # Add JS trigger to take screenshot
        js = f"""
        <script>
            setTimeout(function() {{
                captureScreenshotAndUpload('{obj.id}', '{obj.id}', '{obj.__class__.__name__.lower()}');
            }}, 1000);
        </script>
        """
        self.message_user(request, format_html(js))



admin.site.site_header = "Buysel"
admin.site.site_title = "Buysel admin"
admin.site.index_title = "Welcome to Buysel Administration"

from developer.models import CustomUser
from django.contrib.auth.admin import UserAdmin


class CustomUserAdmin(UserAdmin):
    model = CustomUser
    fieldsets = UserAdmin.fieldsets + (
        ('Custom Fields', {'fields': ('rate_limit', 'last_failed_login')}),
    )
    add_fieldsets = UserAdmin.add_fieldsets + (
        ('Custom Fields', {'fields': ('rate_limit', 'last_failed_login')}),
    )

admin.site.register(CustomUser, CustomUserAdmin)


admin.site.register(Property)
admin.site.register(PropertyImage)
admin.site.register(ExpiredProperty)
admin.site.register(Premium)
admin.site.register(Agents)
admin.site.register(Blog)
admin.site.register(Contact)

admin.site.register(AgentForm)
admin.site.register(Propertylist)
admin.site.register(Request)
admin.site.register(ExpiredPremium)
admin.site.register(ExpireAgents)
admin.site.register(Budget)
admin.site.register(Amenities)
admin.site.register(Category)
admin.site.register(Subcategory)
class FieldOptionInline(admin.TabularInline):
    model = FieldOption
    extra = 1   # how many empty rows show


# 👉 Main admin
@admin.register(SubcategoryField)
class SubcategoryFieldAdmin(admin.ModelAdmin):
    list_display = ("field_name", "subcategory", "field_type", "required")
    list_filter = ("field_type", "subcategory")
    search_fields = ("field_name",)

    inlines = [FieldOptionInline]   # 🔥 IMPORTANT


# 👉 (Optional) also register separately
@admin.register(FieldOption)
class FieldOptionAdmin(admin.ModelAdmin):
    list_display = ("name", "field")
admin.site.register(Purpose)
# admin.site.register(UserAdd)
admin.site.register(Userplan)
admin.site.register(Userupgrade)
admin.site.register(Promotion)
admin.site.register(PromotionExtra)
admin.site.register(ElitePlan)
admin.site.register(AgentPlan)
admin.site.register(PremiumPlan)
admin.site.register(PropertyEnquiry)
admin.site.register(PropertyView)
admin.site.register(UserCreate)
admin.site.register(SliderBannerAd)
admin.site.register(HeroImage)
admin.site.register(AgentUserProfile)



@admin.register(AdvertisementPackage)
class AdvertisementPackageAdmin(admin.ModelAdmin):
    list_display = ("name", "package_type", "price_per_day", "ads_per_day", "display_seconds")
    list_filter = ("package_type",)
    search_fields = ("name",)


@admin.register(ReelPackage)
class ReelPackageAdmin(admin.ModelAdmin):
    list_display = ("name", "reel_type", "price_per_day", "duration")
    list_filter = ("reel_type",)
    search_fields = ("name",)