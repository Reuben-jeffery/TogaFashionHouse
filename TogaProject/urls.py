from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views
from TogaProject import views as project_views
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

urlpatterns = [
    path('admin/', admin.site.urls),

    # --- Authentication ---
    path('login/', auth_views.LoginView.as_view(template_name='login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='login'), name='logout'),
    path('register/', project_views.register, name='register'),

    # --- Entry Point ---
    path('', project_views.home_view, name='home'),
    
    # --- Router ---
    path('dashboard-router/', project_views.dashboard_router, name='dashboard_router'),
    
    # --- Main Dashboard ---
    path('dashboard/', project_views.dashboard, name='dashboard'),
    path('admin-dashboard/', project_views.admin_dashboard, name='admin_dashboard'),

    # --- Core App Inclusions (Delegates routing to apps) ---
    path('clients/', include('TogaClients.urls')),
    path('inventory/', include('TogaInventory.urls')),
    path('measurements/', include('TogaMeasurements.urls')),
    path("roles/", project_views.role_list, name="role_list"),

    # --- API ---
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]