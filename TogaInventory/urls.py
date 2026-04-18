from django.urls import path
from . import views

urlpatterns = [
    path("inventory/", views.inventory_list, name="inventory_list"),
    path("inventory/<int:inventory_id>/", views.inventory_detail, name="inventory_detail"),
    path("inventory/<int:inventory_id>/edit/", views.inventory_edit, name="inventory_edit"),
    path("inventory/<int:inventory_id>/delete/", views.inventory_delete, name="inventory_delete"),
    path("inventory/<int:inventory_id>/mark-paid/", views.inventory_mark_paid, name="inventory_mark_paid"),
    path("worker/dashboard/", views.worker_dashboard, name="worker_dashboard"),
    path("inventory/add/", views.add_inventory, name="add_inventory"),
]
