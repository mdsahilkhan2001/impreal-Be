from django.db import models
from django.conf import settings


class Costing(models.Model):
    """
    Costing sheet for calculating EXW price per garment
    """
    
    # Style Information
    style_name = models.CharField(max_length=255)
    style_number = models.CharField(max_length=100, blank=True)
    
    # Cost Components
    fabric_cost = models.DecimalField(max_digits=10, decimal_places=2, help_text='Cost per unit (e.g., per meter)')
    fabric_consumption = models.DecimalField(max_digits=8, decimal_places=2, help_text='Units consumed per garment')
    trim_cost = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    cm_cost = models.DecimalField(max_digits=10, decimal_places=2, help_text='Cut & Make cost')
    packing_cost = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    overhead_cost = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    
    # Pricing
    profit_margin = models.DecimalField(max_digits=5, decimal_places=2, default=20, help_text='Profit margin percentage')
    currency = models.CharField(max_length=3, default='USD')
    exw_price = models.DecimalField(max_digits=10, decimal_places=2, editable=False, null=True)
    total_price = models.DecimalField(max_digits=10, decimal_places=2, editable=False, null=True)
    
    # Additional Info
    notes = models.TextField(blank=True)
    
    # Relations
    lead = models.ForeignKey('leads.Lead', on_delete=models.SET_NULL, null=True, blank=True, related_name='costings')
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True)
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Costing'
        verbose_name_plural = 'Costings'
    
    def save(self, *args, **kwargs):
        """Auto-calculate prices before saving"""
        base_cost = (
            (self.fabric_cost * self.fabric_consumption) +
            self.trim_cost +
            self.cm_cost +
            self.packing_cost +
            self.overhead_cost
        )
        profit_amount = base_cost * (self.profit_margin / 100)
        self.exw_price = base_cost + profit_amount
        self.total_price = self.exw_price
        super().save(*args, **kwargs)
    
    def __str__(self):
        return f'{self.style_name} - ${self.exw_price:.2f} EXW'
