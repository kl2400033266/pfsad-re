from django.contrib import admin
from django.urls import path, include
from django.http import JsonResponse
from django.db import connection

def health_check(request):
    try:
        with connection.cursor() as cursor:
            cursor.execute('SELECT 1')
            cursor.fetchone()
        db_status = 'ok'
    except Exception:
        db_status = 'error'

    payload = {
        'status': 'ok' if db_status == 'ok' else 'degraded',
        'database': db_status,
    }

    status_code = 200 if db_status == 'ok' else 503
    return JsonResponse(payload, status=status_code)


urlpatterns = [
    path('', include('core.urls')),
    path('health/', health_check, name='health_check'),
    path('', include('accounts.urls')),
    path('', include('support.urls')),
    path('', include('communication.urls')),
    path('', include('resources.urls')),
    path('admin/', admin.site.urls),
]