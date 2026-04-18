from django.contrib import admin
from .models import Client

# Register your Client model with custom admin options
@admin.register(Client)
class ClientAdmin(admin.ModelAdmin):
    list_display = ("name", "phone", "gender", "created_at", "last_order_date")
    search_fields = ("name", "phone")
    list_filter = ("gender", "created_at")