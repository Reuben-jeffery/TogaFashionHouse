from django.urls import path
from . import views

urlpatterns = [
    path("measurements/", views.measurement_list, name="measurement_list"),
    path("measurements/select/", views.measurement_select_gender, name="measurement_select_gender"),

    #Add client_id and match template names
    path("measurements/create/men/", views.measurement_create_men, name="measurement_create_men"),
    path("measurements/create/women/", views.measurement_create_women, name="measurement_create_women"),

    path("measurements/<int:measurement_id>/edit/", views.measurement_edit, name="measurement_edit"),
    path("measurements/<int:measurement_id>/", views.measurement_detail, name="measurement_detail"),
    path("measurements/<int:measurement_id>/delete/", views.measurement_delete, name="measurement_delete"),
]
from django.urls import path
from . import views

urlpatterns = [
    path("measurements/", views.measurement_list, name="measurement_list"),
    path("measurements/select/", views.measurement_select_gender, name="measurement_select_gender"),

    # Support both naming conventions
    path("measurements/create/men/<int:client_id>/", views.measurement_create_men, name="add_men_measurement"),
    path("measurements/create/men/", views.measurement_create_men, name="measurement_create_men"),

    path("measurements/create/women/<int:client_id>/", views.measurement_create_women, name="add_women_measurement"),
    path("measurements/create/women/", views.measurement_create_women, name="measurement_create_women"),

    path("measurements/<int:measurement_id>/edit/", views.measurement_edit, name="measurement_edit"),
    path("measurements/<int:measurement_id>/", views.measurement_detail, name="measurement_detail"),
    path("measurements/<int:measurement_id>/delete/", views.measurement_delete, name="measurement_delete"),
]
