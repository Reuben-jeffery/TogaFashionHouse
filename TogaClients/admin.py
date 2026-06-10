from django.contrib import admin
from django.utils.html import format_html
from .models import Client

@admin.register(Client)
class ClientAdmin(admin.ModelAdmin):
    # Core Layout Field Pipelines
    list_display = (
        "name_identity_badge", 
        "formatted_phone", 
        "gender_badge", 
        "registration_timeline", 
        "last_order_date"
    )
    
    list_display_links = ("name_identity_badge",)
    
    search_fields = ("name", "phone")
    
    list_filter = (
        "gender", 
        ("created_at", admin.DateFieldListFilter),  # Date hierarchy dropdown configuration
    )
    
    ordering = ("-created_at", "name")
    
    # Structural Detail Form Grid Configurations
    fieldsets = (
        ("Core Identity Parameters", {
            "fields": ("name", "gender"),
            "description": "Primary client profile metadata elements."
        }),
        ("Communication Channels", {
            "fields": ("phone",),
        }),
    )

    # Custom Presentation Decorators & Fields
    @admin.display(ordering="name", description="Client Identity")
    def name_identity_badge(self, obj):
        """Renders an elegant typographic entry layout for client identities."""
        return format_html(
            '<strong style="color: #111111; font-weight: 600;">{}</strong>', 
            obj.name
        )

    @admin.display(ordering="phone", description="Phone Channel")
    def formatted_phone(self, obj):
        """Displays phone values using code monospacing rules."""
        if not obj.phone:
            return format_html('<span style="color: #8c857e; font-style: italic;">—</span>')
        return format_html(
            '<code style="font-family: monospace; font-size: 0.85rem; color: #5c5552;">{}</code>', 
            obj.phone
        )

    @admin.display(ordering="gender", description="Gender")
    def gender_badge(self, obj):
        """Renders subtle, clean monochromatic context flags for user tags."""
        if not obj.gender:
            return "—"
        
        # Subtle, neutral-toned inline styles mapping
        color_map = {
            "male": ("#2b2927", "#eeebe7"),
            "female": ("#4a4542", "#f6f4f0"),
        }
        text_color, bg_color = color_map.get(obj.gender.lower(), ("#5c5552", "#faf9f6"))
        
        return format_html(
            '<span style="padding: 0.2rem 0.5rem; background: {}; color: {}; '
            'border-radius: 4px; font-size: 0.75rem; font-weight: 600; '
            'text-transform: uppercase; letter-spacing: 0.5px;">{}</span>',
            bg_color, text_color, obj.gender
        )

    @admin.display(ordering="created_at", description="Enrolled")
    def registration_timeline(self, obj):
        """Formates entry timestamps without unnecessary seconds values."""
        if not obj.created_at:
            return "—"
        return obj.created_at.strftime("%b %d, %Y")