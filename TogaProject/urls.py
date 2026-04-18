"""
URL configuration for TogaProject project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views
from TogaClients import views as client_views
from TogaProject import views as project_views
from . import views

urlpatterns = [
    path('admin/', admin.site.urls),

    # Core apps
    path('', include('TogaClients.urls')),
    path('', include('TogaInventory.urls')),
    path('measurements/', include('TogaMeasurements.urls')),

    # Authentication
    path('login/', auth_views.LoginView.as_view(template_name='login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='login'), name='logout'),
    path('register/', project_views.register, name='register'),

    # Dashboards
    path('', project_views.dashboard, name='dashboard'),
    path('admin-dashboard/', project_views.admin_dashboard, name='admin_dashboard'),

    # Roles
    path("roles/", project_views.role_list, name="role_list"),
    path("worker/dashboard/", views.worker_dashboard, name="worker_dashboard"),
]

