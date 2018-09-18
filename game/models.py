from random import randint
from django.db import models

from django.contrib.auth.models import User

class Resource(models.Model):
    user_id = models.OneToOneField(User, on_delete=models.CASCADE)
    gold = models.PositiveIntegerField(default=0)
    gold_production = models.PositiveIntegerField(default=1)
    rock = models.PositiveIntegerField(default=0)
    rock_production = models.PositiveIntegerField(default=4)
    wood = models.PositiveIntegerField(default=0)
    wood_production = models.PositiveIntegerField(default=5)
    last_updated = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.user_id) + "'s resources"

class Building(models.Model):
    user_id = models.OneToOneField(User, on_delete=models.CASCADE)
    gold_mine = models.PositiveIntegerField(default=1)
    rock_mine = models.PositiveIntegerField(default=1)
    lumber_camp = models.PositiveIntegerField(default=1)

    def __str__(self):
        return str(self.user_id) + "'s buildings"

    def get_gold_mine_upgrade_cost(self):
        return (self.gold_mine * 7, self.gold_mine * 11)

    def get_rock_mine_upgrade_cost(self):
        return (self.rock_mine * 5, self.rock_mine * 9)

    def get_lumber_camp_upgrade_cost(self):
        return (self.lumber_camp * 4, self.lumber_camp * 8)

class Unit(models.Model):
    user_id = models.OneToOneField(User, on_delete=models.CASCADE)
    explorer = models.PositiveIntegerField(default=0)
    footman = models.PositiveIntegerField(default=0)
    rifleman = models.PositiveIntegerField(default=0)
    almirant = models.PositiveIntegerField(default=0)
    assassin = models.PositiveIntegerField(default=0)
    samurai = models.PositiveIntegerField(default=0)
    
    def __str__(self):
        return str(self.user_id) + "'s units" 

    def get_explorer_cost(self):
        return (1, 4)

    def get_footman_cost(self):
        return (7, 32)

    def get_rifleman_cost(self):
        return (28, 112)

    def get_almirant_cost(self):
        return (74, 301)

    def get_assassin_cost(self):
        return (157, 709)

    def get_samurai_cost(self):
        return (409, 1104)

    def get_explorer_stats(self):
        return (11, 3)

    def get_footman_stats(self):
        return (84, 43)

    def get_rifleman_stats(self):
        return (375, 64)

    def get_almirant_stats(self):
        return (1099, 575)

    def get_assassin_stats(self):
        return (3447, 227)

    def get_samurai_stats(self):
        return (9224, 1311)

    def get_combat_points(self):
        """Combat points define the probability of winning a match"""
        points = 0

        explorer_stats = self.get_explorer_stats()
        footman_stats = self.get_footman_stats()
        rifleman_stats = self.get_rifleman_stats()
        almirant_stats = self.get_almirant_stats()
        assassin_stats = self.get_assassin_stats()
        samurai_stats = self.get_samurai_stats()

        points += self.explorer * (explorer_stats[0] + explorer_stats[1]//2)
        points += self.footman * (footman_stats[0] + footman_stats[1]//2)
        points += self.rifleman * (rifleman_stats[0] + rifleman_stats[1]//2)
        points += self.almirant * (almirant_stats[0] + almirant_stats[1]//2)
        points += self.assassin * (assassin_stats[0] + assassin_stats[1]//2)
        points += self.samurai * (samurai_stats[0] + samurai_stats[1]//2)

        return points

class Attack(models.Model):
    user_id = models.OneToOneField(User, on_delete=models.CASCADE)
    enemy_id = models.ForeignKey(User, on_delete=models.CASCADE, related_name='attack_enemy_id')
    last_updated = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.user_id) + "'s enemies"

    def generate_random_enemy(self): # This assumes that there have been no deletions.
        n = User.objects.all().count()
        if n == 1:
            return self.user_id
        user = User.objects.get(id=int(randint(1, n)))
        while user == self.user_id or user.is_staff: # Search new one while current is self or staff.
            user = User.objects.get(id=int(randint(1, n)))
        return user

class Notification(models.Model):
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    enemy_id = models.ForeignKey(User, on_delete=models.CASCADE, related_name='notification_enemy_id')
    result = models.BooleanField()

    def __str__(self):
        return str(self.user_id) + " vs " + str(self.enemy_id) + ": " + str(self.result)