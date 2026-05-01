from django.urls import path
from .views import AdminRequestListView, AssignedCaseListView, CreateHelpRequestView, SurvivorRequestListView
from .views import AssignCaseView
from .views import CloseAssignedCaseView

urlpatterns = [
    path('request/create/', CreateHelpRequestView.as_view(), name='create_request'),
    path('request/my/', SurvivorRequestListView.as_view(), name='my_requests'),
    path('request/<int:pk>/assign/', AssignCaseView.as_view(), name='assign_case'),
    path('request/<int:pk>/close/', CloseAssignedCaseView.as_view(), name='close_case'),
    path('manage/requests/', AdminRequestListView.as_view(), name='admin_requests'),
    path('assigned/', AssignedCaseListView.as_view(), name='assigned_cases'),
]