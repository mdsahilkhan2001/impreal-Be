from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    """
    Custom User model with role-based access control
    Roles: BUYER, SELLER, DESIGNER, ADMIN
    """
    
    ROLE_CHOICES = [
        ('BUYER', 'Buyer'),
        ('SELLER', 'Seller'),
        ('DESIGNER', 'Designer'),
        ('ADMIN', 'Admin'),
    ]
    
    # Override email to make it unique and required
    email = models.EmailField(unique=True)
    
    # Additional fields
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='BUYER')
    phone = models.CharField(max_length=20, blank=True)
    company = models.CharField(max_length=255, blank=True)
    avatar = models.ImageField(upload_to='avatars/', blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    # Use email as the username field
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'first_name']
    
    class Meta:
        ordering = ['-created_at']
        verbose_name = 'User'
        verbose_name_plural = 'Users'
    
    def __str__(self):
        return f'{self.get_full_name() or self.email} ({self.get_role_display()})'
    
    @property
    def is_buyer(self):
        return self.role == 'BUYER'
    
    @property
    def is_seller(self):
        return self.role == 'SELLER'
    
    @property
    def is_designer(self):
        return self.role == 'DESIGNER'
    
    @property
    def is_admin_role(self):
        return self.role == 'ADMIN'
