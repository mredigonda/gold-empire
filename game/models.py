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