from django.urls import path
from . import views

app_name = 'core'

urlpatterns = [
    path('', views.HomePageView.as_view(), name='home'),    
    
    path('trips', views.TripsView.as_view(), name='trips'),
    path('trips/create', views.TripCreateView.as_view(), name = 'trip_create'),
    path('trips/<pk>/delete', views.TripDeleteView.as_view(), name = 'trip_delete'),
    path('trips/<pk>/edit', views.TripEditView.as_view(), name = 'trip_edit'),
    
    path('trips/<pk>/add_point/<int:point_id>', views.add_point, name = 'trip_add_point'),
    
    path('points', views.PointsView.as_view(), name='points'),
    path('point/create', views.PointCreateView.as_view(), name = 'point_create'),
    path('point/<pk>/delete', views.PointDeleteView.as_view(), name = 'point_delete'),
    path('point/<pk>/edit', views.PointEditView.as_view(), name = 'point_edit'),

    path('objects', views.ObjectsView.as_view(), name='objects'),
    path('object/create', views.ObjectCreateView.as_view(), name = 'object_create'),
    path('object/<pk>/delete', views.ObjectDeleteView.as_view(), name = 'object_delete'),
    path('object/<pk>/edit', views.ObjectEditView.as_view(), name = 'object_edit'),

    path('photos', views.PhotosView.as_view(), name='photos'),
    path('photo/create', views.PhotoCreateView.as_view(), name = 'photo_create'),
    path('photo/<pk>/delete', views.PhotoDeleteView.as_view(), name = 'photo_delete'),
    path('photo/<pk>/edit', views.PhotoEditView.as_view(), name = 'photo_edit')

]



