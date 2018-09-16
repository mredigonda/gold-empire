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