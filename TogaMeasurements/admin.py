from django.contrib import admin
from .models import MenMeasurement, WomenMeasurement

class BaseMeasurementAdmin(admin.ModelAdmin):
    # Updated: Changed 'tailors_name' to 'tailor_name'
    list_display = ("client", "date", "tailor_name", "created_by")
    search_fields = ("client__name", "tailor_name")
    list_filter = ("date", "tailor_name")
    readonly_fields = ("date", "created_by") # Added created_by here as it's set by the system
    
    # Helper to exclude fields we don't want to list in fieldsets
    def get_fieldsets(self, request, obj=None):
        # Dynamically get field names, excluding system/auto fields
        all_fields = [f.name for f in self.model._meta.fields 
                      if f.name not in ['id', 'updated_at']]
        
        return (
            ('Basic Info', {
                'fields': ('client', 'tailor_name', 'date', 'created_by')
            }),
            ('Body Measurements', {
                'classes': ('collapse',),
                'fields': [f for f in all_fields if f not in ['client', 'tailor_name', 'date', 'created_by']]
            }),
        )

@admin.register(MenMeasurement)
class MenMeasurementAdmin(BaseMeasurementAdmin):
    pass

@admin.register(WomenMeasurement)
class WomenMeasurementAdmin(BaseMeasurementAdmin):
    pass