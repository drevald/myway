from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader
from . import models

def index(request):
    return HttpResponse('hi')

def trips_list(request):
    trips = models.Trip.objects
    template = loader.get_template('trips.html')
    context = {'trips' : trips}
    return HttpResponse(template.render(context, request))

def trips_create(request):
    return HttpResponse('trip_create')

def trips_delete(request):
    return HttpResponse('trip_delete')

def trips_details(request):
    return HttpResponse('trip_details')