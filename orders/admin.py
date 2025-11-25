from django.contrib import admin
from .models import Order, OrderProduct


class OrderProductInline(admin.TabularInline):
    model = OrderProduct
    extra = 1
    readonly_fields = ['total_price']


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['pi_number', 'buyer_name', 'total_amount', 'status', 'pi_date']
    list_filter = ['status', 'commercial_term', 'pi_date']
    search_fields = ['pi_number', 'buyer_name', 'buyer_email']
    readonly_fields = ['pi_number', 'pi_date', 'created_at', 'updated_at']
    inlines = [OrderProductInline]
    
    fieldsets = (
        ('order Information', {
            'fields': ('lead', 'pi_number', 'status')
        }),
        ('Buyer Details', {
            'fields': ('buyer_name', 'buyer_company', 'buyer_address', 'buyer_email', 'buyer_phone')
        }),
        ('Commercial Terms', {
            'fields': ('commercial_term', 'payment_terms', 'bank_details', 'total_amount', 'currency')
        }),
        ('Timeline', {
            'fields': ('pi_date', 'advance_date', 'production_start_date', 'shipment_date')
        }),
        ('Documents', {
            'fields': ('pi_url', 'invoice_url', 'packing_list_url', 'awb_url'),
            'classes': ('collapse',)
        }),
    )
