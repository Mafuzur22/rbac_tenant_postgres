from django.db import models
from django_tenants.models import TenantMixin, DomainMixin
from django.contrib.auth.models import AbstractUser

class Client(TenantMixin):
    name = models.CharField(max_length=100)
    created_on = models.DateField(auto_now_add=True)

    # default true, schema will be automatically created and synced when it is saved
    auto_create_schema = True

class Domain(DomainMixin):
    pass

class Role(models.Model):
    SUPER_ADMIN = 'super_admin'
    MANAGER = 'manager'
    LAWYER = 'lawyer'
    NPL = 'npl'
    USER = 'user'
    
    ROLE_CHOICES = [
        (SUPER_ADMIN, 'Super Admin'),
        (MANAGER, 'Manager'),
        (LAWYER, 'Lawyer'),
        (NPL, 'NPL'),
        (USER, 'User'),
    ]
    
    name = models.CharField(max_length=20, choices=ROLE_CHOICES, unique=True)
    
    def __str__(self):
        return self.get_name_display()
    
class UserProfile(models.Model):
    user = models.OneToOneField('auth.User', on_delete=models.CASCADE)
    role = models.ForeignKey(Role, on_delete=models.CASCADE, default=Role.USER)
    
    def __str__(self):
        return f"{self.user.username} - {self.role}"

class AccountRequest(models.Model):
    PENDING = 'pending'
    APPROVED = 'approved'
    REJECTED = 'rejected'
    
    STATUS_CHOICES = [
        (PENDING, 'Pending'),
        (APPROVED, 'Approved'),
        (REJECTED, 'Rejected'),
    ]
    
    username = models.CharField(max_length=150)
    email = models.EmailField()
    password = models.CharField(max_length=128)
    requested_role = models.ForeignKey(Role, on_delete=models.CASCADE)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default=PENDING)
    requested_by = models.ForeignKey('auth.User', on_delete=models.CASCADE, null=True, blank=True)
    approved_by = models.ForeignKey('auth.User', on_delete=models.CASCADE, null=True, blank=True, related_name='approved_requests')
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.username} - {self.requested_role} ({self.status})"