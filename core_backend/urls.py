"""
URL configuration for core_backend project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
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
from django.http import JsonResponse
from django.urls import path
from django.urls import include
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from dashboard.views import dashboard_home


def api_root(request):
    """
    JSON listing of API endpoints at /api/.
    """

    return JsonResponse(
        {
            "name": "Health Monitoring & Telemedicine Platform API",
            "endpoints": {
                "auth": {
                    "token": "/api/auth/token/",
                    "refresh": "/api/auth/token/refresh/",
                },
                "accounts": "/api/accounts/",
                "patients": "/api/patients/",
                "consultations": "/api/consultations/",
                "analytics": "/api/analytics/",
                "dashboard": "/api/dashboard/overview/",
            },
        }
    )

urlpatterns = [
    path("", dashboard_home, name="dashboard-home"),
    path("dashboard/", include("dashboard.urls")),
    path("api/", api_root, name="api-root"),
    path("admin/", admin.site.urls),
    # Django built-in auth views (login/logout/password reset) at /accounts/
    path("accounts/", include("django.contrib.auth.urls")),
    # Auth & accounts
    path("api/auth/token/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("api/auth/token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    path("api/accounts/", include("accounts.urls")),
    path("api/patients/", include("patients.urls")),
    path("api/consultations/", include("consultations.urls")),
    path("api/analytics/", include("analytics.urls")),
    path("api/dashboard/", include("dashboard.urls")),
]
