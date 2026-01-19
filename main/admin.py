from django.contrib import admin
from django_tenants.admin import TenantAdminMixin

from main.models import Client, Domain, Role, UserProfile, AccountRequest

@admin.register(Client)
class ClientAdmin(TenantAdminMixin, admin.ModelAdmin):
        list_display = ('name', 'created_on')
        
@admin.register(Domain)
class DomainAdmin(TenantAdminMixin, admin.ModelAdmin):
        list_display = ('id', 'domain', 'tenant', 'is_primary')

@admin.register(Role)
class RoleAdmin(admin.ModelAdmin):
    list_display = ('name',)

@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'role')

@admin.register(AccountRequest)
class AccountRequestAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'requested_role', 'status', 'requested_by', 'approved_by', 'created_at')
    list_filter = ('status', 'requested_role')
    search_fields = ('username', 'email')