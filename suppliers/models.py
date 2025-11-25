from django.db import models


class Supplier(models.Model):
    """
    Supplier master database
    """
    
    CATEGORY_CHOICES = [
        ('FABRIC', 'Fabric'),
        ('TRIMS', 'Trims'),
        ('MANUFACTURING', 'Manufacturing'),
        ('PACKING', 'Packing'),
        ('LOGISTICS', 'Logistics'),
    ]
    
    # Basic Information
    name = models.CharField(max_length=255)
    contact_person = models.CharField(max_length=255, blank=True)
    email = models.EmailField(blank=True)
    phone = models.CharField(max_length=20, blank=True)
    address = models.TextField(blank=True)
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES, blank=True)
    
    # Bank Details
    account_name = models.CharField(max_length=255, blank=True)
    account_number = models.CharField(max_length=100, blank=True)
    bank_name = models.CharField(max_length=255, blank=True)
    ifsc_code = models.CharField(max_length=20, blank=True)
    
    # Ledger - Auto-updated via PO transactions
    total_billed = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    total_paid = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    balance = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['name']
        verbose_name = 'Supplier'
        verbose_name_plural = 'Suppliers'
    
    def __str__(self):
        return f'{self.name} ({self.get_category_display()})'
