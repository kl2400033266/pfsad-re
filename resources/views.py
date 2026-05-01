from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import CreateView, UpdateView, DeleteView, ListView
from django.db.models import Q
from .models import Resource
from .forms import ResourceForm
from accounts.mixins import AdminRequiredMixin


def resource_list_view(request):
	resources = Resource.objects.order_by('resource_type', '-created_at')

	if resources.exists():
		grouped_resources = {
			'legal': resources.filter(resource_type='legal'),
			'counselling': resources.filter(resource_type='counselling'),
			'emergency': resources.filter(resource_type='emergency'),
		}
	else:
		grouped_resources = {
			'legal': [
				{'title': 'Legal Rights Orientation', 'content': 'Understand protective orders, reporting paths, and legal documentation preparation.'},
				{'title': 'Court Procedure Guide', 'content': 'Prepare for hearings with timeline planning and practical checklists.'},
			],
			'counselling': [
				{'title': 'Trauma-Informed Counselling', 'content': 'Access structured emotional support and coping strategy sessions.'},
				{'title': 'Safety Planning Session', 'content': 'Build a personalized safety plan covering immediate and long-term risk reduction.'},
			],
			'emergency': [
				{'title': '24/7 Emergency Hotline', 'content': 'Call local emergency services immediately if there is immediate danger.'},
				{'title': 'Shelter Intake Support', 'content': 'Connect with nearby temporary shelter and relocation coordination support.'},
			],
		}

	return render(request, 'resources/resource_list.html', {'grouped_resources': grouped_resources})


class ResourceAdminListView(AdminRequiredMixin, ListView):
	model = Resource
	template_name = 'resources/resource_admin_list.html'
	context_object_name = 'resources'
	paginate_by = 10

	def get_queryset(self):
		queryset = Resource.objects.all()

		resource_type = self.request.GET.get('type', '').strip()
		query = self.request.GET.get('q', '').strip()

		if resource_type in ['legal', 'counselling', 'emergency']:
			queryset = queryset.filter(resource_type=resource_type)

		if query:
			queryset = queryset.filter(
				Q(title__icontains=query)
				| Q(content__icontains=query)
			)

		return queryset.order_by('resource_type', '-created_at')

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		context['current_type'] = self.request.GET.get('type', '').strip()
		context['current_query'] = self.request.GET.get('q', '').strip()

		query_params = self.request.GET.copy()
		query_params.pop('page', None)
		context['query_params'] = query_params.urlencode()
		return context


class ResourceCreateView(AdminRequiredMixin, CreateView):
	model = Resource
	form_class = ResourceForm
	template_name = 'resources/resource_form.html'
	success_url = reverse_lazy('resource_admin_list')

	def form_valid(self, form):
		form.instance.created_by = self.request.user
		return super().form_valid(form)


class ResourceUpdateView(AdminRequiredMixin, UpdateView):
	model = Resource
	form_class = ResourceForm
	template_name = 'resources/resource_form.html'
	success_url = reverse_lazy('resource_admin_list')


class ResourceDeleteView(AdminRequiredMixin, DeleteView):
	model = Resource
	template_name = 'resources/resource_confirm_delete.html'
	success_url = reverse_lazy('resource_admin_list')
