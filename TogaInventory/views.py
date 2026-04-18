from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from .models import Inventory
from .forms import InventoryForm
from datetime import timedelta

# ---------------- INVENTORY VIEWS ---------------- #

@login_required
def inventory_list(request):
    inventories = Inventory.objects.select_related('client').all()
    return render(request, 'inventory/inventory_list.html', {'inventories': inventories})


@login_required
def inventory_detail(request, inventory_id):
    inventory = get_object_or_404(Inventory, id=inventory_id)
    return render(request, 'inventory/inventory_detail.html', {'inventory': inventory})


@login_required
def add_inventory(request):
    if request.method == "POST":
        form = InventoryForm(request.POST)
        if form.is_valid():
            inventory = form.save(commit=False)
            inventory.created_by = request.user  # tie to worker
            inventory.save()
            messages.success(request, "Inventory record created successfully!")
            return redirect("inventory_detail", inventory_id=inventory.id)
        else:
            messages.error(request, "There was an error creating the inventory record.")
    else:
        form = InventoryForm()

    return render(request, "inventory/add_inventory.html", {"form": form})


@login_required
def inventory_edit(request, inventory_id):
    inventory = get_object_or_404(Inventory, id=inventory_id)
    if request.method == 'POST':
        form = InventoryForm(request.POST, instance=inventory)
        if form.is_valid():
            form.save()
            messages.success(request, "Inventory record updated successfully!")
            return redirect('inventory_detail', inventory_id=inventory.id)
        else:
            messages.error(request, "There was an error updating the inventory record.")
    else:
        form = InventoryForm(instance=inventory)
    return render(request, 'inventory/inventory_form.html', {'form': form, 'inventory': inventory})


@login_required
def inventory_mark_paid(request, inventory_id):
    inventory = get_object_or_404(Inventory, id=inventory_id)
    inventory.paid_fully = True
    inventory.paid_fully_date = timezone.now()
    inventory.balance = 0
    inventory.save()
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
