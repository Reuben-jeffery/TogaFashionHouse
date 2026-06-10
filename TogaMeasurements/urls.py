from django.urls import path
from . import views

urlpatterns = [
    # Main list view
    path("", views.measurement_list, name="measurement_list"),
    path("select/", views.measurement_select_gender, name="measurement_select_gender"),

    # Creation paths (with and without client_id)
    path("create/men/", views.measurement_create_men, name="measurement_create_men"),
    path("create/men/<int:client_id>/", views.measurement_create_men, name="add_men_measurement"),
    
    path("create/women/", views.measurement_create_women, name="measurement_create_women"),
    path("create/women/<int:client_id>/", views.measurement_create_women, name="add_women_measurement"),

    # Detail, Edit, Delete
    path("<int:measurement_id>/", views.measurement_detail, name="measurement_detail"),
    path("<int:measurement_id>/edit/", views.measurement_edit, name="measurement_edit"),
    path("<int:measurement_id>/delete/", views.measurement_delete, name="measurement_delete"),
]