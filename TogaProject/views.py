from django.contrib.auth.decorators import login_required, user_passes_test
from django.shortcuts import render, redirect, get_object_or_404
from django.db.models import Count, F, Sum
from django.db.models.functions import TruncMonth
from django.contrib.auth.models import User
from django.contrib import messages
from django.db import transaction, IntegrityError
from django.http import HttpResponse
from django.core.mail import send_mail
import csv
import json
from datetime import timedelta
from django.utils.safestring import mark_safe
from django.utils.timezone import now

# Auth imports for register view
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login

# Import models and forms from each app
from TogaClients.models import Client
from TogaClients.forms import ClientForm
from TogaInventory.models import Inventory
from TogaInventory.forms import InventoryForm
from TogaMeasurements.models import MenMeasurement, WomenMeasurement
from TogaMeasurements.forms import MenMeasurementForm, WomenMeasurementForm
from django.utils import timezone

@login_required
def dashboard(request):
    client_count = Client.objects.count()
    inventory_count = Inventory.objects.count()

    # Separate measurement counts
    men_measurement_count = MenMeasurement.objects.count()
    women_measurement_count = WomenMeasurement.objects.count()
    measurement_count = men_measurement_count + women_measurement_count

    # Inventory per client
    inventories_per_client = Client.objects.annotate(inventory_total=Count('inventories'))
    inventory_labels = [client.name for client in inventories_per_client]
    inventory_counts = [client.inventory_total for client in inventories_per_client]

    # Payments summary (based on Inventory financials)
    payments_per_client = Client.objects.annotate(
        total_deposits=Sum('inventories__amount_deposited')
    )
    payments_labels = [client.name for client in payments_per_client]
    payments_data = [client.total_deposits or 0 for client in payments_per_client]

    context = {
        'client_count': client_count,
        'inventory_count': inventory_count,
        'measurement_count': measurement_count,
        'men_measurement_count': men_measurement_count,
        'women_measurement_count': women_measurement_count,
        'inventory_labels': mark_safe(json.dumps(inventory_labels)),
        'inventory_counts': mark_safe(json.dumps(inventory_counts)),
        'payments_labels': mark_safe(json.dumps(payments_labels)),
        'payments_data': mark_safe(json.dumps(payments_data)),
    }
    return render(request, 'dashboard.html', context)

@login_required
def worker_dashboard(request):
    # Only inventories created by this worker
    inventories = Inventory.objects.filter(created_by=request.user)

    # Upcoming collections within 3 days, unpaid only
    upcoming_due = inventories.filter(
        collection_date__lte=timezone.now() + timedelta(days=3),
        balance__gt=0
    )

    if upcoming_due.exists():
        messages.warning(
            request,
            f"You have {upcoming_due.count()} unpaid inventories with collection dates due soon!"
        )

    return render(request, "workers/dashboard.html", {
        "inventories": inventories,
        "upcoming_due": upcoming_due,
    })

def register(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)  # log them in immediately
            return redirect('dashboard')
    else:
        form = UserCreationForm()
    return render(request, "registration/register.html", {"form": form})


def is_admin(user):
    return user.is_superuser or user.groups.filter(name="Admin").exists()


@login_required
@user_passes_test(is_admin)
def admin_dashboard(request):
    # Clients per month
    clients_per_month = (
        Client.objects.values('created_at__month')
        .annotate(count=Count('id'))
        .order_by('created_at__month')
    )
    client_labels = [c['created_at__month'] for c in clients_per_month]
    client_data = [c['count'] for c in clients_per_month]

    # Inventory per month
    inventories_per_month = (
        Inventory.objects.values('created_at__month')
        .annotate(count=Count('id'))
        .order_by('created_at__month')
    )
    inventory_labels = [i['created_at__month'] for i in inventories_per_month]
    inventory_data = [i['count'] for i in inventories_per_month]

    # Employee role distribution
    roles = User.objects.values('groups__name').annotate(count=Count('id'))
    role_labels = [r['groups__name'] or "No Group" for r in roles]
    role_data = [r['count'] for r in roles]

    context = {
        "client_labels": client_labels,
        "client_data": client_data,
        "inventory_labels": inventory_labels,
        "inventory_data": inventory_data,
        "role_labels": role_labels,
        "role_data": role_data,
    }
    return render(request, "admin_dashboard.html", context)


@login_required
def role_list(request):
    roles = []  # Replace with your actual logic for roles
    return render(request, "roles/role_list.html", {"roles": roles})
