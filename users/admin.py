from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from users.models import CustomUser

@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    list_display = ("id", "email", "birthday")
    fieldsets = (
        (None, {'fields': ('email', 'password', 'is_staff', 'is_active')}),
        ('Personal info', {'fields': ('username', )}),
        ('Date information', {'fields': ('last_login',)}),
    
    )