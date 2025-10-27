from django.contrib import admin
from django.utils.html import format_html
from .models import (
    Department, IncomeCategory, Income, ExpenseCategory, 
    Expense, Investor, InvestorPayout, ConsultationFee
)


@admin.register(Department)
class DepartmentAdmin(admin.ModelAdmin):
    """Admin for Department model"""
    list_display = ['code', 'name', 'head', 'is_active', 'created_at']
    list_filter = ['is_active', 'created_at']
    search_fields = ['name', 'code', 'description']
    list_editable = ['is_active']
    ordering = ['name']
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('name', 'code', 'description')
        }),
        ('Management', {
            'fields': ('head', 'is_active')
        }),
    )


@admin.register(IncomeCategory)
class IncomeCategoryAdmin(admin.ModelAdmin):
    """Admin for Income Category"""
    list_display = ['name', 'description']
    search_fields = ['name', 'description']
    ordering = ['name']


@admin.register(Income)
class IncomeAdmin(admin.ModelAdmin):
    """Admin for Income model"""
    list_display = ['income_number', 'source', 'amount_display', 'date', 'category', 'recorded_by', 'recorded_at']
    list_filter = ['source', 'date', 'payment_method', 'category', 'department']
    search_fields = ['income_number', 'description', 'reference_number']
    readonly_fields = ['income_number', 'recorded_at', 'recorded_by']
    date_hierarchy = 'date'
    ordering = ['-date', '-recorded_at']
    
    fieldsets = (
        ('Income Details', {
            'fields': ('income_number', 'source', 'category', 'department', 'amount', 'date')
        }),
        ('Description', {
            'fields': ('description',)
        }),
        ('Payment Information', {
            'fields': ('reference_number', 'payment_method')
        }),
        ('Record Information', {
            'fields': ('recorded_by', 'recorded_at'),
            'classes': ('collapse',)
        }),
    )
    
    def amount_display(self, obj):
        return format_html('<strong style="color: green;">৳{:,.2f}</strong>', obj.amount)
    amount_display.short_description = 'Amount'
    
    def save_model(self, request, obj, form, change):
        if not change:  # If creating new object
            obj.recorded_by = request.user
        super().save_model(request, obj, form, change)


@admin.register(ExpenseCategory)
class ExpenseCategoryAdmin(admin.ModelAdmin):
    """Admin for Expense Category"""
    list_display = ['name', 'description']
    search_fields = ['name', 'description']
    ordering = ['name']


@admin.register(Expense)
class ExpenseAdmin(admin.ModelAdmin):
    """Admin for Expense model"""
    list_display = ['expense_number', 'expense_type', 'amount_display', 'date', 'vendor', 'approval_status', 'recorded_by']
    list_filter = ['expense_type', 'date', 'is_approved', 'category', 'department']
    search_fields = ['expense_number', 'description', 'vendor', 'invoice_number']
    readonly_fields = ['expense_number', 'recorded_at', 'recorded_by']
    date_hierarchy = 'date'
    ordering = ['-date', '-recorded_at']
    
    fieldsets = (
        ('Expense Details', {
            'fields': ('expense_number', 'expense_type', 'category', 'department', 'amount', 'date')
        }),
        ('Description', {
            'fields': ('description',)
        }),
        ('Vendor Information', {
            'fields': ('vendor', 'invoice_number', 'payment_method')
        }),
        ('Approval', {
            'fields': ('is_approved', 'approved_by')
        }),
        ('Attachment', {
            'fields': ('receipt',)
        }),
        ('Record Information', {
            'fields': ('recorded_by', 'recorded_at'),
            'classes': ('collapse',)
        }),
    )
    
    def amount_display(self, obj):
        return format_html('<strong style="color: red;">৳{:,.2f}</strong>', obj.amount)
    amount_display.short_description = 'Amount'
    
    def approval_status(self, obj):
        if obj.is_approved:
            return format_html('<span style="color: green; font-weight: bold;">✓ Approved</span>')
        return format_html('<span style="color: orange; font-weight: bold;">⏳ Pending</span>')
    approval_status.short_description = 'Status'
    
    def save_model(self, request, obj, form, change):
        if not change:  # If creating new object
            obj.recorded_by = request.user
        super().save_model(request, obj, form, change)
    
    actions = ['approve_expenses']
    
    def approve_expenses(self, request, queryset):
        updated = queryset.update(is_approved=True, approved_by=request.user)
        self.message_user(request, f'{updated} expense(s) approved successfully.')
    approve_expenses.short_description = 'Approve selected expenses'


@admin.register(Investor)
class InvestorAdmin(admin.ModelAdmin):
    """Admin for Investor model"""
    list_display = ['name', 'share_display', 'investment_amount_display', 'investment_date', 'is_active', 'phone']
    list_filter = ['is_active', 'investment_date']
    search_fields = ['name', 'email', 'phone', 'address']
    list_editable = ['is_active']
    ordering = ['-share_percentage']
    
    fieldsets = (
        ('Personal Information', {
            'fields': ('name', 'email', 'phone', 'address')
        }),
        ('Investment Details', {
            'fields': ('share_percentage', 'investment_amount', 'investment_date')
        }),
        ('Status', {
            'fields': ('is_active', 'notes')
        }),
    )
    
    def share_display(self, obj):
        return format_html('<strong>{:.2f}%</strong>', obj.share_percentage)
    share_display.short_description = 'Share %'
    
    def investment_amount_display(self, obj):
        return format_html('<strong style="color: blue;">৳{:,.2f}</strong>', obj.investment_amount)
    investment_amount_display.short_description = 'Investment'


@admin.register(InvestorPayout)
class InvestorPayoutAdmin(admin.ModelAdmin):
    """Admin for Investor Payout"""
    list_display = ['payout_number', 'investor', 'period', 'share_amount_display', 'payout_date', 'processed_by']
    list_filter = ['payout_date', 'investor']
    search_fields = ['payout_number', 'investor__name', 'notes']
    readonly_fields = ['payout_number', 'processed_at', 'processed_by']
    date_hierarchy = 'payout_date'
    ordering = ['-payout_date']
    
    fieldsets = (
        ('Payout Details', {
            'fields': ('payout_number', 'investor', 'period_start', 'period_end')
        }),
        ('Financial Details', {
            'fields': ('total_profit', 'share_amount', 'payout_date', 'payment_method')
        }),
        ('Notes', {
            'fields': ('notes',)
        }),
        ('Processing Information', {
            'fields': ('processed_by', 'processed_at'),
            'classes': ('collapse',)
        }),
    )
    
    def period(self, obj):
        return f"{obj.period_start.strftime('%d %b')} - {obj.period_end.strftime('%d %b %Y')}"
    period.short_description = 'Period'
    
    def share_amount_display(self, obj):
        return format_html('<strong style="color: purple;">৳{:,.2f}</strong>', obj.share_amount)
    share_amount_display.short_description = 'Share Amount'
    
    def save_model(self, request, obj, form, change):
        if not change:  # If creating new object
            obj.processed_by = request.user
        super().save_model(request, obj, form, change)


@admin.register(ConsultationFee)
class ConsultationFeeAdmin(admin.ModelAdmin):
    """Admin for Consultation Fee"""
    list_display = ['doctor', 'fee_amount_display', 'effective_from', 'effective_until', 'is_active']
    list_filter = ['is_active', 'effective_from', 'doctor']
    search_fields = ['doctor__first_name', 'doctor__last_name']
    list_editable = ['is_active']
    ordering = ['-effective_from']
    
    fieldsets = (
        ('Doctor', {
            'fields': ('doctor',)
        }),
        ('Fee Details', {
            'fields': ('fee_amount', 'effective_from', 'effective_until')
        }),
        ('Status', {
            'fields': ('is_active',)
        }),
    )
    
    def fee_amount_display(self, obj):
        return format_html('<strong style="color: green;">৳{:,.2f}</strong>', obj.fee_amount)
    fee_amount_display.short_description = 'Fee Amount'

