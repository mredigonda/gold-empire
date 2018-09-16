from django.shortcuts import render, redirect
from django.views.generic.edit import FormView
from django.views.generic.base import RedirectView
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User

from game.models import Resource

class SignUpView(FormView):
    template_name = 'accounts/signup.html'
    form_class = UserCreationForm
    success_url = '/'

    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('home')
        return super().get(request, *args, **kwargs)

    def form_valid(self, form):
        username = form.cleaned_data['username']
        password = form.cleaned_data['password1']
        form.save() # Isn't this called implicitly by "super().form_valid(form)" below?
        user = authenticate(username=username, password=password) 
        login(self.request, user)

        # Create new resource associated with this user
        new_resource = Resource.objects.create(user_id=user)
        new_resource.save()
        
        return super().form_valid(form)

class LoginView(FormView):
    template_name = 'accounts/login.html'
    form_class = AuthenticationForm
    success_url = '/'

    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('home')
        return super().get(request, *args, **kwargs)

    def form_valid(self, form):
        username = form.cleaned_data['username']
        password = form.cleaned_data['password']
        user = authenticate(username=username, password=password) 
        login(self.request, user)
        return redirect('home')

class LogoutView(RedirectView):
    url = '/'

    def get(self, request, *args, **kwargs):
        logout(request)
        return super().get(request, *args, **kwargs)