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
    path('persons/<pk>/edit', views.PersonEditView.as_view(), name='person_edit'),

    path('events', views.EventsView.as_view(), name='events'),
    path('events/create', views.EventCreateView.as_view(), name='event_create'),
    path('events/<pk>/delete', views.EventDeleteView.as_view(), name='event_delete'),
    path('events/<pk>/edit', views.EventEditView.as_view(), name='event_edit'),

    path('tags', views.TagsView.as_view(), name='tags'),
    path('tags/create', views.TagCreateView.as_view(), name='tag_create'),
    path('tags/<pk>/delete', views.TagDeleteView.as_view(), name='tag_delete'),
    path('tags/<pk>/edit', views.TagEditView.as_view(), name='tag_edit'),

    path('sites', views.SitesView.as_view(), name='sites'),
    path('sites/create', views.SiteCreateView.as_view(), name='site_create'),
    path('sites/<pk>/delete', views.SiteDeleteView.as_view(), name='site_delete'),
    path('sites/<pk>/edit', views.SiteEditView.as_view(), name='site_edit'),

    path('object/<pk>/events', views.ObjectEventsView.as_view(), name='object_events'),
    path('object/<pk>/event/<int:event_id>/add', views.ObjectEventsAddView.as_view(), name='object_event_add'),
    path('object/<pk>/event/<int:event_id>/delete', views.ObjectEventsDeleteView.as_view(), name='object_event_delete'),

    path('object/<pk>/tags', views.ObjectTagsView.as_view(), name='object_tags'),
    path('object/<pk>/tag/<int:tag_id>/add', views.ObjectTagsAddView.as_view(), name='object_tag_add'),
    path('object/<pk>/tag/<int:tag_id>/delete', views.ObjectTagsDeleteView.as_view(), name='object_tag_delete'),    

    path('object/<pk>/persons', views.ObjectPersonsView.as_view(), name='object_persons'),
    path('object/<pk>/person/<int:person_id>/add', views.ObjectPersonsAddView.as_view(), name='object_person_add'),
    path('object/<pk>/person/<int:person_id>/delete', views.ObjectPersonsDeleteView.as_view(), name='object_person_delete'),    

    path('object/<pk>/sites', views.ObjectSitesView.as_view(), name='object_sites'),
    path('object/<pk>/site/<int:site_id>/add', views.ObjectSitesAddView.as_view(), name='object_site_add'),
    path('object/<pk>/site/<int:site_id>/delete', views.ObjectSitesDeleteView.as_view(), name='object_site_delete')  

]