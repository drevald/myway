from django.urls import reverse
from django.urls import reverse_lazy
from django.views.generic import TemplateView
from django.views.generic import ListView
from django.views.generic.edit import CreateView
from django.views.generic.edit import DeleteView
from django.views.generic.edit import UpdateView
from django.http import HttpResponseRedirect
from . import models

class HomePageView(TemplateView):
    template_name = 'index.html'


class TripsView(ListView):
    model = models.Trip
    template_name = 'trips.html'
    context_object_name = 'all_trips_list' # new    

class TripCreateView(CreateView):
    model = models.Trip
    template_name = 'trip_new.html'
    fields = ('name',)
    success_url = reverse_lazy('core:trips')

class TripDeleteView(DeleteView):
    model = models.Trip
    template_name = 'trip_delete.html'
    success_url = reverse_lazy('core:trips')    

class TripEditView(UpdateView):
    model = models.Trip
    template_name = 'trip_edit.html'
    fields = ('name',)
    success_url = reverse_lazy('core:trips')     
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['points'] = models.ShowPoint.objects.all()
        context['trip_points'] = models.TripPoint.objects.all()
        return context

class PointsView(ListView):
    model = models.ShowPoint
    template_name = 'points.html'
    context_object_name = 'points_list'

class PointCreateView(CreateView):
    model = models.ShowPoint
    template_name = 'point_new.html'
    fields = ('name','latitude','longitude')
    success_url = reverse_lazy('core:points')

class PointDeleteView(DeleteView):
    model = models.ShowPoint
    template_name = 'point_delete.html'
    success_url = reverse_lazy('core:points')

class PointEditView(UpdateView):
    model = models.ShowPoint
    template_name = 'point_edit.html'
    fields = ('name','latitude','longitude')
    success_url = reverse_lazy('core:points')

class ObjectsView(ListView):
    model = models.ShowObject
    template_name = 'objects.html'
    context_object_name = 'objects_list'

class ObjectCreateView(CreateView):
    model = models.ShowObject
    template_name = 'object_new.html'
    fields = ('name','latitude','longitude')
    success_url = reverse_lazy('core:objects')

class ObjectDeleteView(DeleteView):
    model = models.ShowObject
    template_name = 'object_delete.html'
    success_url = reverse_lazy('core:objects')

class ObjectEditView(UpdateView):
    model = models.ShowObject
    template_name = 'object_edit.html'
    fields = ('name','latitude','longitude')
    success_url = reverse_lazy('core:objects')

class PhotosView(ListView):
    model = models.Photo
    template_name = 'photos.html'
    context_object_name = 'photos_list'

class PhotoCreateView(CreateView):
    model = models.Photo
    template_name = 'photo_new.html'
    fields = '__all__'
    success_url = reverse_lazy('core:photos')

class PhotoDeleteView(DeleteView):
    model = models.Photo
    template_name = 'photo_delete.html'
    success_url = reverse_lazy('core:photos')

class PhotoEditView(UpdateView):
    model = models.Photo
    template_name = 'photo_edit.html'
    fields = '__all__'
    success_url = reverse_lazy('core:photos')

def trip_point_add(request, pk, point_id):
    trip_points = models.TripPoint.objects.filter(trip = models.Trip.objects.get(id = pk))
    trip_point = models.TripPoint(
        trip = models.Trip.objects.get(id = pk),
        point = models.ShowPoint.objects.get(id = point_id),
        order = len(list(trip_points)))
    trip_point.save()
    return HttpResponseRedirect(reverse('core:trip_edit', kwargs={'pk':pk}))

def trip_point_delete(request, pk, point_id):
    trip_points = models.TripPoint.objects.filter(trip = models.Trip.objects.get(id = pk))
    trip_point_del = models.TripPoint.objects.get(
        trip = models.Trip.objects.get(id = pk),
        point = models.ShowPoint.objects.get(id = point_id))
    for trip_point in trip_points:
        if trip_point.order > trip_point_del.order:
            trip_point.order = trip_point.order - 1
            trip_point.save()
    trip_point_del.delete()
    return HttpResponseRedirect(reverse('core:trip_edit', kwargs={'pk':pk}))    

def trip_point_up(request, pk, point_id):
    trip_points = models.TripPoint.objects.filter(trip = models.Trip.objects.get(id = pk))
    trip_point_mov = models.TripPoint.objects.get(
        trip = models.Trip.objects.get(id = pk),
        point = models.ShowPoint.objects.get(id = point_id))
    for trip_point in trip_points:
        if trip_point.order == trip_point_mov.order + 1:
            trip_point.order = trip_point.order - 1
            trip_point_mov.order = trip_point_mov.order + 1
            trip_point.save()
            trip_point_mov.save()
            break
    return HttpResponseRedirect(reverse('core:trip_edit', kwargs={'pk':pk}))       

def trip_point_down(request, pk, point_id):
    trip_points = models.TripPoint.objects.filter(trip = models.Trip.objects.get(id = pk))
    trip_point_mov = models.TripPoint.objects.get(
        trip = models.Trip.objects.get(id = pk),
        point = models.ShowPoint.objects.get(id = point_id))
    for trip_point in trip_points:
        if trip_point.order == trip_point_mov.order - 1:
            trip_point.order = trip_point.order + 1
            trip_point_mov.order = trip_point_mov.order - 1
            trip_point.save()
            trip_point_mov.save()
            break
    return HttpResponseRedirect(reverse('core:trip_edit', kwargs={'pk':pk}))      

class TripPointEditView(UpdateView):
    model = models.TripPoint
    template_name = 'trip_point_edit.html'
    fields = '__all__'
    def get_success_url(self):
        trip_point = models.TripPoint.objects.get(id=self.kwargs.get('pk'))
        return reverse_lazy('core:trip_edit', kwargs={'pk':trip_point.trip.id})
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['objects'] = models.ShowObject.objects.all()
        return context