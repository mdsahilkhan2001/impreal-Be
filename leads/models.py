from django.db import models
from django.conf import settings


class Lead(models.Model):
    """
    Lead model for tracking customer inquiries from website
    """
    
    STATUS_CHOICES = [
        ('NEW', 'New'),
        ('QUALIFIED', 'Qualified'),
        ('SCOPE_LOCKED', 'Scope Locked'),
        ('PI_SENT', 'PI Sent'),
        ('ORDER_CONFIRMED', 'Order Confirmed'),
        ('LOST', 'Lost'),
    ]
    
    # Basic Information
    name = models.CharField(max_length=255)
    email = models.EmailField()
    phone = models.CharField(max_length=20, blank=True)
    country = models.CharField(max_length=100)
    
    # Product Information
    product_type = models.CharField(max_length=100)
    quantity = models.IntegerField(null=True, blank=True)
    budget = models.CharField(max_length=100, blank=True)
    message = models.TextField(blank=True)
    
    # Reference files (stored as JSON array of URLs)
    reference_images = models.JSONField(default=list, blank=True)
    
    # Status & Assignment
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='NEW')
    assigned_to = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='assigned_leads'
    )
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='my_leads',
        help_text='The buyer who created this lead (if logged in)'
    )
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Lead'
        verbose_name_plural = 'Leads'
    
    def __str__(self):
        return f'{self.name} - {self.product_type} ({self.get_status_display()})'


class LeadHistory(models.Model):
    """
    Track all changes/actions on a lead
    """
    lead = models.ForeignKey(Lead, on_delete=models.CASCADE, related_name='history')
    action = models.CharField(max_length=255)
    timestamp = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True
    )
    
    class Meta:
        ordering = ['-timestamp']
        verbose_name = 'Lead History'
        verbose_name_plural = 'Lead Histories'
    
    def __str__(self):
        return f'{self.lead.name} - {self.action} at {self.timestamp}'
