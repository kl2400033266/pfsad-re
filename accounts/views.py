from django.urls import reverse_lazy
from django.views.generic import CreateView
from django.views.generic import ListView
from django.views.generic import UpdateView, DeleteView
from django.contrib.auth.views import LoginView
from django.contrib.auth import login
from django.db.models import Q
from .forms import (
    SurvivorRegistrationForm,
    EmailOrUsernameAuthenticationForm,
    ProfessionalCreationForm,
    ProfessionalUpdateForm,
)
from .bootstrap import ensure_bootstrap_admin
from .models import CustomUser
from .mixins import AdminRequiredMixin


class SurvivorRegisterView(CreateView):
    form_class = SurvivorRegistrationForm
    template_name = 'accounts/register.html'
    success_url = reverse_lazy('dashboard')

    def form_valid(self, form):
        response = super().form_valid(form)
        login(self.request, self.object)
        return response


class CustomLoginView(LoginView):
    template_name = 'accounts/login.html'
    authentication_form = EmailOrUsernameAuthenticationForm

    def dispatch(self, request, *args, **kwargs):
        ensure_bootstrap_admin()
        return super().dispatch(request, *args, **kwargs)


class ProfessionalCreateView(AdminRequiredMixin, CreateView):
    form_class = ProfessionalCreationForm
    template_name = 'accounts/create_professional.html'
    success_url = reverse_lazy('professional_list')


class ProfessionalListView(AdminRequiredMixin, ListView):
    model = CustomUser
    template_name = 'accounts/professional_list.html'
    context_object_name = 'professionals'
    paginate_by = 10

    def get_queryset(self):
        queryset = CustomUser.objects.filter(
            role__in=['counsellor', 'legal_advisor']
        )

        role = self.request.GET.get('role', '').strip()
        status = self.request.GET.get('status', '').strip()
        query = self.request.GET.get('q', '').strip()

        if role in ['counsellor', 'legal_advisor']:
            queryset = queryset.filter(role=role)

        if status == 'active':
            queryset = queryset.filter(is_active=True)
        elif status == 'inactive':
            queryset = queryset.filter(is_active=False)

        if query:
            queryset = queryset.filter(
                Q(username__icontains=query)
                | Q(email__icontains=query)
                | Q(phone_number__icontains=query)
            )

        return queryset.order_by('role', 'username')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['current_role'] = self.request.GET.get('role', '').strip()
        context['current_status'] = self.request.GET.get('status', '').strip()
        context['current_query'] = self.request.GET.get('q', '').strip()

        query_params = self.request.GET.copy()
        query_params.pop('page', None)
        context['query_params'] = query_params.urlencode()
        return context


class ProfessionalUpdateView(AdminRequiredMixin, UpdateView):
    model = CustomUser
    form_class = ProfessionalUpdateForm
    template_name = 'accounts/edit_professional.html'
    success_url = reverse_lazy('professional_list')

    def get_queryset(self):
        return CustomUser.objects.filter(role__in=['counsellor', 'legal_advisor'])


class ProfessionalDeleteView(AdminRequiredMixin, DeleteView):
    model = CustomUser
    template_name = 'accounts/delete_professional.html'
    success_url = reverse_lazy('professional_list')

    def get_queryset(self):
        return CustomUser.objects.filter(role__in=['counsellor', 'legal_advisor'])