from django.contrib import admin
from django.utils.html import format_html
from django.contrib.humanize.templatetags.humanize import intcomma
from .models import Inventory

@admin.register(Inventory)
class InventoryAdmin(admin.ModelAdmin):
    # Overriding standard numeric strings with formatted currency methods
    list_display = (
        "client",
        "description_short",
        "formatted_amount_charged",
        "formatted_amount_deposited",
        "formatted_balance",
        "payment_status_badge",
        "collection_date",
        "received_by",
    )
    
    # Enhanced relational drill-down configuration matrix
    list_filter = ("paid_fully", "date_of_registration", "collection_date")
    search_fields = (
        "client__name", 
        "phone", 
        "description", 
        "received_by", 
        "cleared_by"
    )
    ordering = ("-date_of_registration",)
    
    # Restricting manual tampering with runtime computed parameters
    readonly_fields = ("balance",)

    # --- Custom Model Interface Formatting Column Methods ---

    @admin.display(description="Description")
    def description_short(self, obj):
        """Truncates prose descriptions inside the row matrix."""
        if obj.description and len(obj.description) > 40:
            return f"{obj.description[:40]}..."
        return obj.description

    @admin.display(description="Total Price", ordering="amount_charged")
    def formatted_amount_charged(self, obj):
        return f"₦{intcomma(f'{obj.amount_charged:.2f}')}"

    @admin.display(description="Deposited", ordering="amount_deposited")
    def formatted_amount_deposited(self, obj):
        return f"₦{intcomma(f'{obj.amount_deposited:.2f}')}"

    @admin.display(description="Balance Due", ordering="balance")
    def formatted_balance(self, obj):
        color = "#b02a37" if obj.balance > 0 else "#212529"
        return format_html(
            '<span style="color: {}; font-weight: 600;">₦{}</span>',
            color,
            intcomma(f"{obj.balance:.2f}")
        )

    @admin.display(description="Status", ordering="paid_fully")
    def payment_status_badge(self, obj):
        """Generates clear micro-status badges mapping cleanly to frontend aesthetics."""
        if obj.paid_fully:
            return format_html('<span style="padding: 3px 8px; background: #d1e7dd; color: #0f5132; border-radius: 4px; font-size: 0.75rem; font-weight: bold;">Fully Paid</span>')
        elif obj.amount_deposited > 0:
            return format_html('<span style="padding: 3px 8px; background: #cff4fc; color: #055160; border-radius: 4px; font-size: 0.75rem; font-weight: bold;">Partial</span>')
        return format_html('<span style="padding: 3px 8px; background: #fff3cd; color: #664d03; border-radius: 4px; font-size: 0.75rem; font-weight: bold;">Unpaid</span>')