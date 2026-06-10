from django.contrib import admin
from .models import MenMeasurement, WomenMeasurement

# Helper to avoid repeating logic
class BaseMeasurementAdmin(admin.ModelAdmin):
    list_display = ("client", "date", "tailors_name")
    search_fields = ("client__name", "tailors_name")
    list_filter = ("date", "tailors_name")
    readonly_fields = ("date",) # Prevent accidental date changes
    
    # Organize fields into logical groups for better UI
    fieldsets = (
        ('Basic Info', {
            'fields': ('client', 'tailors_name', 'date')
        }),
        ('Body Measurements', {
            'classes': ('collapse',), # Keeps it hidden by default to declutter
            'fields': tuple(
                [f.name for f in MenMeasurement._meta.fields 
                 if f.name not in ['id', 'client', 'tailors_name', 'date', 'updated_at']]
            )
        }),
    )

@admin.register(MenMeasurement)
class MenMeasurementAdmin(BaseMeasurementAdmin):
    pass

@admin.register(WomenMeasurement)
class WomenMeasurementAdmin(BaseMeasurementAdmin):
    pass