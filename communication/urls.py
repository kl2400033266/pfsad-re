from django.urls import path
from .views import CaseChatView

urlpatterns = [
    path('chat/<int:pk>/', CaseChatView.as_view(), name='case_chat'),
]