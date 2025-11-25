from django.db import models
from django.db.models import Sum


class PurchaseOrder(models.Model):
    """
    Purchase Order system for fabric, trims, and manufacturing
    """
    
    PO_TYPE_CHOICES = [
        ('FABRIC', 'Fabric'),
        ('TRIM', 'Trim'),
        ('MANUFACTURING', 'Manufacturing'),
    ]
    
    PO_STATUS_CHOICES = [
        ('DRAFT', 'Draft'),
        ('SENT', 'Sent'),
        ('PARTIAL_RECEIVED', 'Partially Received'),
        ('COMPLETED', 'Completed'),
        ('CANCELLED', 'Cancelled'),
    ]
    
    # PO Information
    po_number = models.CharField(max_length=100, unique=True, blank=True)
    supplier = models.ForeignKey('suppliers.Supplier', on_delete=models.CASCADE, related_name='purchase_orders')
    type = models.CharField(max_length=15, choices=PO_TYPE_CHOICES)
    linked_order = models.ForeignKey(
        'orders.Order',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='purchase_orders'
    )
    
    # Pricing
    total_amount = models.DecimalField(max_digits=12, decimal_places=2)
    delivery_date = models.DateField(null=True, blank=True)
    status = models.CharField(max_length=20, choices=PO_STATUS_CHOICES, default='DRAFT')
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Purchase Order'
        verbose_name_plural = 'Purchase Orders'
    
    def save(self, *args, **kwargs):
        """Auto-generate PO number and update supplier ledger"""
        is_new = self.pk is None
        
        if not self.po_number:
            import time
            self.po_number = f'PO-{int(time.time())}'
        
        super().save(*args, **kwargs)
        
        # Update supplier ledger when creating PO
        if is_new:
            supplier = self.supplier
            supplier.total_billed += self.total_amount
            supplier.balance += self.total_amount
            supplier.save()
    
    def __str__(self):
        return f'{self.po_number} - {self.supplier.name} (${self.total_amount})'


class POItem(models.Model):
    """
    Line items in a Purchase Order
    """
    purchase_order = models.ForeignKey(PurchaseOrder, on_delete=models.CASCADE, related_name='items')
    
    description = models.CharField(max_length=255)
    quantity = models.DecimalField(max_digits=10, decimal_places=2)
    unit = models.CharField(max_length=20, blank=True, help_text='e.g., meters, pieces, kg')
    rate = models.DecimalField(max_digits=10, decimal_places=2)
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    
    def save(self, *args, **kwargs):
        """Auto-calculate amount"""
        self.amount = self.quantity * self.rate
        super().save(*args, **kwargs)
    
    def __str__(self):
        return f'{self.description} x {self.quantity}'


class POPayment(models.Model):
    """
    Payment records against a PO
    """
    purchase_order = models.ForeignKey(PurchaseOrder, on_delete=models.CASCADE, related_name='payments')
    
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    date = models.DateTimeField(auto_now_add=True)
    method = models.CharField(max_length=100, blank=True, help_text='e.g., Bank Transfer, Cash')
    reference = models.CharField(max_length=255, blank=True, help_text='Transaction reference')
    proof_url = models.FileField(upload_to='po_payments/', blank=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-date']
        verbose_name = 'PO Payment'
        verbose_name_plural = 'PO Payments'
    
    def save(self, *args, **kwargs):
        """Update supplier ledger and PO status on payment"""
        is_new = self.pk is None
        
        super().save(*args, **kwargs)
        
        if is_new:
            # Update supplier ledger
            supplier = self.purchase_order.supplier
            supplier.total_paid += self.amount
            supplier.balance -= self.amount
            supplier.save()
            
            # Update PO status based on total payments
            po = self.purchase_order
            total_paid = po.payments.aggregate(Sum('amount'))['amount__sum'] or 0
            
            if total_paid >= po.total_amount:
                po.status = 'COMPLETED'
            else:
                po.status = 'PARTIAL_RECEIVED'
            po.save()
    
    def __str__(self):
        return f'Payment ${self.amount} for {self.purchase_order.po_number}'
