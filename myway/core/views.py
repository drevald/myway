from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from . import models
from . import forms

def index(request):
    return HttpResponse('hi')

def trips_list(request):
    trips = models.Trip.objects.all()
    template = loader.get_template('trips.html')
    context = {'trips' : trips}
    return HttpResponse(template.render(context, request))

def trips_create(request):
    trip = models.Trip()
    form = forms.TripForm(request.POST or None, instance=trip)
    if form.is_valid():
        form.save()        
        return HttpResponseRedirect(reverse('core:trips_list'))
    template = 'trip_new.html'
    context = {'form':form}
    return render(request, template, context)

def trips_delete(request, pk):
    return HttpResponse('trip_delete')

def trips_details(request, pk):
    return HttpResponse('trip_details')