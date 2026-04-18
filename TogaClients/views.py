from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from django.db.models import Count
from django.utils.safestring import mark_safe
import json

# Correct imports
from .models import Client
from .forms import ClientForm
from TogaInventory.models import Inventory
from TogaMeasurements.models import MenMeasurement, WomenMeasurement


# ---------------- CLIENT VIEWS ---------------- #

@login_required
def client_list(request):
    clients = Client.objects.all()
    return render(request, "clients/client_list.html", {"clients": clients})


@login_required
def client_detail(request, client_id):
    client = get_object_or_404(Client, id=client_id)

    # Related records
    inventories = client.inventories.all()
    men_measurements = MenMeasurement.objects.filter(client=client)
    women_measurements = WomenMeasurement.objects.filter(client=client)

    return render(request, "clients/client_detail.html", {
        "client": client,
        "inventories": inventories,
        "men_measurements": men_measurements,
        "women_measurements": women_measurements,
    })


@login_required
@permission_required("TogaClients.add_client")
def client_create(request):
    if request.method == "POST":
        form = ClientForm(request.POST)
        if form.is_valid():
            client = form.save()
            messages.success(request, "Client added successfully!")
            return redirect("client_detail", client_id=client.id)
        messages.error(request, "There was an error adding the client.")
    else:
        form = ClientForm()
    return render(request, "clients/client_form.html", {"form": form})


@login_required
def client_edit(request, client_id):
    client = get_object_or_404(Client, id=client_id)
    if request.method == "POST":
        form = ClientForm(request.POST, instance=client)
        if form.is_valid():
            form.save()
            messages.success(request, "Client updated successfully!")
            return redirect("client_detail", client_id=client.id)
        messages.error(request, "There was an error updating the client.")
    else:
        form = ClientForm(instance=client)
    return render(request, "clients/client_form.html", {"form": form})


@login_required
def client_delete(request, client_id):
    client = get_object_or_404(Client, id=client_id)
    if request.method == "POST":
        client.delete()
        messages.success(request, "Client deleted successfully!")
        return redirect("client_list")
    return render(request, "clients/client_confirm_delete.html", {"client": client})


# ---------------- USER REGISTRATION ---------------- #

def register(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, "Account created successfully!")
            return redirect("client_list")
        messages.error(request, "There was an error creating the account.")
    else:
        form = UserCreationForm()
    return render(request, "register.html", {"form": form})


# ---------------- DASHBOARD ---------------- #

@login_required
def dashboard(request):
    client_count = Client.objects.count()
    inventory_count = Inventory.objects.count()
    men_measurement_count = MenMeasurement.objects.count()
    women_measurement_count = WomenMeasurement.objects.count()

    # Inventories per client
    inventories_per_client = Client.objects.annotate(inventory_total=Count("inventories"))

    chart_labels = [client.name for client in inventories_per_client]
    chart_data = [client.inventory_total for client in inventories_per_client]

    return render(request, "dashboard.html", {
        "client_count": client_count,
        "inventory_count": inventory_count,
        "men_measurement_count": men_measurement_count,
        "women_measurement_count": women_measurement_count,
        "inventories_per_client": inventories_per_client,
        "chart_labels": mark_safe(json.dumps(chart_labels)),
        "chart_data": mark_safe(json.dumps(chart_data)),
    })
