from django.urls import path
from .views import (
    resource_list_view,
    ResourceAdminListView,
    ResourceCreateView,
    ResourceUpdateView,
    ResourceDeleteView,
)

urlpatterns = [
    path('resources/', resource_list_view, name='resource_list'),
    path('manage/resources/', ResourceAdminListView.as_view(), name='resource_admin_list'),
    path('manage/resources/create/', ResourceCreateView.as_view(), name='resource_create'),
    path('manage/resources/<int:pk>/edit/', ResourceUpdateView.as_view(), name='resource_edit'),
    path('manage/resources/<int:pk>/delete/', ResourceDeleteView.as_view(), name='resource_delete'),
]
