from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import BoltUser

class BoltUserAdmin(UserAdmin):
    list_display = ('username', 'email', 'first_name', 'last_name', 'distance')
    list_filter = ('is_active', 'is_staff', 'is_superuser')
    search_fields = ('email', 'first_name', 'last_name')
    ordering = ('email',)

admin.site.register(BoltUser, BoltUserAdmin)
