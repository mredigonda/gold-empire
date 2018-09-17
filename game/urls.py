from django.urls import path

from . import views

urlpatterns = [
    path('', views.HomeView.as_view(), name='home'),
    path('buildings/', views.BuildingsView.as_view(), name='buildings'),
    path('units/', views.UnitsView.as_view(), name='units'),
]