from django.shortcuts import render, redirect
from django.views.generic.base import TemplateView
from django.contrib.auth.models import User

from .models import Resource

from datetime import datetime, timezone

# Create your views here.
class HomeView(TemplateView):
    template_name = 'game/home.html'

    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return super().get(self, request, *args, **kwargs)
        return redirect('login')

    def get_context_data(self):
        """
        First updates the resource model, and then sets those
        resource values to the context.
        """
        user = User.objects.get(pk=1)
        resource = Resource.objects.get(user_id=user)

        # Update resources
        now = datetime.now(timezone.utc)
        delta = now - resource.last_updated
        seconds = delta.total_seconds()

        resource.gold += int(resource.gold_production * seconds)
        resource.rock += int(resource.rock_production * seconds)
        resource.wood += int(resource.wood_production * seconds)
        resource.last_updated = now
        resource.save()

        context = {}

        context['gold_units'] = resource.gold // 1000
        context['gold_subunits'] = resource.gold % 1000
        context['rock_units'] = resource.rock // 1000
        context['rock_subunits'] = resource.rock % 1000
        context['wood_units'] = resource.wood // 1000
        context['wood_subunits'] = resource.wood % 1000
        context['username'] = self.request.user.username

        return context