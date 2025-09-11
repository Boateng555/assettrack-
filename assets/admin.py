from django.contrib import admin
from .models import Employee, Asset, Handover, HandoverAsset, WelcomePack

@admin.register(Employee)
class EmployeeAdmin(admin.ModelAdmin):
    list_display = ['name', 'email', 'department', 'is_active', 'created_at']
    list_filter = ['department', 'is_active', 'created_at']
    search_fields = ['name', 'email']
    ordering = ['name']

@admin.register(Asset)
class AssetAdmin(admin.ModelAdmin):
    list_display = ['name', 'asset_type', 'serial_number', 'status', 'assigned_to', 'can_delete', 'deletion_restricted', 'created_at']
    list_filter = ['asset_type', 'status', 'can_delete', 'deletion_restricted', 'created_at']
    search_fields = ['name', 'serial_number', 'model']
    ordering = ['name']
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('name', 'asset_type', 'serial_number', 'model', 'manufacturer', 'status', 'assigned_to')
        }),
        ('Dates', {
            'fields': ('purchase_date', 'warranty_expiry', 'subscription_end')
        }),
        ('Software Details', {
            'fields': ('license_key', 'license_type', 'version', 'vendor', 'seats', 'used_seats'),
            'classes': ('collapse',)
        }),
        ('Maintenance Information', {
            'fields': ('maintenance_start_date', 'maintenance_expected_end', 'maintenance_notes'),
            'classes': ('collapse',)
        }),
        ('Azure AD Integration', {
            'fields': ('azure_ad_id', 'operating_system', 'os_version', 'last_azure_sync'),
            'classes': ('collapse',)
        }),
        ('Permissions', {
            'fields': ('can_delete', 'deletion_restricted'),
            'description': 'Control who can delete this asset'
        }),
        ('Notes', {
            'fields': ('notes',),
            'classes': ('collapse',)
        })
    )

@admin.register(Handover)
class HandoverAdmin(admin.ModelAdmin):
    list_display = ['handover_id', 'employee', 'mode', 'status', 'created_at', 'completed_at']
    list_filter = ['mode', 'status', 'created_at']
    search_fields = ['handover_id', 'employee__name']
    ordering = ['-created_at']
    readonly_fields = ['handover_id', 'created_at', 'updated_at']

@admin.register(HandoverAsset)
class HandoverAssetAdmin(admin.ModelAdmin):
    list_display = ['handover', 'asset', 'condition_before', 'condition_after']
    list_filter = ['handover__status']
    search_fields = ['handover__handover_id', 'asset__name']

@admin.register(WelcomePack)
class WelcomePackAdmin(admin.ModelAdmin):
    list_display = ['employee', 'employee_email', 'it_contact_person', 'is_active', 'generated_at', 'generated_by']
    list_filter = ['is_active', 'generated_at', 'email_sent_to_employee', 'email_sent_to_it']
    search_fields = ['employee__name', 'employee_email', 'it_contact_person']
    ordering = ['-generated_at']
    readonly_fields = ['generated_at', 'email_sent_at']
