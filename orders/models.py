from django.db import models
from django.conf import settings


class Order(models.Model):
    """
    Order/Proforma Invoice model
    """
    
    TERM_CHOICES = [
        ('EXW', 'EX Works'),
        ('FOB', 'Free On Board'),
        ('CIF', 'Cost, Insurance & Freight'),
        ('CIP', 'Carriage & Insurance Paid'),
        ('DDP_AIR', 'DDP Air'),
        ('DDP_SEA', 'DDP Sea'),
    ]
    
    STATUS_CHOICES = [
        ('PI_GENERATED', 'PI Generated'),
        ('ADVANCE_RECEIVED', 'Advance Received'),
        ('PRODUCTION', 'In Production'),
        ('QC_PASSED', 'QC Passed'),
        ('SHIPPED', 'Shipped'),
        ('DELIVERED', 'Delivered'),
        ('CANCELLED', 'Cancelled'),
    ]
    
    # Relations
    lead = models.ForeignKey('leads.Lead', on_delete=models.CASCADE, related_name='orders')
    
    # PI Information
    pi_number = models.CharField(max_length=100, unique=True, blank=True)
    
    # Buyer Details
    buyer_name = models.CharField(max_length=255)
    buyer_company = models.CharField(max_length=255, blank=True)
    buyer_address = models.TextField(blank=True)
    buyer_email = models.EmailField()
    buyer_phone = models.CharField(max_length=20, blank=True)
    
    # Commercial Terms
    commercial_term = models.CharField(max_length=20, choices=TERM_CHOICES, default='EXW')
    payment_terms = models.CharField(max_length=255, default='50% Advance, 50% Before Shipment')
    bank_details = models.TextField(blank=True)
    
    # Pricing
    total_amount = models.DecimalField(max_digits=12, decimal_places=2)
    currency = models.CharField(max_length=3, default='USD')
    
    # Status
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='PI_GENERATED')
    
    # Timeline
    pi_date = models.DateTimeField(auto_now_add=True)
    advance_date = models.DateTimeField(null=True, blank=True)
    production_start_date = models.DateTimeField(null=True, blank=True)
    shipment_date = models.DateTimeField(null=True, blank=True)
    
    # Documents
    pi_url = models.FileField(upload_to='documents/pi/', blank=True)
    invoice_url = models.FileField(upload_to='documents/invoices/', blank=True)
    packing_list_url = models.FileField(upload_to='documents/packing/', blank=True)
    awb_url = models.FileField(upload_to='documents/awb/', blank=True)
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Order'
        verbose_name_plural = 'Orders'
    
    def save(self, *args, **kwargs):
        """Auto-generate PI number if not provided"""
        if not self.pi_number:
            import time
            self.pi_number = f'PI-{int(time.time())}'
        super().save(*args, **kwargs)
    
    def __str__(self):
        return f'{self.pi_number} - {self.buyer_name} (${self.total_amount})'


class OrderProduct(models.Model):
    """
    Line items in an order
    """
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='products')
    
    style_name = models.CharField(max_length=255)
    style_number = models.CharField(max_length=100)
    quantity = models.IntegerField()
    unit_price = models.DecimalField(max_digits=10, decimal_places=2)
    total_price = models.DecimalField(max_digits=12, decimal_places=2)
    size_breakdown = models.CharField(max_length=255, blank=True, help_text='e.g., S:10, M:20, L:15')
    
    def save(self, *args, **kwargs):
        """Auto-calculate total price"""
        self.total_price = self.quantity * self.unit_price
        super().save(*args, **kwargs)
    
    def __str__(self):
        return f'{self.style_name} x {self.quantity}'
