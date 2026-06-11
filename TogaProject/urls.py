from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views
from TogaProject import views as project_views
from . import views
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

urlpatterns = [
    # Admin
    path('admin/', admin.site.urls),

    # Core apps (keep these as they are, assuming they have their own urls.py)
    path('', include('TogaClients.urls')),
    path('', include('TogaInventory.urls')),
    path('measurements/', include('TogaMeasurements.urls')),

    # Authentication
    path('login/', auth_views.LoginView.as_view(template_name='login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='login'), name='logout'),
    path('register/', project_views.register, name='register'),

    # Dashboards (Cleaned up to avoid duplicates)
    # The 'dashboard_router' is now the central point for logins
    path('dashboard-router/', views.dashboard_router, name='dashboard_router'),
    path('dashboard/', project_views.dashboard, name='dashboard'),
    path('admin-dashboard/', project_views.admin_dashboard, name='admin_dashboard'),
    path('worker/dashboard/', views.worker_dashboard, name='worker_dashboard'),

    # Roles & API
    path("roles/", project_views.role_list, name="role_list"),
    path('', auth_views.LoginView.as_view(template_name='login.html'), name='login'),
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('', views.home_view, name='home'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]