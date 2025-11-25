from django.contrib import admin
from .models import Production, QCReport, Shipment


class QCReportInline(admin.TabularInline):
    model = QCReport
    extra = 0


class ShipmentInline(admin.StackedInline):
    model = Shipment
    max_num = 1


@admin.register(Production)
class ProductionAdmin(admin.ModelAdmin):
    list_display = ['order', 'created_at']
    search_fields = ['order__pi_number']
    inlines = [QCReportInline, ShipmentInline]


@admin.register(QCReport)
class QCReportAdmin(admin.ModelAdmin):
    list_display = ['production', 'type', 'status', 'date', 'aql']
    list_filter = ['type', 'status', 'date']


@admin.register(Shipment)
class ShipmentAdmin(admin.ModelAdmin):
    list_display = ['production', 'courier', 'tracking_number', 'status', 'eta']
    list_filter = ['status']
    search_fields = ['tracking_number', 'courier']
