from django.contrib import admin
from .models import MenMeasurement, WomenMeasurement

@admin.register(MenMeasurement)
class MenMeasurementAdmin(admin.ModelAdmin):
    list_display = ("client", "date", "tailors_name")
    search_fields = ("client__name", "tailors_name")
    list_filter = ("date",)

@admin.register(WomenMeasurement)
class WomenMeasurementAdmin(admin.ModelAdmin):
    list_display = ("client", "date", "tailors_name")
    search_fields = ("client__name", "tailors_name")
    list_filter = ("date",)
