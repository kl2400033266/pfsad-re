from django.urls import path
from .views import dashboard_router, demo_credentials_page, emergency_page, home_page, services_page

urlpatterns = [
    path('', home_page, name='home'),
    path('demo-credentials/', demo_credentials_page, name='demo_credentials'),
    path('services/', services_page, name='services'),
    path('emergency/', emergency_page, name='emergency'),
    path('dashboard/', dashboard_router, name='dashboard'),
]