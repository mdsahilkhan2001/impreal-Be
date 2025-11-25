from django.contrib import admin
from .models import Product


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['name', 'category', 'sub_category', 'moq', 'lead_time', 'created_at']
    list_filter = ['category', 'sub_category', 'created_at']
    search_fields = ['name', 'description']
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('name', 'description', 'category', 'sub_category')
        }),
        ('Media & Pricing', {
            'fields': ('images', 'price_tiers', 'colors', 'sizes')
        }),
        ('Requirements', {
            'fields': ('moq', 'lead_time', 'customization')
        }),
        ('Specifications', {
            'fields': ('specifications',),
            'classes': ('collapse',)
        }),
    )
