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
    """Show all inventories with related client data."""
    inventories = Inventory.objects.select_related('client').all()
    return render(request, 'inventory/inventory_list.html', {'inventories': inventories})


@login_required
def inventory_detail(request, inventory_id):
    """Single inventory detail view with deposits."""
    inventory = get_object_or_404(Inventory, id=inventory_id)
    deposits = inventory.deposits.all().order_by("date")  # show deposit history
    deposit_form = DepositForm()

    return render(request, 'inventory/inventory_detail.html', {
        'inventory': inventory,
        'deposits': deposits,
        'deposit_form': deposit_form
    })


@login_required
def add_inventory(request):
    """Create a new inventory record."""
    if request.method == "POST":
        form = InventoryForm(request.POST)
        if form.is_valid():
            inventory = form.save(commit=False)
            inventory.created_by = request.user

            # Auto-calculate balance using cleaned data
            inventory.balance = inventory.amount_charged - inventory.amount_deposited

            # Update paid_fully flag if balance is zero
            if inventory.balance <= 0:
                inventory.paid_fully = True
                inventory.paid_fully_date = timezone.now()

            inventory.save()
            messages.success(request, "Inventory record created successfully!")
            return redirect("inventory_detail", inventory_id=inventory.id)
        else:
            messages.error(request, "There was an error creating the inventory record.")
    else:
        form = InventoryForm()

    return render(request, "inventory/inventory_form.html", {"form": form})


@login_required
def inventory_edit(request, inventory_id):
    """Edit an existing inventory record."""
    inventory = get_object_or_404(Inventory, id=inventory_id)
    if request.method == 'POST':
        form = InventoryForm(request.POST, instance=inventory)
        if form.is_valid():
            inventory = form.save(commit=False)

            # Recalculate balance using cleaned data
            inventory.balance = inventory.amount_charged - inventory.amount_deposited

            # Update paid_fully flag if balance is zero
            if inventory.balance <= 0:
                inventory.paid_fully = True
                if not inventory.paid_fully_date:
                    inventory.paid_fully_date = timezone.now()
            else:
                inventory.paid_fully = False
                inventory.paid_fully_date = None

            inventory.save()
            messages.success(request, "Inventory record updated successfully!")
            return redirect('inventory_detail', inventory_id=inventory.id)
        else:
            messages.error(request, "There was an error updating the inventory record.")
    else:
        form = InventoryForm(instance=inventory)

    return render(request, 'inventory/inventory_form.html', {
        'form': form,
        'inventory': inventory
    })


@login_required
def inventory_mark_paid(request, inventory_id):
    """Manually mark an inventory as fully paid."""
    inventory = get_object_or_404(Inventory, id=inventory_id)
    inventory.paid_fully = True
    inventory.paid_fully_date = timezone.now()
    inventory.balance = 0
    inventory.save()
    messages.success(request, "Inventory marked as Paid Fully.")
    return redirect('inventory_detail', inventory_id=inventory.id)


@login_required
def inventory_delete(request, inventory_id):
    """Delete an inventory record."""
    inventory = get_object_or_404(Inventory, id=inventory_id)
    if request.method == 'POST':
        inventory.delete()
        messages.success(request, "Inventory record deleted successfully!")
        return redirect('inventory_list')
    return render(request, 'inventory/inventory_confirm_delete.html', {'inventory': inventory})


@login_required
def worker_dashboard(request):
    """Dashboard showing inventories created by the logged-in worker."""
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


# ---------------- DEPOSIT VIEWS ---------------- #

@login_required
def add_deposit(request, inventory_id):
    """Add a new deposit to an inventory record."""
    inventory = get_object_or_404(Inventory, id=inventory_id)

    if request.method == "POST":
        form = DepositForm(request.POST)
        if form.is_valid():
            deposit = form.save(commit=False)
            deposit.inventory = inventory
            deposit.save()

            # Update inventory totals
            inventory.update_deposit_summary()

            messages.success(request, "Deposit recorded successfully!")
            return redirect("inventory_detail", inventory_id=inventory.id)
        else:
            messages.error(request, "There was an error recording the deposit.")
    else:
        form = DepositForm()

    return render(request, "inventory/deposit_form.html", {
        "form": form,
        "inventory": inventory
    })
