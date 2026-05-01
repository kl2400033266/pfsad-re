from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, get_object_or_404, redirect
from support.models import HelpRequest
from .models import Message
from django.core.exceptions import PermissionDenied


class CaseChatView(LoginRequiredMixin, View):

    template_name = 'communication/chat.html'

    def get(self, request, pk):
        help_request = get_object_or_404(HelpRequest, pk=pk)

        if not self._has_access(request.user, help_request):
            raise PermissionDenied

        messages = help_request.messages.all().order_by('timestamp')

        return render(request, self.template_name, {
            'help_request': help_request,
            'messages': messages
        })

    def post(self, request, pk):
        help_request = get_object_or_404(HelpRequest, pk=pk)

        if not self._has_access(request.user, help_request):
            raise PermissionDenied

        content = request.POST.get('content')

        receiver = self._get_receiver(request.user, help_request)

        if not receiver or not content:
            raise PermissionDenied

        Message.objects.create(
            help_request=help_request,
            sender=request.user,
            receiver=receiver,
            content=content
        )

        return redirect('case_chat', pk=pk)

    def _has_access(self, user, help_request):
        assignment = getattr(help_request, 'assignment', None)

        if user.role == 'survivor':
            return help_request.survivor == user

        if user.role == 'counsellor':
            return bool(assignment and assignment.counsellor == user)

        if user.role == 'legal_advisor':
            return bool(assignment and assignment.legal_advisor == user)

        return False

    def _get_receiver(self, user, help_request):
        assignment = getattr(help_request, 'assignment', None)

        if user.role == 'survivor':
            if assignment:
                return assignment.counsellor or assignment.legal_advisor
            return None

        return help_request.survivor