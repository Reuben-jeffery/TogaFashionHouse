from django.urls import path
from . import views

urlpatterns = [
    # Remove the 'inventory/' prefix from these paths
    path("", views.inventory_list, name="inventory_list"),
    path("add/", views.add_inventory, name="inventory_add"),
    path("<int:inventory_id>/", views.inventory_detail, name="inventory_detail"),
    path("<int:inventory_id>/edit/", views.inventory_edit, name="inventory_edit"),
    path("<int:inventory_id>/delete/", views.inventory_delete, name="inventory_delete"),
    path("<int:inventory_id>/mark-paid/", views.inventory_mark_paid, name="inventory_mark_paid"),
    path("<int:inventory_id>/deposit/", views.add_deposit, name="add_deposit"),
    
    # Worker dashboard now lives at /inventory/dashboard/
    path("dashboard/", views.worker_dashboard, name="worker_dashboard"),
]