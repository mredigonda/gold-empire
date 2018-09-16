from django.shortcuts import render, redirect
from django.views.generic.base import TemplateView
from django.views.generic.edit import FormView
from django.contrib.auth.models import User
from django.contrib import messages
from django import forms

from .models import Resource
from .models import Building

from datetime import datetime, timezone

class Helper():

    def update_resources(self, user):
        resource = Resource.objects.get(user_id=user)

        now = datetime.now(timezone.utc)
        delta = now - resource.last_updated
        seconds = delta.total_seconds()

        resource.gold += int(resource.gold_production * seconds)
        resource.rock += int(resource.rock_production * seconds)
        resource.wood += int(resource.wood_production * seconds)
        resource.last_updated = now
        resource.save()

        return resource

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
        helper = Helper()
        resource = helper.update_resources(self.request.user)

        context = {}

        context['gold_units'] = resource.gold // 1000
        context['gold_subunits'] = resource.gold % 1000
        context['rock_units'] = resource.rock // 1000
        context['rock_subunits'] = resource.rock % 1000
        context['wood_units'] = resource.wood // 1000
        context['wood_subunits'] = resource.wood % 1000
        context['username'] = self.request.user.username

        return context

class BuildingsView(FormView): # Maybe FormView is not the most appropriate, but it must be something with support for post
    template_name = 'game/buildings.html'
    form_class = forms.Form
    success_url = 'buildings/'

    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return super().get(self, request, *args, **kwargs)
        messages.error(request, 'You must log in to see your buildings status.')
        return redirect('login')

    def form_valid(self, form):
        if not self.request.user.is_authenticated:
            messages.error(self.request, 'You must log in to upgrade your buildings.')
            return redirect('login')
        helper = Helper()
        resource = helper.update_resources(self.request.user)
        building = Building.objects.get(user_id=self.request.user)
        if 'gold_mine' in self.request.POST:
            building.gold_mine += 1
            resource.gold_production += 3
        elif 'rock_mine' in self.request.POST:
            building.rock_mine += 1
            resource.rock_production += 5
        elif 'lumber_camp' in self.request.POST:
            building.lumber_camp += 1
            resource.wood_production += 7
        resource.save()
        building.save()
        return redirect('buildings')
