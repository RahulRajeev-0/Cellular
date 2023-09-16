from django.contrib import admin
from .models import Account
from django.contrib.auth.admin import UserAdmin

class AccountAdmin(UserAdmin):
    ordering=['-date_joined']
    list_display = ('user_name','email','phone_number','date_joined','is_superuser','is_staff','is_active','is_admin')
    list_display_links=('user_name','email')
    readonly_fields=('date_joined',)
    filter_horizontal=()
    list_filter=()
    fieldsets=()

# Register your models here.

admin.site.register(Account,AccountAdmin)

