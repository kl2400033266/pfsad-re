from django.urls import path
from django.contrib.auth import views as auth_views
from .views import (
    SurvivorRegisterView,
    CustomLoginView,
    ProfessionalCreateView,
    ProfessionalListView,
    ProfessionalUpdateView,
    ProfessionalDeleteView,
)

urlpatterns = [
    path(
        'login/',
        CustomLoginView.as_view(),
        name='login'
    ),

    path(
        'logout/',
        auth_views.LogoutView.as_view(next_page='/login/'),
        name='logout'
    ),

    path(
        'register/',
        SurvivorRegisterView.as_view(),
        name='register'
    ),

    path(
        'manage/professionals/',
        ProfessionalListView.as_view(),
        name='professional_list'
    ),

    path(
        'manage/professionals/create/',
        ProfessionalCreateView.as_view(),
        name='create_professional'
    ),

    path(
        'manage/professionals/<int:pk>/edit/',
        ProfessionalUpdateView.as_view(),
        name='edit_professional'
    ),

    path(
        'manage/professionals/<int:pk>/delete/',
        ProfessionalDeleteView.as_view(),
        name='delete_professional'
    ),
]