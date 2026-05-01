from django.urls import reverse_lazy
from django.views.generic import CreateView, ListView
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import HelpRequest
from .forms import HelpRequestForm
from accounts.mixins import SurvivorRequiredMixin, AdminRequiredMixin
from django.shortcuts import get_object_or_404, redirect, render
from .forms import CaseAssignmentForm
from django.views import View
from django.core.exceptions import PermissionDenied


class CreateHelpRequestView(LoginRequiredMixin, SurvivorRequiredMixin, CreateView):
    model = HelpRequest
    form_class = HelpRequestForm
    template_name = 'support/create_request.html'
    success_url = reverse_lazy('dashboard')
    def form_valid(self, form):
        form.instance.survivor = self.request.user
        return super().form_valid(form)

class SurvivorRequestListView(LoginRequiredMixin, SurvivorRequiredMixin, ListView):
    model = HelpRequest
    template_name = 'support/request_list.html'
    context_object_name = 'requests'
    def get_queryset(self):
        return HelpRequest.objects.filter(survivor=self.request.user)
    
class AssignCaseView(LoginRequiredMixin, AdminRequiredMixin, View):
    template_name = 'support/assign_case.html'

    def get(self, request, pk):
        help_request = get_object_or_404(HelpRequest, pk=pk)
        assignment = getattr(help_request, 'assignment', None)
        form = CaseAssignmentForm(instance=assignment)
        return render(request, self.template_name, {'form': form, 'help_request': help_request})

    def post(self, request, pk):
        help_request = get_object_or_404(HelpRequest, pk=pk)
        assignment = getattr(help_request, 'assignment', None)
        form = CaseAssignmentForm(request.POST, instance=assignment)
        if form.is_valid():
            assignment = form.save(commit=False)
            assignment.help_request = help_request
            assignment.assigned_by = request.user
            assignment.save()
            help_request.status = 'assigned'
            help_request.save()
            return redirect('dashboard')
        return render(request, self.template_name, {'form': form, 'help_request': help_request})
    
class AdminRequestListView(LoginRequiredMixin, ListView):
    model = HelpRequest
    template_name = 'support/request_list.html'
    context_object_name = 'requests'
    def get_queryset(self):
        user = self.request.user
        if not (user.role == 'admin' or user.is_superuser or user.is_staff):
            raise PermissionDenied
        return HelpRequest.objects.all()
    
class AssignedCaseListView(LoginRequiredMixin, ListView):
    model = HelpRequest
    template_name = 'support/request_list.html'
    context_object_name = 'requests'

    def get_queryset(self):
        user = self.request.user

        if user.role == 'counsellor':
            return HelpRequest.objects.filter(
                assignment__counsellor=user
            )

        elif user.role == 'legal_advisor':
            return HelpRequest.objects.filter(
                assignment__legal_advisor=user
            )

        else:
            raise PermissionDenied


class CloseAssignedCaseView(LoginRequiredMixin, View):
    def post(self, request, pk):
        user = request.user
        if user.role not in ['counsellor', 'legal_advisor']:
            raise PermissionDenied

        help_request = get_object_or_404(HelpRequest, pk=pk)
        assignment = getattr(help_request, 'assignment', None)
        if not assignment:
            raise PermissionDenied

        can_close = (
            (user.role == 'counsellor' and assignment.counsellor == user)
            or (user.role == 'legal_advisor' and assignment.legal_advisor == user)
        )
        if not can_close:
            raise PermissionDenied

        help_request.status = 'closed'
        help_request.save(update_fields=['status', 'updated_at'])
        return redirect('assigned_cases')