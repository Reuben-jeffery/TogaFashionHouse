from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from datetime import timedelta

from .models import Inventory, Deposit
from .forms import InventoryForm, DepositForm

# ---------------- INVENTORY VIEWS ---------------- #

@login_required
def inventory_list(request):
    inventories = Inventory.objects.select_related('client').all()
    return render(request, 'inventory/inventory_list.html', {'inventories': inventories})

@login_required
def inventory_detail(request, inventory_id):
    inventory = get_object_or_404(Inventory, id=inventory_id)
    return render(request, 'inventory/inventory_detail.html', {
        'inventory': inventory,
        'deposits': inventory.deposits.all().order_by("date"),
        'deposit_form': DepositForm()
    })

@login_required
def add_inventory(request):
    if request.method == "POST":
        form = InventoryForm(request.POST)
        if form.is_valid():
            inventory = form.save(commit=False)
            inventory.created_by = request.user
            inventory.save()
            # Ensure calculations are triggered on new records
            inventory.update_deposit_summary()
            messages.success(request, "Inventory record created successfully!")
            return redirect("inventory_detail", inventory_id=inventory.id)
    else:
        form = InventoryForm()
    return render(request, "inventory/inventory_form.html", {"form": form})

@login_required
def inventory_edit(request, inventory_id):
    inventory = get_object_or_404(Inventory, id=inventory_id)
    if request.method == 'POST':
        form = InventoryForm(request.POST, instance=inventory)
        if form.is_valid():
            form.save()
            # Ensure calculations are triggered after editing amounts
            inventory.update_deposit_summary()
            messages.success(request, "Inventory updated successfully!")
            return redirect('inventory_detail', inventory_id=inventory.id)
    else:
        form = InventoryForm(instance=inventory)
    return render(request, 'inventory/inventory_form.html', {'form': form, 'inventory': inventory})

@login_required
def inventory_mark_paid(request, inventory_id):
    inventory = get_object_or_404(Inventory, id=inventory_id)
    # Using the model method is safer than manual setting
    inventory.paid_fully = True
    inventory.update_deposit_summary() 
    messages.success(request, "Inventory marked as Paid Fully.")
    return redirect('inventory_detail', inventory_id=inventory.id)

@login_required
def inventory_delete(request, inventory_id):
    inventory = get_object_or_404(Inventory, id=inventory_id)
    if request.method == 'POST':
        inventory.delete()
        messages.success(request, "Inventory record deleted successfully!")
        return redirect('inventory_list')
    return render(request, 'inventory/inventory_confirm_delete.html', {'inventory': inventory})

# ---------------- WORKER DASHBOARD ---------------- #

@login_required
@login_required
def worker_dashboard(request):
    inventories = Inventory.objects.filter(created_by=request.user)
    upcoming_due = inventories.filter(
        collection_date__lte=timezone.now() + timedelta(days=3),
        balance__gt=0
    )
    # This path MUST match the directory structure inside TogaInventory/templates/
    return render(request, "inventory/workers/dashboard.html", {
        "inventories": inventories,
        "upcoming_due": upcoming_due,
    })

# ---------------- DEPOSIT VIEWS ---------------- #

@login_required
def add_deposit(request, inventory_id):
    inventory = get_object_or_404(Inventory, id=inventory_id)
    if request.method == "POST":
        form = DepositForm(request.POST)
        if form.is_valid():
            deposit = form.save(commit=False)
            deposit.inventory = inventory
            # Saving the deposit automatically triggers your Deposit model's save() 
            # method, which runs inventory.update_deposit_summary()
            deposit.save()
            messages.success(request, "Deposit recorded successfully!")
    return redirect("inventory_detail", inventory_id=inventory.id)