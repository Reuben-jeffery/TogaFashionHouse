from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db import transaction

from .forms import MenMeasurementForm, WomenMeasurementForm
from .models import MenMeasurement, WomenMeasurement
from TogaClients.models import Client
from TogaClients.forms import ClientForm

@login_required
def measurement_select_gender(request):
    return render(request, "measurements/measurement_select_gender.html")

@login_required
def measurement_list(request):
    men = MenMeasurement.objects.select_related("client").all().order_by('-date')
    women = WomenMeasurement.objects.select_related("client").all().order_by('-date')
    data_list = [
        ("Men's Measurements", men, "primary", "fa-male", "table-primary"),
        ("Women's Measurements", women, "danger", "fa-female", "table-danger"),
    ]
    return render(request, "measurements/measurement_list.html", {"data_list": data_list})

@login_required
def measurement_create_men(request, client_id=None):
    client = get_object_or_404(Client, id=client_id) if client_id else None
    if request.method == "POST":
        if client:
            form = MenMeasurementForm(request.POST)
            if form.is_valid():
                m = form.save(commit=False)
                m.client = client
                m.created_by = request.user # Automated tracking
                m.save()
                return redirect("client_detail", client_id=client.id)
        else:
            cf, mf = ClientForm(request.POST), MenMeasurementForm(request.POST)
            if cf.is_valid() and mf.is_valid():
                with transaction.atomic():
                    c = cf.save()
                    m = mf.save(commit=False)
                    m.client = c
                    m.created_by = request.user # Automated tracking
                    m.save()
                return redirect("measurement_list")
    return render(request, "measurements/measurement_form.html", {
        "client_form": ClientForm() if not client else None, "form": MenMeasurementForm(),
        "gender": "Men", "client": client
    })

@login_required
def measurement_create_women(request, client_id=None):
    client = get_object_or_404(Client, id=client_id) if client_id else None
    if request.method == "POST":
        if client:
            form = WomenMeasurementForm(request.POST)
            if form.is_valid():
                m = form.save(commit=False)
                m.client = client
                m.created_by = request.user # Automated tracking
                m.save()
                return redirect("client_detail", client_id=client.id)
        else:
            cf, mf = ClientForm(request.POST), WomenMeasurementForm(request.POST)
            if cf.is_valid() and mf.is_valid():
                with transaction.atomic():
                    c = cf.save()
                    m = mf.save(commit=False)
                    m.client = c
                    m.created_by = request.user # Automated tracking
                    m.save()
                return redirect("measurement_list")
    return render(request, "measurements/measurement_form.html", {
        "client_form": ClientForm() if not client else None, "form": WomenMeasurementForm(),
        "gender": "Women", "client": client
    })

@login_required
def measurement_detail(request, measurement_id):
    try: measurement = MenMeasurement.objects.get(id=measurement_id)
    except MenMeasurement.DoesNotExist: measurement = get_object_or_404(WomenMeasurement, id=measurement_id)
    return render(request, 'measurements/measurement_detail.html', {'measurement': measurement})

@login_required
def measurement_edit(request, measurement_id):
    try:
        m = MenMeasurement.objects.get(id=measurement_id); f, g = MenMeasurementForm, "Men"
    except MenMeasurement.DoesNotExist:
        m = get_object_or_404(WomenMeasurement, id=measurement_id); f, g = WomenMeasurementForm, "Women"
    if request.method == "POST":
        form = f(request.POST, instance=m)
        if form.is_valid():
            form.save()
            return redirect("measurement_list")
    return render(request, "measurements/measurement_form.html", {"form": f(instance=m), "is_edit": True, "gender": g})

@login_required
def measurement_delete(request, measurement_id):
    try: m = MenMeasurement.objects.get(id=measurement_id)
    except MenMeasurement.DoesNotExist: m = get_object_or_404(WomenMeasurement, id=measurement_id)
    if request.method == "POST":
        m.delete()
        return redirect("measurement_list")
    return render(request, "measurements/measurement_confirm_delete.html", {"measurement": m})