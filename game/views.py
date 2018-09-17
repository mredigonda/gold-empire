from django.shortcuts import render, redirect
from django.views.generic.base import TemplateView
from django.views.generic.edit import FormView
from django.contrib.auth.models import User
from django.contrib import messages
from django import forms

from .models import Resource, Building, Unit, Attack

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

    def update_attack(self, user):
        attack = Attack.objects.get(user_id=user)

        now = datetime.now(timezone.utc)
        delta = now - attack.last_updated
        minutes = delta.total_seconds() // 60

        if minutes >= 5 or attack.enemy_id == attack.user_id:
            attack.enemy_id = attack.generate_random_enemy()
            attack.last_updated = now
            attack.save()

        return attack

    def get_context(self, user):
        resource = self.update_resources(user)
        building = Building.objects.get(user_id=user)
        unit = Unit.objects.get(user_id=user)
        attack = self.update_attack(user)

        upgrade_gold_mine = building.get_gold_mine_upgrade_cost()
        upgrade_rock_mine = building.get_rock_mine_upgrade_cost()
        upgrade_lumber_camp = building.get_lumber_camp_upgrade_cost()

        explorer_cost = unit.get_explorer_cost()
        footman_cost = unit.get_footman_cost()
        rifleman_cost = unit.get_rifleman_cost()
        almirant_cost = unit.get_almirant_cost()
        assassin_cost = unit.get_assassin_cost()
        samurai_cost = unit.get_samurai_cost()

        explorer_stats = unit.get_explorer_stats()
        footman_stats = unit.get_footman_stats()
        rifleman_stats = unit.get_rifleman_stats()
        almirant_stats = unit.get_almirant_stats()
        assassin_stats = unit.get_assassin_stats()
        samurai_stats = unit.get_samurai_stats()

        context = {
            'username': user.username,

            'gold_units': resource.gold // 1000,
            'gold_subunits': resource.gold % 1000,
            'rock_units': resource.rock // 1000,
            'rock_subunits': resource.rock % 1000,
            'wood_units': resource.wood // 1000,
            'wood_subunits': resource.wood % 1000,

            'upgrade_gold_mine_rock_cost': upgrade_gold_mine[0],
            'upgrade_gold_mine_wood_cost': upgrade_gold_mine[1],
            'upgrade_rock_mine_rock_cost': upgrade_rock_mine[0],
            'upgrade_rock_mine_wood_cost': upgrade_rock_mine[1],
            'upgrade_lumber_camp_rock_cost': upgrade_lumber_camp[0],
            'upgrade_lumber_camp_wood_cost': upgrade_lumber_camp[1],

            'gold_mine_level': building.gold_mine,
            'rock_mine_level': building.rock_mine,
            'lumber_camp_level': building.lumber_camp,

            'gold_mine_disabled': resource.rock < upgrade_gold_mine[0]*1000 or resource.wood < upgrade_gold_mine[1]*1000,
            'rock_mine_disabled': resource.rock < upgrade_rock_mine[0]*1000 or resource.wood < upgrade_rock_mine[1]*1000,
            'lumber_camp_disabled': resource.rock < upgrade_lumber_camp[0]*1000 or resource.wood < upgrade_lumber_camp[1]*1000,

            'explorer_gold_cost': explorer_cost[0],
            'explorer_wood_cost': explorer_cost[1],
            'footman_gold_cost': footman_cost[0],
            'footman_wood_cost': footman_cost[1],
            'rifleman_gold_cost': rifleman_cost[0],
            'rifleman_wood_cost': rifleman_cost[1],
            'almirant_gold_cost': almirant_cost[0],
            'almirant_wood_cost': almirant_cost[1],
            'assassin_gold_cost': assassin_cost[0],
            'assassin_wood_cost': assassin_cost[1],
            'samurai_gold_cost': samurai_cost[0],
            'samurai_wood_cost': samurai_cost[1],
            
            'explorer_attack': explorer_stats[0],
            'explorer_defense': explorer_stats[1],
            'footman_attack': footman_stats[0],
            'footman_defense': footman_stats[1],
            'rifleman_attack': rifleman_stats[0],
            'rifleman_defense': rifleman_stats[1],
            'almirant_attack': almirant_stats[0],
            'almirant_defense': almirant_stats[1],
            'assassin_attack': assassin_stats[0],
            'assassin_defense': assassin_stats[1],
            'samurai_attack': samurai_stats[0],
            'samurai_defense': samurai_stats[1],

            'explorer_disabled': resource.gold < explorer_cost[0]*1000 or resource.wood < explorer_cost[1]*1000,
            'footman_disabled': resource.gold < footman_cost[0]*1000 or resource.wood < footman_cost[1]*1000,
            'rifleman_disabled': resource.gold < rifleman_cost[0]*1000 or resource.wood < rifleman_cost[1]*1000,
            'almirant_disabled': resource.gold < almirant_cost[0]*1000 or resource.wood < almirant_cost[1]*1000,
            'assassin_disabled': resource.gold < assassin_cost[0]*1000 or resource.wood < assassin_cost[1]*1000,
            'samurai_disabled': resource.gold < samurai_cost[0]*1000 or resource.wood < samurai_cost[1]*1000,

            'enemy_name': 'izak',

            'enemy_gold': 327,
            'enemy_rock': 213,
            'enemy_wood': 915,

            'enemy_explorer': 37,
            'enemy_footman': 12,
            'enemy_rifleman': 3,
            'enemy_almirant': 1,
            'enemy_assassin': 0,
            'enemy_samurai': 0,
        }

        return context

class HomeView(TemplateView):
    template_name = 'game/home.html'

    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return super().get(self, request, *args, **kwargs)
        return redirect('login')

    def get_context_data(self):
        helper = Helper()
        return helper.get_context(self.request.user)

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
        if not self.request.user.is_authenticated: # Is this 'if' statement really needed? if so, there should be more like this.
            messages.error(self.request, 'You must log in to upgrade your buildings.')
            return redirect('login')
        helper = Helper()
        resource = helper.update_resources(self.request.user)
        building = Building.objects.get(user_id=self.request.user)
        if 'gold_mine' in self.request.POST:
            cost = building.get_gold_mine_upgrade_cost()
            cost = (cost[0]*1000, cost[1]*1000)
            if resource.rock >= cost[0] and resource.wood >= cost[1]:
                building.gold_mine += 1
                resource.gold_production += 3
                resource.rock -= cost[0]
                resource.wood -= cost[1]
            else:
                messages.error(self.request, "You don't have enough resources to upgrade your gold mine.")
        elif 'rock_mine' in self.request.POST:
            cost = building.get_rock_mine_upgrade_cost()
            cost = (cost[0]*1000, cost[1]*1000)
            if resource.rock >= cost[0] and resource.wood >= cost[1]:
                building.rock_mine += 1
                resource.rock_production += 5
                resource.rock -= cost[0]
                resource.wood -= cost[1]
            else:
                messages.error(self.request, "You don't have enough resources to upgrade your rock mine.")
        elif 'lumber_camp' in self.request.POST:
            cost = building.get_lumber_camp_upgrade_cost()
            cost = (cost[0]*1000, cost[1]*1000)
            if resource.rock >= cost[0] and resource.wood >= cost[1]:
                building.lumber_camp += 1
                resource.wood_production += 7
                resource.rock -= cost[0]
                resource.wood -= cost[1]
            else:
                messages.error(self.request, "You don't have enough resources to upgrade your lumber camp.")
        resource.save()
        building.save()
        return redirect('buildings')

    def get_context_data(self):
        helper = Helper()
        return helper.get_context(self.request.user)

class UnitsView(FormView):
    template_name = 'game/units.html'
    form_class = forms.Form
    success_url = 'units/'

    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return super().get(self, request, *args, **kwargs)
        messages.error(request, 'You must log in to see your units status.')
        return redirect('login')

    def form_valid(self, form):
        helper = Helper()
        resource = helper.update_resources(self.request.user)
        unit = Unit.objects.get(user_id=self.request.user)
        if 'explorer' in self.request.POST:
            cost = unit.get_explorer_cost()
            cost = (cost[0]*1000, cost[1]*1000)
            if resource.gold >= cost[0] and resource.wood >= cost[1]:
                unit.explorer += 1
                resource.gold -= cost[0]
                resource.wood -= cost[1]
            else:
                messages.error(self.request, "You don't have enough resources to create an explorer.")
        elif 'footman' in self.request.POST:
            cost = unit.get_footman_cost()
            cost = (cost[0]*1000, cost[1]*1000)
            if resource.gold >= cost[0] and resource.wood >= cost[1]:
                unit.footman += 1
                resource.gold -= cost[0]
                resource.wood -= cost[1]
            else:
                messages.error(self.request, "You don't have enough resources to create a footman.")
        elif 'rifleman' in self.request.POST:
            cost = unit.get_rifleman_cost()
            cost = (cost[0]*1000, cost[1]*1000)
            if resource.gold >= cost[0] and resource.wood >= cost[1]:
                unit.rifleman += 1
                resource.gold -= cost[0]
                resource.wood -= cost[1]
            else:
                messages.error(self.request, "You don't have enough resources to create a rifleman.")
        elif 'almirant' in self.request.POST:
            cost = unit.get_almirant_cost()
            cost = (cost[0]*1000, cost[1]*1000)
            if resource.gold >= cost[0] and resource.wood >= cost[1]:
                unit.almirant += 1
                resource.gold -= cost[0]
                resource.wood -= cost[1]
            else:
                messages.error(self.request, "You don't have enough resources to create an almirant.")
        elif 'assassin' in self.request.POST:
            cost = unit.get_assassin_cost()
            cost = (cost[0]*1000, cost[1]*1000)
            if resource.gold >= cost[0] and resource.wood >= cost[1]:
                unit.assassin += 1
                resource.gold -= cost[0]
                resource.wood -= cost[1]
            else:
                messages.error(self.request, "You don't have enough resources to create an assassin.")
        elif 'samurai' in self.request.POST:
            cost = unit.get_samurai_cost()
            cost = (cost[0]*1000, cost[1]*1000)
            if resource.gold >= cost[0] and resource.wood >= cost[1]:
                unit.samurai += 1
                resource.gold -= cost[0]
                resource.wood -= cost[1]
            else:
                messages.error(self.request, "You don't have enough resources to create a samurai.")
        resource.save()
        unit.save()
        return redirect('units')

    def get_context_data(self):
        helper = Helper()
        return helper.get_context(self.request.user)

class AttackView(FormView):
    template_name = 'game/attack.html'
    form_class = forms.Form
    success_url = 'attack/'

    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return super().get(self, request, *args, **kwargs)
        messages.error(request, 'You must log in to see your attacking options.')
        return redirect('login')

    def get_context_data(self):
        helper = Helper()
        return helper.get_context(self.request.user)