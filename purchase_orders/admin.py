from django.contrib import admin
from .models import PurchaseOrder, POItem, POPayment


class POItemInline(admin.TabularInline):
    model = POItem
    extra = 1
    readonly_fields = ['amount']


class POPaymentInline(admin.TabularInline):
    model = POPayment
    extra = 0
    readonly_fields = ['date', 'created_at']


@admin.register(PurchaseOrder)
class PurchaseOrderAdmin(admin.ModelAdmin):
    list_display = ['po_number', 'supplier', 'type', 'total_amount', 'status', 'created_at']
    list_filter = ['type', 'status', 'created_at']
    search_fields = ['po_number', 'supplier__name']
    readonly_fields = ['po_number', 'created_at', 'updated_at']
    inlines = [POItemInline, POPaymentInline]
    
    fieldsets = (
        ('PO Information', {
            'fields': ('po_number', 'supplier', 'type', 'linked_order', 'status')
        }),
        ('Pricing & Delivery', {
            'fields': ('total_amount', 'delivery_date')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )


@admin.register(POPayment)
class POPaymentAdmin(admin.ModelAdmin):
    list_display = ['purchase_order', 'amount', 'method', 'date']
    list_filter = ['date']
    search_fields = ['purchase_order__po_number', 'reference']
