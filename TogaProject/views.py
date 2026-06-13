from django.contrib.auth.decorators import login_required, user_passes_test
from django.shortcuts import render, redirect
from django.db.models import Count, Sum
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from django.contrib import messages
from django.utils.safestring import mark_safe
from django.utils import timezone
from datetime import timedelta
import json

from TogaClients.models import Client
from TogaInventory.models import Inventory
from TogaMeasurements.models import MenMeasurement, WomenMeasurement

# --- Helper: Permissions ---
def is_admin(user):
    return user.is_superuser or user.groups.filter(name="Admin").exists()

# --- Auth & Registration ---
def register(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('dashboard_router')
    else:
        form = UserCreationForm()
    return render(request, "registration/register.html", {"form": form})

# --- Dashboard Routing ---
def home_view(request):
    if not User.objects.filter(username='admin').exists():
        User.objects.create_superuser('admin', 'admin@togafashionhouse.com', 'TogaSecure2026!')
    
    if request.user.is_authenticated:
        return redirect('dashboard_router')
    return redirect('login')

@login_required
def dashboard_router(request):
    if is_admin(request.user):
        return redirect('admin_dashboard')
    return redirect('worker_dashboard')

# --- Dashboards ---
@login_required
def dashboard(request):
    """General overview dashboard."""
    men_count = MenMeasurement.objects.count()
    women_count = WomenMeasurement.objects.count()
    
    financial_agg = Inventory.objects.filter(paid_fully=False).aggregate(total=Sum('balance'))
    total_outstanding = financial_agg['total'] or 0
    
    today = timezone.now().date()
    upcoming_due = Inventory.objects.filter(collection_date__gte=today).order_by('collection_date')[:10]
    client_stats = Client.objects.annotate(inventory_total=Count('inventories', distinct=True))

    context = {
        'client_count': Client.objects.count(),
        'inventory_count': Inventory.objects.count(),
        'measurement_count': men_count + women_count,
        'total_outstanding': total_outstanding,
        'upcoming_due': upcoming_due,
        'inventory_labels': mark_safe(json.dumps([c.name for c in client_stats])),
        'inventory_counts': mark_safe(json.dumps([c.inventory_total for c in client_stats])),
    }
    return render(request, 'dashboard.html', context)

@login_required
def worker_dashboard(request):
    """Worker console - rendering explicitly to the nested path."""
    inventories = Inventory.objects.filter(created_by=request.user)
    upcoming_due = inventories.filter(
        collection_date__lte=timezone.now() + timedelta(days=3),
        balance__gt=0
    )
    if upcoming_due.exists():
        messages.warning(request, f"You have {upcoming_due.count()} unpaid orders due soon!")
    
    # This path matches the confirmed location: TogaInventory/templates/inventory/workers/dashboard.html
    return render(request, "inventory/workers/dashboard.html", {
        "inventories": inventories, 
        "upcoming_due": upcoming_due
    })

@login_required
@user_passes_test(is_admin)
def admin_dashboard(request):
    def get_monthly_data(model):
        return model.objects.values('created_at__month').annotate(count=Count('id')).order_by('created_at__month')

    client_stats = get_monthly_data(Client)
    inv_stats = get_monthly_data(Inventory)
    roles = User.objects.values('groups__name').annotate(count=Count('id'))

    return render(request, "admin_dashboard.html", {
        "client_labels": [c['created_at__month'] for c in client_stats],
        "client_data": [c['count'] for c in client_stats],
        "inventory_labels": [i['created_at__month'] for i in inv_stats],
        "inventory_data": [i['count'] for i in inv_stats],
        "role_labels": [r['groups__name'] or "No Group" for r in roles],
        "role_data": [r['count'] for r in roles],
    })

@login_required
def role_list(request):
    return render(request, "roles/role_list.html", {"roles": []})