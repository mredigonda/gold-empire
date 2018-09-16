from django.test import TestCase

from django.contrib.auth.models import User
from .models import Resource
from .models import Building

class HomeViewTests(TestCase):

    def setUp(self):
        user = User.objects.create_user(username='john', password='secret')
        user.save()
        resource = Resource.objects.create(user_id=user)
        resource.save()

    def test_redirect_if_not_authenticated(self):
        response = self.client.get('/')
        self.assertRedirects(response, '/login/')

    def test_resource_view_if_authenticated(self):
        self.client.login(username='john', password='secret')
        response = self.client.get('/')
        self.assertTemplateUsed(response, 'game/home.html')

class BuildingsViewTests(TestCase):

    def setUp(self):
        user = User.objects.create_user(username='john', password='secret')
        user.save()
        resource = Resource.objects.create(user_id=user)
        resource.save()
        building = Building.objects.create(user_id=user)
        building.save()

    def test_redirect_if_not_authenticated(self):
        response = self.client.get('/buildings/')
        self.assertRedirects(response, '/login/')

    def test_upgrade_gold_mine(self):
        self.client.login(username='john', password='secret')
        response = self.client.post('/buildings/', {'gold_mine': True})
        user = User.objects.get(pk=1)
        building = Building.objects.get(user_id=user)
        self.assertEqual(building.gold_mine, 2)

    def test_upgrade_rock_mine(self):
        self.client.login(username='john', password='secret')
        response = self.client.post('/buildings/', {'rock_mine': True})
        user = User.objects.get(pk=1)
        building = Building.objects.get(user_id=user)
        self.assertEqual(building.rock_mine, 2)

    def test_upgrade_lumber_camp(self):
        self.client.login(username='john', password='secret')
        response = self.client.post('/buildings/', {'lumber_camp': True})
        response = self.client.post('/buildings/', {'lumber_camp': True})
        response = self.client.post('/buildings/', {'lumber_camp': True})
        user = User.objects.get(pk=1)
        building = Building.objects.get(user_id=user)
        self.assertEqual(building.lumber_camp, 4)