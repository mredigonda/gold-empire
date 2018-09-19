from django.shortcuts import render, redirect
from django.views.generic.base import TemplateView
from django.views.generic.edit import FormView
from django.contrib.auth.models import User
from django.contrib import messages
from django import forms

from .models import Resource, Building, Unit, Attack, Notification

from random import randint
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
        updated = False
        attack = Attack.objects.get(user_id=user)

        now = datetime.now(timezone.utc)
        delta = now - attack.last_updated
        minutes = delta.total_seconds() // 60

        if minutes >= 5 or attack.enemy_id == attack.user_id:
            attack.enemy_id = attack.generate_random_enemy()
            attack.last_updated = now
            attack.save()
            updated = True

        return (attack, updated)

    def get_context(self, user):
        resource = self.update_resources(user)
        building = Building.objects.get(user_id=user)
        unit = Unit.objects.get(user_id=user)
        attack, _ = self.update_attack(user)
        enemy = User.objects.get(username=attack.enemy_id)
        enemy_resources = self.update_resources(enemy)
        enemy_units = Unit.objects.get(user_id=enemy)

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

        notifications = []
        notification_queryset = Notification.objects.filter(user_id=user) # Get fights fought by this user
        notification_queryset = reversed(notification_queryset)

        for notification in notification_queryset:
            notifications.append({
                'result': 'won' if notification.result else 'lost',
                'enemy': str(notification.enemy_id),
                'type': 'alert-success' if notification.result else 'alert-danger'
            })
            if len(notifications) >= 10:
                break

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

            'enemy_name': enemy.username,

            'enemy_gold': enemy_resources.gold // 1000,
            'enemy_rock': enemy_resources.rock // 1000,
            'enemy_wood': enemy_resources.wood // 1000,

            'enemy_explorer': enemy_units.explorer,
            'enemy_footman': enemy_units.footman,
            'enemy_rifleman': enemy_units.rifleman,
            'enemy_almirant': enemy_units.almirant,
            'enemy_assassin': enemy_units.assassin,
            'enemy_samurai': enemy_units.samurai,

            'explorer': unit.explorer,
            'footman': unit.footman,
            'rifleman': unit.rifleman,
            'almirant': unit.almirant,
            'assassin': unit.assassin,
            'samurai': unit.samurai,

            'notifications': notifications,
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
        messages.error(request, 'You must log in to see your buildings status.', extra_tags='alert-danger')
        return redirect('login')

    def form_valid(self, form):
        if not self.request.user.is_authenticated: # Is this 'if' statement really needed? if so, there should be more like this.
            messages.error(request, 'You must log in to upgrade your buildings.', extra_tags='alert-danger')
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
                messages.error(self.request, "You don't have enough resources to upgrade your gold mine.", extra_tags='alert-danger')
        elif 'rock_mine' in self.request.POST:
            cost = building.get_rock_mine_upgrade_cost()
            cost = (cost[0]*1000, cost[1]*1000)
            if resource.rock >= cost[0] and resource.wood >= cost[1]:
                building.rock_mine += 1
                resource.rock_production += 5
                resource.rock -= cost[0]
                resource.wood -= cost[1]
            else:
                messages.error(self.request, "You don't have enough resources to upgrade your rock mine.", extra_tags='alert-danger')
        elif 'lumber_camp' in self.request.POST:
            cost = building.get_lumber_camp_upgrade_cost()
            cost = (cost[0]*1000, cost[1]*1000)
            if resource.rock >= cost[0] and resource.wood >= cost[1]:
                building.lumber_camp += 1
                resource.wood_production += 7
                resource.rock -= cost[0]
                resource.wood -= cost[1]
            else:
                messages.error(self.request, "You don't have enough resources to upgrade your lumber camp.", extra_tags='alert-danger')
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
        messages.error(request, 'You must log in to see your units status.', extra_tags='alert-danger')
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
                messages.error(self.request, "You don't have enough resources to create an explorer.", extra_tags='alert-danger')
        elif 'footman' in self.request.POST:
            cost = unit.get_footman_cost()
            cost = (cost[0]*1000, cost[1]*1000)
            if resource.gold >= cost[0] and resource.wood >= cost[1]:
                unit.footman += 1
                resource.gold -= cost[0]
                resource.wood -= cost[1]
            else:
                messages.error(self.request, "You don't have enough resources to create a footman.", extra_tags='alert-danger')
        elif 'rifleman' in self.request.POST:
            cost = unit.get_rifleman_cost()
            cost = (cost[0]*1000, cost[1]*1000)
            if resource.gold >= cost[0] and resource.wood >= cost[1]:
                unit.rifleman += 1
                resource.gold -= cost[0]
                resource.wood -= cost[1]
            else:
                messages.error(self.request, "You don't have enough resources to create a rifleman.", extra_tags='alert-danger')
        elif 'almirant' in self.request.POST:
            cost = unit.get_almirant_cost()
            cost = (cost[0]*1000, cost[1]*1000)
            if resource.gold >= cost[0] and resource.wood >= cost[1]:
                unit.almirant += 1
                resource.gold -= cost[0]
                resource.wood -= cost[1]
            else:
                messages.error(self.request, "You don't have enough resources to create an almirant.", extra_tags='alert-danger')
        elif 'assassin' in self.request.POST:
            cost = unit.get_assassin_cost()
            cost = (cost[0]*1000, cost[1]*1000)
            if resource.gold >= cost[0] and resource.wood >= cost[1]:
                unit.assassin += 1
                resource.gold -= cost[0]
                resource.wood -= cost[1]
            else:
                messages.error(self.request, "You don't have enough resources to create an assassin.", extra_tags='alert-danger')
        elif 'samurai' in self.request.POST:
            cost = unit.get_samurai_cost()
            cost = (cost[0]*1000, cost[1]*1000)
            if resource.gold >= cost[0] and resource.wood >= cost[1]:
                unit.samurai += 1
                resource.gold -= cost[0]
                resource.wood -= cost[1]
            else:
                messages.error(self.request, "You don't have enough resources to create a samurai.", extra_tags='alert-danger')
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
        messages.error(request, 'You must log in to see your attacking options.', extra_tags='alert-dangers')
        return redirect('login')

    def get_context_data(self):
        helper = Helper()
        return helper.get_context(self.request.user)

    def form_valid(self, form):
        helper = Helper()
        user = self.request.user
        attack, updated = helper.update_attack(user)
        if updated:
            messages.error(self.request, "The enemy to attack was updated.", extra_tags='alert-danger')
            return redirect('attack')
        resource = helper.update_resources(user)
        unit = Unit.objects.get(user_id=user)
        enemy = User.objects.get(username=attack.enemy_id)
        enemy_resources = helper.update_resources(enemy)
        enemy_units = Unit.objects.get(user_id=enemy)

        combat_points = unit.get_combat_points()
        enemy_combat_points = enemy_units.get_combat_points()
        total_points = combat_points + enemy_combat_points

        if combat_points == 0:
            messages.error(self.request, "You don't have any units in your army!", extra_tags='alert-danger')
            return redirect('attack')

        print(str(combat_points) + " vs " + str(enemy_combat_points))
        print("Chances of winning: " + str(combat_points / total_points))

        result = randint(1, total_points) <= combat_points

        if result:
            delta_gold = int(enemy_resources.gold * 0.1)
            delta_rock = int(enemy_resources.rock * 0.1)
            delta_wood = int(enemy_resources.wood * 0.1)

            delta_explorer = int(enemy_units.explorer * 0.1)
            delta_footman = int(enemy_units.footman * 0.1)
            delta_rifleman = int(enemy_units.rifleman * 0.1)
            delta_almirant = int(enemy_units.almirant * 0.1)
            delta_assassin = int(enemy_units.assassin * 0.1)
            delta_samurai = int(enemy_units.samurai * 0.1)

            enemy_units.explorer -= delta_explorer
            enemy_units.footman -= delta_footman
            enemy_units.rifleman -= delta_rifleman
            enemy_units.almirant -= delta_almirant
            enemy_units.assassin -= delta_assassin
            enemy_units.samurai -= delta_samurai

            enemy_resources.gold -= delta_gold
            enemy_resources.rock -= delta_rock
            enemy_resources.wood -= delta_wood
            
            resource.gold += delta_gold
            resource.rock += delta_rock
            resource.wood += delta_wood

            messages.info(self.request, "You won the match against " + str(enemy) + ", you won 10% of his resources!", extra_tags='alert-success')
        else:
            delta_explorer = int(unit.explorer * 0.1)
            delta_footman = int(unit.footman * 0.1)
            delta_rifleman = int(unit.rifleman * 0.1)
            delta_almirant = int(unit.almirant * 0.1)
            delta_assassin = int(unit.assassin * 0.1)
            delta_samurai = int(unit.samurai * 0.1)

            unit.explorer -= delta_explorer
            unit.footman -= delta_footman
            unit.rifleman -= delta_rifleman
            unit.almirant -= delta_almirant
            unit.assassin -= delta_assassin
            unit.samurai -= delta_samurai

            messages.info(self.request, "You lost the match against " + str(enemy) + ", you lost 10% of your units!", extra_tags='alert-danger')

        resource.save()
        unit.save()
        enemy_resources.save()
        enemy_units.save()

        new_notification = Notification.objects.create(user_id=user, enemy_id=enemy, result=result)
        new_notification.save()

        new_notification = Notification.objects.create(user_id=enemy, enemy_id=user, result=not result)
        new_notification.save()

        return redirect('attack')
