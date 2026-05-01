from django.core.exceptions import PermissionDenied


class SurvivorRequiredMixin:
    def dispatch(self, request, *args, **kwargs):
        if request.user.role != 'survivor':
            raise PermissionDenied
        return super().dispatch(request, *args, **kwargs)


class AdminRequiredMixin:
    def dispatch(self, request, *args, **kwargs):
        user = request.user
        if not (user.is_superuser or user.is_staff or user.role == 'admin'):
            raise PermissionDenied
        return super().dispatch(request, *args, **kwargs)