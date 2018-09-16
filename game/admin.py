from django.contrib import admin
from django.contrib.auth.models import User

from .models import Resource
from .models import Building

admin.site.register(Resource)
admin.site.register(Building)