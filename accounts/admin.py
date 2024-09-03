from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Account, UserProfile

class AccountAdmin(UserAdmin):
    # Fields to display in the admin list view
    list_display = ('email', 'first_name', 'last_name', 'username', 'last_login', 'date_joined', 'is_active', 'is_staff', 'is_admin')
    # Fields to enable search functionality
    search_fields = ('email', 'username', 'first_name', 'last_name')
    # Fields to make read-only
    readonly_fields = ('last_login', 'date_joined')
    # Fields to determine the default ordering of objects in the admin view
    ordering = ('-date_joined',)

    # Specify fieldsets to customize the admin interface layout
    filter_horizontal = ()
    list_filter = ()
    fieldsets = ()

class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'city', 'state', 'country')

# Register your models with the custom admin configurations
admin.site.register(Account, AccountAdmin)
admin.site.register(UserProfile, UserProfileAdmin)
