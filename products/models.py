from django.db import models


class Product(models.Model):
    """
    Product catalog for the public website
    """
    
    # Basic Information
    name = models.CharField(max_length=255)
    description = models.TextField()
    category = models.CharField(max_length=100)
    sub_category = models.CharField(max_length=100)
    
    # Images, Pricing, Colors, Sizes - Stored as JSON arrays
    images = models.JSONField(default=list, help_text='Array of image URLs')
    price_tiers = models.JSONField(
        default=list,
        help_text='Array of {minQty, maxQty, price} objects'
    )
    colors = models.JSONField(
        default=list,
        help_text='Array of {name, hex, image} objects'
    )
    sizes = models.JSONField(default=list, help_text='Array of size strings')
    
    # MOQ & Lead Time
    moq = models.IntegerField(default=1, help_text='Minimum Order Quantity')
    lead_time = models.CharField(max_length=100, blank=True, help_text='e.g., "7-15 days"')
    
    # Product Features & Material
    material = models.CharField(max_length=255, blank=True, help_text='Product material')
    warranty = models.CharField(max_length=255, blank=True, help_text='Warranty information')
    certifications = models.CharField(max_length=255, blank=True, help_text='Certifications')
    
    # Shipping & Payment Terms
    shipping_terms = models.CharField(max_length=255, blank=True, help_text='Shipping terms')
    payment_terms = models.CharField(max_length=255, blank=True, help_text='Payment terms')
    bulk_pricing = models.TextField(blank=True, help_text='Bulk pricing information')
    
    # Customization & Specifications
    customization = models.JSONField(
        default=list,
        blank=True,
        help_text='Array of customization options (e.g., ["Logo", "Packaging"])'
    )
    specifications = models.JSONField(
        default=dict,
        blank=True,
        help_text='Object with material, fabricType, technics, feature, origin'
    )
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Product'
        verbose_name_plural = 'Products'
    
    def __str__(self):
        return f'{self.name} ({self.category})'
