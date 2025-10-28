from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User, PCMember, PCTransaction

@admin.register(User)
class UserAdmin(BaseUserAdmin):
    """Admin for custom User model"""
    
    list_display = ['username', 'email', 'first_name', 'last_name', 'role', 'is_active', 'is_staff']
    list_filter = ['role', 'is_active', 'is_staff', 'is_superuser']
    search_fields = ['username', 'first_name', 'last_name', 'email', 'phone']
    
    fieldsets = BaseUserAdmin.fieldsets + (
        ('Additional Info', {
            'fields': ('role', 'phone', 'address', 'specialization', 'license_number', 'profile_picture')
        }),
    )
    
    add_fieldsets = BaseUserAdmin.add_fieldsets + (
        ('Additional Info', {
            'fields': ('role', 'phone', 'address', 'specialization', 'license_number')
        }),
    )


@admin.register(PCMember)
class PCMemberAdmin(admin.ModelAdmin):
    """Admin for PC Members"""
    
    list_display = ['pc_code', 'name', 'member_type', 'commission_percentage', 'total_commission_earned', 'total_referrals', 'is_active']
    list_filter = ['member_type', 'is_active', 'created_at']
    search_fields = ['pc_code', 'name', 'phone', 'email']
    readonly_fields = ['pc_code', 'total_commission_earned', 'total_referrals', 'created_at', 'updated_at']
    
    fieldsets = (
        ('Member Information', {
            'fields': ('pc_code', 'member_type', 'name', 'phone', 'email', 'address')
        }),
        ('Commission Settings', {
            'fields': ('commission_percentage',)
        }),
        ('Statistics', {
            'fields': ('total_commission_earned', 'total_referrals')
        }),
        ('Status', {
            'fields': ('is_active', 'notes')
        }),
        ('Metadata', {
            'fields': ('created_by', 'created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    def save_model(self, request, obj, form, change):
        if not change:  # If creating new
            obj.created_by = request.user
        super().save_model(request, obj, form, change)


@admin.register(PCTransaction)
class PCTransactionAdmin(admin.ModelAdmin):
    """Admin for PC Transactions"""
    
    list_display = ['transaction_number', 'pc_member', 'transaction_date', 'total_amount', 'commission_amount', 'admin_amount', 'is_paid_to_member']
    list_filter = ['transaction_date', 'is_paid_to_member', 'pc_member__member_type']
    search_fields = ['transaction_number', 'pc_member__pc_code', 'pc_member__name']
    readonly_fields = ['transaction_number', 'commission_amount', 'admin_amount', 'transaction_date']
    date_hierarchy = 'transaction_date'
    
    fieldsets = (
        ('Transaction Information', {
            'fields': ('transaction_number', 'pc_member', 'transaction_date')
        }),
        ('Patient/Appointment', {
            'fields': ('patient', 'appointment')
        }),
        ('Amounts', {
            'fields': ('total_amount', 'commission_percentage', 'commission_amount', 'admin_amount')
        }),
        ('Payment Status', {
            'fields': ('is_paid_to_member', 'paid_at')
        }),
        ('Metadata', {
            'fields': ('recorded_by', 'notes'),
            'classes': ('collapse',)
        }),
    )
    
    def save_model(self, request, obj, form, change):
        if not change:  # If creating new
            obj.recorded_by = request.user
        super().save_model(request, obj, form, change)

