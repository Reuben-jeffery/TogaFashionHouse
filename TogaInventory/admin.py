from django.contrib import admin
from .models import Inventory

@admin.register(Inventory)
class InventoryAdmin(admin.ModelAdmin):
    list_display = (
        "client",
        "description",
        "amount_charged",
        "amount_deposited",
        "balance",
        "paid_fully",
        "collection_date",
        "received_by",
        "cleared_by",
    )
    list_filter = ("paid_fully", "collection_date")
    search_fields = ("client__name", "description", "received_by", "cleared_by")