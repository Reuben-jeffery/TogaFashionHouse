from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db import transaction

from .forms import MenMeasurementForm, WomenMeasurementForm
from TogaMeasurements.models import MenMeasurement, WomenMeasurement
from TogaClients.forms import ClientForm

# --- 1. SELECT GENDER ---
@login_required
def measurement_select_gender(request):
    return render(request, "measurements/measurement_select_gender.html")

# --- 2. CREATE MEN ---
@login_required
def measurement_create_men(request):
    if request.method == "POST":
        client_form = ClientForm(request.POST)
        measurement_form = MenMeasurementForm(request.POST)
        if client_form.is_valid() and measurement_form.is_valid():
            with transaction.atomic():
                client = client_form.save()
                measurement = measurement_form.save(commit=False)
                measurement.client = client
                measurement.save()
            messages.success(request, "Men’s measurement saved successfully!")
            return redirect("measurement_list")
    else:
        client_form = ClientForm()
        measurement_form = MenMeasurementForm()
    return render(request, "measurements/measurement_form.html", {
        "client_form": client_form, "form": measurement_form, "gender": "Men"
    })

# --- 3. CREATE WOMEN ---
@login_required
def measurement_create_women(request):
    if request.method == "POST":
        client_form = ClientForm(request.POST)
        measurement_form = WomenMeasurementForm(request.POST)
        if client_form.is_valid() and measurement_form.is_valid():
            with transaction.atomic():
                client = client_form.save()
                measurement = measurement_form.save(commit=False)
                measurement.client = client
                measurement.save()
            messages.success(request, "Women’s measurement saved successfully!")
            return redirect("measurement_list")
    else:
        client_form = ClientForm()
        measurement_form = WomenMeasurementForm()
    return render(request, "measurements/measurement_form.html", {
        "client_form": client_form, "form": measurement_form, "gender": "Women"
    })

# --- 4. LIST ALL (Corrected for your template loop) ---
@login_required
def measurement_list(request):
    men = MenMeasurement.objects.select_related("client").all().order_by('-date')
    women = WomenMeasurement.objects.select_related("client").all().order_by('-date')
    
    # This structure is REQUIRED by your current measurement_list.html template
    data_list = [
        ("Men's Measurements", men, "primary", "fa-male", "table-primary"),
        ("Women's Measurements", women, "danger", "fa-female", "table-danger"),
    ]
    
    return render(request, "measurements/measurement_list.html", {"data_list": data_list})

# --- 5. DETAIL ---
@login_required
def measurement_detail(request, measurement_id):
    # Try fetching as Men, if not found, try Women
    try:
        measurement = MenMeasurement.objects.get(id=measurement_id)
    except MenMeasurement.DoesNotExist:
        measurement = get_object_or_404(WomenMeasurement, id=measurement_id)
    return render(request, 'measurements/measurement_detail.html', {'measurement': measurement})

# --- 6. EDIT ---
@login_required
def measurement_edit(request, measurement_id):
    try:
        measurement = MenMeasurement.objects.get(id=measurement_id)
        form_class = MenMeasurementForm
        gender = "Men"
    except MenMeasurement.DoesNotExist:
        measurement = get_object_or_404(WomenMeasurement, id=measurement_id)
        form_class = WomenMeasurementForm
        gender = "Women"
    
    if request.method == "POST":
        form = form_class(request.POST, instance=measurement)
        if form.is_valid():
            form.save()
            messages.success(request, f"{gender} measurement updated!")
            return redirect("measurement_list")
    else:
        form = form_class(instance=measurement)
    return render(request, "measurements/measurement_form.html", {"form": form, "is_edit": True, "gender": gender})

# --- 7. DELETE ---
@login_required
def measurement_delete(request, measurement_id):
    try:
        measurement = MenMeasurement.objects.get(id=measurement_id)
    except MenMeasurement.DoesNotExist:
        measurement = get_object_or_404(WomenMeasurement, id=measurement_id)
    
    if request.method == "POST":
        measurement.delete()
        messages.success(request, "Measurement deleted successfully.")
        return redirect("measurement_list")
    return render(request, "measurements/measurement_confirm_delete.html", {"measurement": measurement})