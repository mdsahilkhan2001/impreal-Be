from django.contrib import admin
from .models import Supplier


@admin.register(Supplier)
class SupplierAdmin(admin.ModelAdmin):
    list_display = ['name', 'category', 'total_billed', 'total_paid', 'balance', 'created_at']
    list_filter = ['category', 'created_at']
    search_fields = ['name', 'contact_person', 'email']
    readonly_fields = ['total_billed', 'total_paid', 'balance', 'created_at', 'updated_at']
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('name', 'contact_person', 'email', 'phone', 'address', 'category')
        }),
        ('Bank Details', {
            'fields': ('account_name', 'account_number', 'bank_name', 'ifsc_code'),
            'classes': ('collapse',)
        }),
        ('Ledger (Auto-Updated)', {
            'fields': ('total_billed', 'total_paid', 'balance'),
            'classes': ('collapse',)
        }),
    )
