from django.urls import path
from . import views

app_name = 'core'

urlpatterns = [

    path('', views.HomePageView.as_view(), name='home'),    
    
    path('trips', views.TripsView.as_view(), name='trips'),
    path('trips/create', views.TripCreateView.as_view(), name = 'trip_create'),
    path('trips/<pk>/delete', views.TripDeleteView.as_view(), name = 'trip_delete'),
    path('trips/<pk>/edit', views.TripEditView.as_view(), name = 'trip_edit'),
    
    path('trips/<pk>/points/add', views.TripPointAddView.as_view(), name = 'trip_point_add'),
    path('trips/<int:trip_id>/points/<pk>/edit', views.TripPointEditView.as_view(), name = 'trip_point_edit'),
    path('trips/<int:trip_id>/points/<pk>/up', views.trip_point_up, name = 'trip_point_up'),
    path('trips/<int:trip_id>/points/<pk>/down', views.trip_point_down, name = 'trip_point_down'),
    path('trips/<int:trip_id>/points/<pk>/delete', views.trip_point_delete, name = 'trip_point_delete'),

    path('objects', views.ObjectsView.as_view(), name='objects'),
    path('objects/create', views.ObjectCreateView.as_view(), name = 'object_create'),
    path('object/<pk>/delete', views.ObjectDeleteView.as_view(), name = 'object_delete'),
    path('object/<pk>/edit', views.ObjectEditView.as_view(), name = 'object_edit'),
    path('object/<pk>/photo/<int:new_id>', views.object_photo, name = 'object_photo'),
    path('object/<pk>/photo/<int:new_id>/rotate/<int:degree>', views.object_photo_rotate, name = 'object_photo_rotate'),

    path('trips/<int:trip_id>/points/<pk>/objects', views.TripPointObjectsView.as_view(), name = 'trip_point_objects'),
    path('trips/<int:trip_id>/points/<int:point_id>/objects/<int:object_id>/add', views.trip_point_object_add, name = 'trip_point_object_add'),
    path('trips/<int:trip_id>/points/<int:point_id>/objects/<int:object_id>/delete', views.trip_point_object_delete, name = 'trip_point_object_delete'),

    path('persons', views.PersonsView.as_view(), name='persons'),
    path('persons/create', views.PersonCreateView.as_view(), name='person_create'),
    path('persons/<pk>/delete', views.PersonDeleteView.as_view(), name='person_delete'),
    path('persons/<pk>/edit', views.PersonEditView.as_view(), name='person_edit')

]