from django.contrib import admin
from .models import Costing


@admin.register(Costing)
class CostingAdmin(admin.ModelAdmin):
    list_display = ['style_name', 'style_number', 'exw_price', 'currency', 'created_by', 'created_at']
    list_filter = ['currency', 'created_at']
    search_fields = ['style_name', 'style_number']
    readonly_fields = ['exw_price', 'total_price', 'created_at', 'updated_at']
    
    fieldsets = (
        ('Style Information', {
            'fields': ('style_name', 'style_number', 'lead')
        }),
        ('Cost Components', {
            'fields': ('fabric_cost', 'fabric_consumption', 'trim_cost', 'cm_cost', 'packing_cost', 'overhead_cost')
        }),
        ('Pricing', {
            'fields': ('profit_margin', 'currency', 'exw_price', 'total_price')
        }),
        ('Additional', {
            'fields': ('notes', 'created_by', 'created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
