import base64
import hashlib
import io
from io import BytesIO
from PIL import Image, ImageFilter
from django.urls import reverse
from django.urls import reverse_lazy
from django.shortcuts import render
from django.views.generic import TemplateView
from django.views.generic import ListView
from django.views.generic.edit import CreateView
from django.views.generic.edit import DeleteView
from django.views.generic.edit import UpdateView
from django.views.generic.edit import ModelFormMixin
from django.views.generic.detail import DetailView
from django.http import HttpResponseRedirect
from . import models
from . import forms

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
    form_class = forms.ObjectForm
    success_url = reverse_lazy('core:objects')
    def get(self, request, *args, **kwargs):
        if 'latitude' not in request.session or request.session['latitude'] == '':
            request.session["latitude"] = "55.7558171758732"
            request.session["longitude"] = "37.61771159788882"
        return super().get(request, *args, **kwargs)
    def post(self, request, *args, **kwargs):
        request.session["latitude"] = request.POST['latitude']
        request.session["longitude"] = request.POST['longitude']
        return super().post(request, *args, **kwargs)

class ObjectDeleteView(DeleteView):
    model = models.ShowObject
    template_name = 'object_delete.html'
    success_url = reverse_lazy('core:objects')

class ObjectEditView(UpdateView):
    model = models.ShowObject
    template_name = 'object_edit.html'
    form_class = forms.ObjectForm    
    success_url = reverse_lazy('core:objects')
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        object = models.ShowObject.objects.get(id=self.kwargs.get('pk'))
        if object.photo is not None:
            context['image'] = object.photo.thumbnail
        return context

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

def trip_point_delete(request, trip_id, pk):
    trip_points = models.TripPoint.objects.filter(trip = models.Trip.objects.get(id = trip_id))
    trip_point_del = models.TripPoint.objects.get(id = pk)
    for trip_point in trip_points:
        if trip_point.order > trip_point_del.order:
            trip_point.order = trip_point.order - 1
            trip_point.save()
    trip_point_del.delete()
    return HttpResponseRedirect(reverse('core:trip_edit', kwargs={'pk':trip_id}))    

def trip_point_up(request, trip_id, pk):
    trip_points = models.TripPoint.objects.filter(trip = models.Trip.objects.get(id = trip_id))
    trip_point_mov = models.TripPoint.objects.get(id = pk)
    for trip_point in trip_points:
        if trip_point.order == trip_point_mov.order + 1:
            trip_point.order = trip_point.order - 1
            trip_point_mov.order = trip_point_mov.order + 1
            trip_point.save()
            trip_point_mov.save()
            break
    return HttpResponseRedirect(reverse('core:trip_edit', kwargs={'pk':trip_id}))       

def trip_point_down(request, trip_id, pk):
    trip_points = models.TripPoint.objects.filter(trip = models.Trip.objects.get(id = trip_id))
    trip_point_mov = models.TripPoint.objects.get(id = pk)
    for trip_point in trip_points:
        if trip_point.order == trip_point_mov.order - 1:
            trip_point.order = trip_point.order + 1
            trip_point_mov.order = trip_point_mov.order - 1
            trip_point.save()
            trip_point_mov.save()
            break
    return HttpResponseRedirect(reverse('core:trip_edit', kwargs={'pk':trip_id}))      

class TripPointAddView(CreateView):
    model = models.TripPoint
    template_name = 'trip_point_new.html'
    form_class = forms.TripPointForm
    success_url = reverse_lazy('core:trip_edit')
    def form_valid(self, form):
        trip = models.Trip.objects.get(id = self.kwargs.get('pk'))
        self.object = form.save(commit = False)        
        self.object.trip = trip
        self.object.order = 1 + len(trip.points.all())
        return super().form_valid(form)
    def get_success_url(self):
        params = {"pk": self.kwargs["pk"]}
        return reverse_lazy("core:trip_edit", kwargs=params)
    def get(self, request, *args, **kwargs):
        if 'latitude' not in request.session:
            request.session["latitude"] = "55.7558171758732"
            request.session["longitude"] = "37.61771159788882"
        return super().get(request, *args, **kwargs)
    def post(self, request, *args, **kwargs):
        request.session["latitude"] = request.POST['latitude']
        request.session["longitude"] = request.POST['longitude']
        return super().post(request, *args, **kwargs)

class TripPointEditView(UpdateView):
    model = models.TripPoint
    template_name = 'trip_point_edit.html'
    form_class = forms.TripPointForm
    success_url = reverse_lazy('core:trip_edit')
    def form_valid(self, form):
        point = models.TripPoint.objects.get(id = self.kwargs.get('pk'))
        self.object = form.save(commit = False)        
        self.object.trip = point.trip
        # self.object.order = 1
        return super().form_valid(form)
    def get_success_url(self):
        point = models.TripPoint.objects.get(id = self.kwargs.get('pk'))
        params = {"pk": point.trip.id}
        return reverse_lazy("core:trip_edit", kwargs=params)

class TripPointObjectsView(DetailView):
    model = models.TripPoint
    template_name = 'trip_point_objects.html'
    form_class = forms.TripPointForm    
    def get_success_url(self):
        return reverse_lazy('core:trip_edit', kwargs={'pk':trip_id})
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        params = [kwargs['object'].latitude, kwargs['object'].latitude, kwargs['object'].longitude, kwargs['object'].longitude]
        context['objects_near'] = models.ShowObject.objects.raw(
            'SELECT * FROM core_showobject WHERE ((latitude - %s)*(latitude - %s) + (longitude - %s)*(longitude-%s)) < 0.0001', params)
        return context

def trip_point_object_add(request, trip_id, point_id, object_id):
    trip_point_object = models.TripPointObject(
        trip_point = models.TripPoint.objects.get(id = point_id),
        object = models.ShowObject.objects.get(id = object_id))
    trip_point_object.save()
    return HttpResponseRedirect(reverse('core:trip_point_objects', kwargs={'trip_id':trip_id, 'pk':point_id}))

def trip_point_object_delete(request, trip_id, point_id, object_id):
    trip_point_object = models.TripPointObject.objects.filter(
        trip_point = models.TripPoint.objects.get(id = point_id),
        object = models.ShowObject.objects.get(id = object_id),
    ).first()
    trip_point_object.delete()
    return HttpResponseRedirect(reverse('core:trip_point_objects', kwargs={'trip_id':trip_id, 'pk':point_id}))    

def object_photo(request, pk, new_id):
    if request.method == 'POST':
        form = forms.UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            if request.POST.get('save') is not None and new_id != 0:
                photo = models.Photo.objects.get(id=new_id)    
                object = models.ShowObject.objects.get(id=pk)
                if object.photo is not None and object.photo.id != photo.id:
                    object.photo.delete() 
                object.photo = photo
                object.save()
                return HttpResponseRedirect(reverse('core:object_edit', kwargs={'pk':pk}))
            elif request.POST.get('save') is not None or request.POST.get('cancel') is not None:
                return HttpResponseRedirect(reverse('core:object_edit', kwargs={'pk':pk}))
            else:
                data = handle_uploaded_file(request.FILES['file'])
                photo = models.Photo(md5 = hash, thumbnail=data)
                photo.save()
                return HttpResponseRedirect(reverse('core:object_photo', kwargs={'pk':pk,'new_id':photo.id}))
        else:
            print(form._errors)
    else:
        form = forms.UploadFileForm()
        show_object = models.ShowObject.objects.get(id=pk)
        if new_id != 0:
            photo = models.Photo.objects.get(id=new_id)
            image_data = photo.thumbnail       
            context = {"image":image_data}
            return render(request, 'object_photo.html', {'form': form,'pk':pk, 'image':image_data,'new_id':photo.id})
        elif show_object.photo is not None:
            photo = show_object.photo
            image_data = photo.thumbnail       
            context = {"image":image_data}
            return render(request, 'object_photo.html', {'form': form,'pk':pk, 'image':image_data,'new_id':photo.id})
        else:
            return render(request, 'object_photo.html', {'form': form,'pk':pk, 'new_id':0})

def object_photo_rotate(request, pk, new_id, degree):   
    photo = models.Photo.objects.get(id=new_id)    
    retrieved_data = photo.thumbnail
    print(retrieved_data[0:10])
    image_arr = base64.b64decode(retrieved_data)
    in_memory_file = BytesIO(image_arr)
    img = Image.open(in_memory_file)
    img = img.rotate(angle=degree, expand=1)
    memstr = io.BytesIO()
    img.save(memstr, 'JPEG')
    memstr.seek(0)
    image_data = base64.b64encode(memstr.read()).decode('utf-8') 
    photo.thumbnail = image_data
    photo.save()
    form = forms.UploadFileForm()
    if new_id != 0:
        context = {"image":image_data}
        return HttpResponseRedirect(reverse('core:object_photo', kwargs={'pk':pk,'new_id':photo.id}))
    else:
        return HttpResponseRedirect(reverse('core:object_photo', kwargs={'pk':pk,'new_id':photo.id}))

def md5(fname):
    hash_md5 = hashlib.md5()
    for chunk in iter(lambda: fname.read(4096), b""):
        hash_md5.update(chunk)
    hash_md5.update(chunk)
    return hash_md5.hexdigest()    

def handle_uploaded_file(f):
    hash = md5(f)
    im = Image.open(f)        
    size = (360, 240)
    im.thumbnail(size)
    memstr = io.BytesIO()
    im.save(memstr, 'JPEG')
    memstr.seek(0)
    data = base64.b64encode(memstr.read()).decode('utf-8') 
    return data

class PersonsView(ListView):
    model = models.Person
    template_name = 'persons.html'

class PersonCreateView(CreateView):
    model = models.Person
    template_name = 'person_edit.html'
    fields = '__all__'
    success_url = reverse_lazy('core:persons')    

class PersonDeleteView(DeleteView):
    model = models.Person
    template_name = 'person_delete.html'
    success_url = reverse_lazy('core:persons')    

class PersonEditView(UpdateView):
    model = models.Person
    template_name = 'person_edit.html'
    form_class = forms.PersonForm
    # fields = '__all__'
    success_url = reverse_lazy('core:persons')    

class SitesView(ListView):
    model = models.Site
    template_name = 'sites.html'

class SiteCreateView(CreateView):
    model = models.Site
    template_name = 'site_edit.html'
    fields = '__all__'
    success_url = reverse_lazy('core:sites')    

class SiteDeleteView(DeleteView):
    model = models.Site
    template_name = 'site_delete.html'
    success_url = reverse_lazy('core:sites')    

class SiteEditView(UpdateView):
    model = models.Site
    template_name = 'site_edit.html'
    fields = '__all__'
    success_url = reverse_lazy('core:sites')   

class EventsView(ListView):
    model = models.Event
    template_name = 'events.html'

class EventCreateView(CreateView):
    model = models.Event
    template_name = 'event_edit.html'
    fields = '__all__'
    success_url = reverse_lazy('core:events')    

class EventDeleteView(DeleteView):
    model = models.Event
    template_name = 'event_delete.html'
    success_url = reverse_lazy('core:events')    

class EventEditView(UpdateView):
    model = models.Event
    template_name = 'event_edit.html'
    fields = '__all__'
    success_url = reverse_lazy('core:events')  

class TagsView(ListView):
    model = models.Tag
    template_name = 'tags.html'

class TagCreateView(CreateView):
    model = models.Tag
    template_name = 'tag_edit.html'
    fields = '__all__'
    success_url = reverse_lazy('core:tags')    

class TagDeleteView(DeleteView):
    model = models.Tag
    template_name = 'tag_delete.html'
    success_url = reverse_lazy('core:tags')    

class TagEditView(UpdateView):
    model = models.Tag
    template_name = 'tag_edit.html'
    fields = '__all__'
    success_url = reverse_lazy('core:tags')      

class ObjectEventsView(DetailView):
    model = models.ShowObject
    template_name = 'object_events.html'    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['all_events'] = models.Event.objects.all()
        return context    

class ObjectEventsAddView(ObjectEventsView):
    def get(self, request, *args, **kwargs):
        object = models.ShowObject.objects.get(id = kwargs['pk'])
        event = models.Event.objects.get(id = kwargs['event_id'])
        object.events.add(event)
        object.save()
        return super().get(self, request, *args, **kwargs)

class ObjectEventsDeleteView(ObjectEventsView):
    def get(self, request, *args, **kwargs):
        object = models.ShowObject.objects.get(id = kwargs['pk'])
        event = models.Event.objects.get(id = kwargs['event_id'])
        object.events.remove(event)
        object.save()
        return super().get(self, request, *args, **kwargs)

class ObjectTagsView(DetailView):
    model = models.ShowObject
    template_name = 'object_tags.html'    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['all_tags'] = models.Tag.objects.all()
        return context    

class ObjectTagsAddView(ObjectTagsView):
    def get(self, request, *args, **kwargs):
        object = models.ShowObject.objects.get(id = kwargs['pk'])
        tag = models.Tag.objects.get(id = kwargs['tag_id'])
        object.tags.add(tag)
        object.save()
        return super().get(self, request, *args, **kwargs)

class ObjectTagsDeleteView(ObjectTagsView):
    def get(self, request, *args, **kwargs):
        object = models.ShowObject.objects.get(id = kwargs['pk'])
        tag = models.Tag.objects.get(id = kwargs['tag_id'])
        object.tags.remove(tag)
        object.save()
        return super().get(self, request, *args, **kwargs)        

class ObjectPersonsView(DetailView):
    model = models.ShowObject
    template_name = 'object_persons.html'    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['all_persons'] = models.Person.objects.all()
        return context    

class ObjectPersonsAddView(ObjectPersonsView):
    def get(self, request, *args, **kwargs):
        object = models.ShowObject.objects.get(id = kwargs['pk'])
        person = models.Person.objects.get(id = kwargs['person_id'])
        object.persons.add(person)
        object.save()
        return super().get(self, request, *args, **kwargs)

class ObjectPersonsDeleteView(ObjectPersonsView):
    def get(self, request, *args, **kwargs):
        object = models.ShowObject.objects.get(id = kwargs['pk'])
        person = models.Person.objects.get(id = kwargs['person_id'])
        object.persons.remove(person)
        object.save()
        return super().get(self, request, *args, **kwargs)

class ObjectSitesView(DetailView):
    model = models.ShowObject
    template_name = 'object_sites.html'    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['all_sites'] = models.Site.objects.all()
        return context    

class ObjectSitesAddView(ObjectSitesView):
    def get(self, request, *args, **kwargs):
        object = models.ShowObject.objects.get(id = kwargs['pk'])
        site = models.Site.objects.get(id = kwargs['site_id'])
        object.sites.add(site)
        object.save()
        return super().get(self, request, *args, **kwargs)

class ObjectSitesDeleteView(ObjectSitesView):
    def get(self, request, *args, **kwargs):
        object = models.ShowObject.objects.get(id = kwargs['pk'])
        site = models.Site.objects.get(id = kwargs['site_id'])
        object.sites.remove(site)
        object.save()
        return super().get(self, request, *args, **kwargs)        