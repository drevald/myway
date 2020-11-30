import base64
import hashlib
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
    fields = ()
    def get_success_url(self):
        trip_point = models.TripPoint.objects.get(id=self.kwargs.get('pk'))
        return reverse_lazy('core:trip_edit', kwargs={'pk':trip_point.trip.id})
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['objects'] = models.ShowObject.objects.all()
        context['trip_point'] = models.TripPoint.objects.get(id=self.kwargs.get('pk'))
        context['trip_point_objects'] = models.TripPointObject.objects.filter(trip_point=context['trip_point'])
        return context

def trip_point_object_add(request, pk, object_id):
    trip_point_object = models.TripPointObject(
    trip_point = models.TripPoint.objects.get(id = pk),
    object = models.ShowObject.objects.get(id = object_id))
    trip_point_object.save()
    return HttpResponseRedirect(reverse('core:trip_point_edit', kwargs={'pk':pk}))

def trip_point_object_delete(request, pk):
    trip_point_object = models.TripPointObject.get(id = pk)
    trip_point = trip_point_object.trip_point
    trip_point_object.delete()
    return HttpResponseRedirect(reverse('core:trip_point_edit', kwargs={'pk':trip_point.id}))    

def object_photo(request, pk, new_id):
    if request.method == 'POST':
        print(request.POST)
        form = forms.UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            if request.POST.get('save') is not None and new_id != 0:
                photo = models.Photo.objects.get(id=new_id)    
                object = models.ShowObject.objects.get(id=pk)
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
    img = img.rotate(angle=degree)
    img.show()
    img.save('thumbnail.jpg', 'JPEG')
    file = open('thumbnail.jpg', "rb")
    image_data = base64.b64encode(file.read()).decode('utf-8') 
    photo.thumbnail = image_data
    photo.save()
    form = forms.UploadFileForm()
    if new_id != 0:
        # photo = models.Photo.objects.get(id=new_id)
        # image_data = photo.thumbnail       
        context = {"image":image_data}
        return render(request, 'object_photo.html', {'form': form,'pk':pk, 'image':image_data,'new_id':photo.id})
    else:
        return render(request, 'object_photo.html', {'form': form,'pk':pk, 'new_id':0})

def md5(fname):
    hash_md5 = hashlib.md5()
    with open(fname, "rb") as f:
        for chunk in iter(lambda: f.read(4096), b""):
            hash_md5.update(chunk)
    return hash_md5.hexdigest()    

def handle_uploaded_file(f):
    stored = '/home/denis/Projects/myway/out'
    with open(stored, 'wb+') as destination:
        for chunk in f.chunks():
            destination.write(chunk)
    hash = md5(stored)
    im = Image.open(stored)        
    size = (360, 240)
    im.thumbnail(size)
    im.save('thumbnail.jpg', 'JPEG')

    image_file = open('thumbnail.jpg', "rb") # opening for [r]eading as [b]inary
    data = base64.b64encode(image_file.read()).decode('utf-8') # if you only wanted to read 512 bytes, do .read(512)
    image_file.close()

    return data

def photo_view(request, pk):
    with open('/home/denis/Projects/myway/out', "rb") as image_file:
        image_data = base64.b64encode(image_file.read()).decode('utf-8')
        ctx = {"image":image_data}
        return render(request, 'index.html', ctx)


