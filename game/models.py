from django.db import models

from django.contrib.auth.models import User

class Resource(models.Model):
    gold = models.PositiveIntegerField()
    gold_production = models.PositiveIntegerField()
    rock = models.PositiveIntegerField()
    rock_production = models.PositiveIntegerField()
    wood = models.PositiveIntegerField()
    wood_production = models.PositiveIntegerField()
    last_updated = models.DateTimeField()
    user_id = models.OneToOneField(User, on_delete=models.CASCADE)