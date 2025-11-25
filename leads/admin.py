from django.contrib import admin
from .models import Lead, LeadHistory


class LeadHistoryInline(admin.TabularInline):
    model = LeadHistory
    extra = 0
    readonly_fields = ['action', 'timestamp', 'user']


@admin.register(Lead)
class LeadAdmin(admin.ModelAdmin):
    list_display = ['name', 'email', 'country', 'product_type', 'status', 'created_at']
    list_filter = ['status', 'country', 'product_type', 'created_at']
    search_fields = ['name', 'email', 'phone', 'company', 'message']
    readonly_fields = ['created_at', 'updated_at']
    inlines = [LeadHistoryInline]
    
    fieldsets = (
        ('Contact Information', {
            'fields': ('name', 'email', 'phone', 'country')
        }),
        ('Product Details', {
            'fields': ('product_type', 'quantity', 'budget', 'message', 'reference_images')
        }),
        ('Status & Assignment', {
            'fields': ('status', 'assigned_to', 'user')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )


@admin.register(LeadHistory)
class LeadHistoryAdmin(admin.ModelAdmin):
    list_display = ['lead', 'action', 'user', 'timestamp']
    list_filter = ['timestamp']
    search_fields = ['lead__name', 'action']
