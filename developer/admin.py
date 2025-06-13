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

# class HouseAdmin(admin.ModelAdmin):
#     list_display = ['Caption', 'status', 'username', 'disabled']  # You can customize which fields to show in the list view
#     actions = [disable_selected]  # Add the action to the list of available actions

# class LandAdmin(admin.ModelAdmin):
#     list_display = ['Caption', 'status', 'username', 'disabled']
#     actions = [disable_selected]

# class CommercialAdmin(admin.ModelAdmin):
#     list_display = ['Caption', 'status', 'username', 'disabled']
#     actions = [disable_selected]

# class OffPlanAdmin(admin.ModelAdmin):
#     list_display = ['Caption', 'status', 'username', 'disabled']
#     actions = [disable_selected]



# class HouseAdmin(admin.ModelAdmin):
#     list_filter = ('category',)  # Filter by the related MainCategory (category field)
#     list_display = ('Caption', 'category', 'price', 'status')  # Show relevant columns

# # Custom Admin for Land model
# class LandAdmin(admin.ModelAdmin):
#     list_filter = ('category',)  # Filter by the related MainCategory (category field)
#     list_display = ('Caption', 'category', 'price', 'status')

# # Custom Admin for Commercial model
# class CommercialAdmin(admin.ModelAdmin):
#     list_filter = ('category',)  # Filter by the related MainCategory (category field)
#     list_display = ('Caption', 'category', 'price', 'status')

# # Custom Admin for OffPlan model
# class OffPlanAdmin(admin.ModelAdmin):
#     list_filter = ('category',)  # Filter by the related MainCategory (category field)
#     list_display = ('Caption', 'category', 'price', 'status')



class MainCategoryAdmin(admin.ModelAdmin):
    list_display = ('catgory',)  # 


class HouseImageInline(admin.TabularInline):  # Or admin.StackedInline
    model = HouseImage
    extra = 1  # Show 10 empty forms by default
    min_num = 1  # Minimum number of images to be added

class HouseAdmin(admin.ModelAdmin):
    list_display = ['Caption', 'status', 'username', 'disabled']  # Customize fields to display in list view
    actions = ['disable_selected']  # Register your custom action
    inlines = [HouseImageInline]  # Add the inline class to the admin

    # Optionally, you can customize list filtering, search, etc.
    search_fields = ['Caption', 'username']
    list_filter = ['status', 'disabled']
    
    def disable_selected(self, request, queryset):
        """
        Custom admin action to disable selected houses.
        """
        queryset.update(disabled=True)
        self.message_user(request, "Selected houses have been disabled.")

    disable_selected.short_description = "Disable selected houses"


class LandImageInline(admin.TabularInline):  # Or admin.StackedInline
    model = LandImage
    extra = 1  # Show 10 empty forms by default
    min_num = 1  # Minimum number of images to be added

class LandAdmin(admin.ModelAdmin):
    list_display = ['Caption', 'status', 'username', 'disabled']  # Customize fields to display in list view
    actions = ['disable_selected']  # Register your custom action
    inlines = [LandImageInline]  # Add the inline class to the admin

    # Optionally, you can customize list filtering, search, etc.
    search_fields = ['Caption', 'username']
    list_filter = ['status', 'disabled']
    
    def disable_selected(self, request, queryset):
        """
        Custom admin action to disable selected houses.
        """
        queryset.update(disabled=True)
        self.message_user(request, "Selected houses have been disabled.")

    disable_selected.short_description = "Disable selected houses"

class CommercialImageInline(admin.TabularInline):  # Or admin.StackedInline
    model = CommercialImage
    extra = 1  # Show 10 empty forms by default
    min_num = 1  # Minimum number of images to be added

class CommercialAdmin(admin.ModelAdmin):
    list_display = ['Caption', 'status', 'username', 'disabled']  # Customize fields to display in list view
    actions = ['disable_selected']  # Register your custom action
    inlines = [CommercialImageInline]  # Add the inline class to the admin

    # Optionally, you can customize list filtering, search, etc.
    search_fields = ['Caption', 'username']
    list_filter = ['status', 'disabled']
    
    def disable_selected(self, request, queryset):
        """
        Custom admin action to disable selected houses.
        """
        queryset.update(disabled=True)
        self.message_user(request, "Selected houses have been disabled.")

    disable_selected.short_description = "Disable selected houses"

class OffplanImageInline(admin.TabularInline):  # Or admin.StackedInline
    model = OffplanImage
    extra = 1  # Show 10 empty forms by default
    min_num = 1  # Minimum number of images to be added

class OffplanAdmin(admin.ModelAdmin):
    list_display = ['Caption', 'status', 'username', 'disabled']  # Customize fields to display in list view
    actions = ['disable_selected']  # Register your custom action
    inlines = [OffplanImageInline]  # Add the inline class to the admin

    # Optionally, you can customize list filtering, search, etc.
    search_fields = ['Caption', 'username']
    list_filter = ['status', 'disabled']
    
    def disable_selected(self, request, queryset):
        """
        Custom admin action to disable selected houses.
        """
        queryset.update(disabled=True)
        self.message_user(request, "Selected houses have been disabled.")

    disable_selected.short_description = "Disable selected houses"

#

# class ItemImageInline(admin.TabularInline):
#     model = ItemImage
#     extra = 3  # Number of empty image slots shown by default in the admin

# class HouseAdmin(admin.ModelAdmin):
#     inlines = [ItemImageInline]

# class LandAdmin(admin.ModelAdmin):
#     inlines = [ItemImageInline]

# class CommercialAdmin(admin.ModelAdmin):
#     inlines = [ItemImageInline]

# class OffPlanAdmin(admin.ModelAdmin):
#     inlines = [ItemImageInline]

admin.site.register(House, HouseAdmin)
admin.site.register(Land, LandAdmin)
admin.site.register(Commercial, CommercialAdmin)
admin.site.register(OffPlan, OffplanAdmin)
admin.site.register(AgentForm)
admin.site.register(Propertylist)
admin.site.register(Blog)
admin.site.register(HouseImage)

admin.site.register(MainCategory)

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