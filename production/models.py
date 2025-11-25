from django.db import models


class Production(models.Model):
    """
    Production tracking for an order
    """
    order = models.OneToOneField('orders.Order', on_delete=models.CASCADE, related_name='production')
    
    # Approvals & Stages stored as JSON for flexibility
    # Structure: {fabric: {status: "APPROVED", date: "...", notes: "..."}, color: {...}, ...}
    approvals = models.JSONField(default=dict, blank=True, help_text='Pre-production approvals')
    
    # Stages: {cutting: {status: "COMPLETED", progress: 100, startDate: "...", endDate: "..."}, ...}
    stages = models.JSONField(default=dict, blank=True, help_text='Production stages progress')
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = 'Production'
        verbose_name_plural = 'Productions'
    
    def __str__(self):
        return f'Production for {self.order.pi_number}'


class QCReport(models.Model):
    """
    Quality Control reports
    """
    
    QC_TYPE_CHOICES = [
        ('INLINE', 'Inline QC'),
        ('TOP', 'TOP QC'),
        ('FINAL', 'Final QC'),
    ]
    
    STATUS_CHOICES = [
        ('PASS', 'Pass'),
        ('FAIL', 'Fail'),
        ('PENDING', 'Pending'),
    ]
    
    production = models.ForeignKey(Production, on_delete=models.CASCADE, related_name='qc_reports')
    
    type = models.CharField(max_length=10, choices=QC_TYPE_CHOICES)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='PENDING')
    date = models.DateTimeField(auto_now_add=True)
    aql = models.DecimalField(max_digits=4, decimal_places=2, default=2.5, help_text='Acceptable Quality Level')
    
    # Defects stored as JSON: [{description: "...", count: 5}, ...]
    defects = models.JSONField(default=list, blank=True)
    
    # Documents
    report_url = models.FileField(upload_to='qc_reports/', blank=True)
    images = models.JSONField(default=list, blank=True, help_text='Array of image URLs')
    
    class Meta:
        ordering = ['-date']
        verbose_name = 'QC Report'
        verbose_name_plural = 'QC Reports'
    
    def __str__(self):
        return f'{self.get_type_display()} - {self.production.order.pi_number} ({self.get_status_display()})'


class Shipment(models.Model):
    """
    Shipment details for an order
    """
    
    STATUS_CHOICES = [
        ('PENDING', 'Pending'),
        ('SHIPPED', 'Shipped'),
        ('DELIVERED', 'Delivered'),
    ]
    
    production = models.OneToOneField(Production, on_delete=models.CASCADE, related_name='shipment')
    
    courier = models.CharField(max_length=255, blank=True)
    tracking_number = models.CharField(max_length=255, blank=True)
    etd = models.DateField(null=True, blank=True, help_text='Estimated Time of Departure')
    eta = models.DateField(null=True, blank=True, help_text='Estimated Time of Arrival')
    
    # Documents
    invoice_url = models.FileField(upload_to='shipment/invoices/', blank=True)
    packing_list_url = models.FileField(upload_to='shipment/packing/', blank=True)
    awb_url = models.FileField(upload_to='shipment/awb/', blank=True)
    
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='PENDING')
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = 'Shipment'
        verbose_name_plural = 'Shipments'
    
    def __str__(self):
        return f'Shipment for {self.production.order.pi_number} ({self.get_status_display()})'
