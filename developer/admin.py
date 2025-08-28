# admin.py
from django.contrib import admin
from .models import *
from django.utils.html import format_html


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

