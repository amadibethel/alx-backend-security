from django.contrib import admin
from django.urls import path, re_path, include
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

# Swagger / OpenAPI schema configuration
schema_view = get_schema_view(
    openapi.Info(
        title="IP Tracking API",
        default_version='v1',
        description="Public API Documentation for IP Tracking and Anomaly Detection",
        terms_of_service="https://www.example.com/terms/",
        contact=openapi.Contact(email="support@example.com"),
        license=openapi.License(name="MIT License"),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
    # Admin route
    path('admin/', admin.site.urls),

    # Swagger UI
    re_path(r'^swagger/$', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    
    # Optional: ReDoc UI
    re_path(r'^redoc/$', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),

    # Your app routes
    path('api/ip_tracking/', include('ip_tracking.urls')),
]
