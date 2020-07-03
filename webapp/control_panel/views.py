from django.shortcuts import render, redirect
from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin, AccessMixin
from django.contrib.auth.models import User


class ControlPanelView (LoginRequiredMixin, UserPassesTestMixin, AccessMixin, TemplateView):
    template_name = 'control_panel/control_panel.html'
    model = User
    raise_exception = True

    def test_func(self):
        return self.request.user.is_staff
