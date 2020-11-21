from django.urls import reverse
from django.views.generic import TemplateView
from django.views.generic import ListView
from django.views.generic.edit import CreateView
from . import models

class HomePageView(TemplateView):
    template_name = 'index.html'

class TripsPageView(ListView):
    model = models.Trip
    template_name = 'trips.html'
    context_object_name = 'all_trips_list' # new    

class TripsCreateView(CreateView):
    model = models.Trip
    template_name = 'trip_new.html'
    fields = '__all__'
    url = reverse('core:trips')