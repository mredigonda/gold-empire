from django.shortcuts import render

from django.views.generic.base import TemplateView

# Create your views here.
class HomeView(TemplateView):
    template_name = 'game/home.html'

    def get_context_data(self):
        context = {}

        context['gold_units'] = 14
        context['gold_subunits'] = 763
        context['rock_units'] = 26
        context['rock_subunits'] = 144
        context['wood_units'] = 32
        context['wood_subunits'] = 298

        return context
