import json
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth.forms import UserCreationForm
from django.db.models import Count, Q
from django.utils.safestring import mark_safe

# Core Application Module Dependencies
from .models import Client
from .forms import ClientForm
from TogaInventory.models import Inventory
from TogaMeasurements.models import MenMeasurement, WomenMeasurement


# ==========================================================================
# Elite Client Domain Layer Control Pipeline
# ==========================================================================

@login_required
def client_list(request):
    """
    Renders the primary customer table workspace dataset with filtering mechanics.
    """
    search_query = request.GET.get("search", "").strip()
    gender_filter = request.GET.get("gender", "").strip()

    # Base selective pre-fetch architecture initialization
    clients = Client.objects.all()

    # Multi-field search interceptor query execution
    if search_query:
        clients = clients.filter(
            Q(name__icontains=search_query) |
            Q(phone__icontains=search_query)
        )

    # Monochromatic categorical gender flags verification parameters
    if gender_filter in [Client.GenderOptions.MALE, Client.GenderOptions.FEMALE]:
        clients = clients.filter(gender=gender_filter)

    return render(request, "clients/client_list.html", {
        "clients": clients,
        "current_search": search_query,
        "current_gender": gender_filter
    })


@login_required
def client_detail(request, client_id):
    """
    Aggregates profile contexts, custom sizing files, and dedicated inventory maps.
    """
    client = get_object_or_404(Client, id=client_id)

    # Database reference lookups mapping configuration pipelines
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
@permission_required("TogaClients.add_client", raise_exception=True)
def client_create(request):
    """
    Injects new profile identities securely into the system database logs.
    """
    if request.method == "POST":
        form = ClientForm(request.POST)
        if form.is_valid():
            client = form.save()
            messages.success(request, "Client profile initialized and verified successfully.")
            return redirect("client_detail", client_id=client.id)
        messages.error(request, "Configuration errors detected. Verification stalled.")
    else:
        form = ClientForm()
        
    return render(request, "clients/client_form.html", {"form": form, "action": "Create"})


@login_required
@permission_required("TogaClients.change_client", raise_exception=True)
def client_edit(request, client_id):
    """
    Modifies custom business metrics and metadata fields inside instance records.
    """
    client = get_object_or_404(Client, id=client_id)
    if request.method == "POST":
        form = ClientForm(request.POST, instance=client)
        if form.is_valid():
            form.save()
            messages.success(request, "Client dataset parameters saved securely.")
            return redirect("client_detail", client_id=client.id)
        messages.error(request, "Profile synchronization payload execution failure.")
    else:
        form = ClientForm(instance=client)
        
    return render(request, "clients/client_form.html", {"form": form, "client": client, "action": "Update"})


@login_required
@permission_required("TogaClients.delete_client", raise_exception=True)
def client_delete(request, client_id):
    """
    Purges client files permanently from primary database indexing structures.
    """
    client = get_object_or_404(Client, id=client_id)
    if request.method == "POST":
        client.delete()
        messages.success(request, "Target customer directory entry deleted securely.")
        return redirect("client_list")
        
    return render(request, "clients/client_confirm_delete.html", {"client": client})


# ==========================================================================
# Interactive Profile Registration Gateways
# ==========================================================================

def register(request):
    """
    Public access onboarding terminal pipelines for operational credential structures.
    """
    if request.user.is_authenticated:
        return redirect("dashboard")

    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, "Atelier interface profile initialization authorized.")
            return redirect("dashboard")
        messages.error(request, "Credential structural rejection. Please audit input limits.")
    else:
        form = UserCreationForm()
        
    return render(request, "registration/register.html", {"form": form})


# ==========================================================================
# Central Corporate Management Dashboard Terminal
# ==========================================================================

@login_required
def dashboard(request):
    """
    Gathers telemetry insights, total metric evaluations, and JSON rendering packages.
    """
    # KPI Metric Summarization Optimization Framework
    metrics_context = {
        "client_count": Client.objects.count(),
        "inventory_count": Inventory.objects.count(),
        "men_measurement_count": MenMeasurement.objects.count(),
        "women_measurement_count": WomenMeasurement.objects.count(),
    }

    # Extract charting relationship values without breaking template namespaces
    inventories_per_client = Client.objects.annotate(
        inventory_total=Count("inventories")
    ).filter(inventory_total__gt=0)[:10]  # Limited to top 10 profiles for clean canvas balancing

    chart_labels = [c.name for c in inventories_per_client]
    chart_data = [c.inventory_total for c in inventories_per_client]

    # Clean JSON serialization block mapping setup
    metrics_context.update({
        "inventories_per_client": inventories_per_client,
        "chart_labels": mark_safe(json.dumps(chart_labels)),
        "chart_data": mark_safe(json.dumps(chart_data)),
    })

    return render(request, "dashboard.html", metrics_context)