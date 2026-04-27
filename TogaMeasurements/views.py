from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required

from .forms import MenMeasurementForm, WomenMeasurementForm
from TogaMeasurements.models import MenMeasurement, WomenMeasurement
from TogaClients.models import Client
from TogaClients.forms import ClientForm


# ---------------------------
# SELECT GENDER ENTRY POINT
# ---------------------------
@login_required
def measurement_select_gender(request):
    return render(request, "measurements/measurement_select_gender.html")


# ---------------------------
# CREATE MEN MEASUREMENT
# ---------------------------
@login_required
def measurement_create_men(request):
    if request.method == "POST":
        client_form = ClientForm(request.POST)
        measurement_form = MenMeasurementForm(request.POST)

        if client_form.is_valid() and measurement_form.is_valid():
            client = client_form.save()
            measurement = measurement_form.save(commit=False)
            measurement.client = client
            measurement.save()
            messages.success(request, "Men’s measurement and client saved successfully!")
            return redirect("measurement_list")
        else:
            messages.error(request, "Please correct the errors below.")
    else:
        client_form = ClientForm()
        measurement_form = MenMeasurementForm()

    return render(request, "measurements/measurement_form.html", {
        "client_form": client_form,
        "form": measurement_form,
        "gender": "men",
    })


# ---------------------------
# CREATE WOMEN MEASUREMENT
# ---------------------------
@login_required
def measurement_create_women(request):
    if request.method == "POST":
        client_form = ClientForm(request.POST)
        measurement_form = WomenMeasurementForm(request.POST)

        if client_form.is_valid() and measurement_form.is_valid():
            client = client_form.save()
            measurement = measurement_form.save(commit=False)
            measurement.client = client
            measurement.save()
            messages.success(request, "Women’s measurement and client saved successfully!")
            return redirect("measurement_list")
        else:
            messages.error(request, "Please correct the errors below.")
    else:
        client_form = ClientForm()
        measurement_form = WomenMeasurementForm()

    return render(request, "measurements/measurement_form.html", {
        "client_form": client_form,
        "form": measurement_form,
        "gender": "women",
    })


# ---------------------------
# EDIT MEASUREMENT
# ---------------------------
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
            messages.success(request, f"{gender} measurement updated successfully!")
            return redirect("client_detail", client_id=measurement.client.id)
        else:
            messages.error(request, "Error updating measurement. Please check the form.")
    else:
        form = form_class(instance=measurement)

    return render(request, "measurements/measurement_form.html", {
        "form": form,
        "client": measurement.client,
        "gender": gender,
        "measurement": measurement,
        "is_edit": True,
    })


# ---------------------------
# DELETE MEASUREMENT
# ---------------------------
@login_required
def measurement_delete(request, measurement_id):
    try:
        measurement = MenMeasurement.objects.get(id=measurement_id)
        gender = "Men"
    except MenMeasurement.DoesNotExist:
        measurement = get_object_or_404(WomenMeasurement, id=measurement_id)
        gender = "Women"

    client = measurement.client

    if request.method == "POST":
        measurement.delete()
        messages.success(request, f"{gender} measurement deleted successfully!")
        return redirect("client_detail", client_id=client.id)

    return render(request, "measurements/measurement_confirm_delete.html", {
        "measurement": measurement,
        "client": client,
        "gender": gender,
    })


# ---------------------------
# LIST ALL MEASUREMENTS
# ---------------------------
@login_required
def measurement_list(request):
    men_measurements = MenMeasurement.objects.select_related("client").all()
    women_measurements = WomenMeasurement.objects.select_related("client").all()
    return render(request, "measurements/measurement_list.html", {
        "men_measurements": men_measurements,
        "women_measurements": women_measurements,
    })


# ---------------------------
# MEASUREMENT DETAIL
# ---------------------------
@login_required
def measurement_detail(request, measurement_id):
    try:
        measurement = MenMeasurement.objects.get(id=measurement_id)
    except MenMeasurement.DoesNotExist:
        measurement = get_object_or_404(WomenMeasurement, id=measurement_id)

    # Build a list of (verbose_name, value) pairs for display
    fields = []
    for field in measurement._meta.fields:
        if field.name not in ["id", "client"]:
            fields.append((field.verbose_name, getattr(measurement, field.name)))

    return render(request, 'measurements/measurement_detail.html', {
        'measurement': measurement,
        'fields': fields,
    })
