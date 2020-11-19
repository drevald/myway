from django.urls import path
from . import views

app_name = 'core'

urlpatterns = [
    path('trips', views.trips_list, name = 'trips_list'),
    path('trips/create', views.trips_create, name = 'trips_create'),
    path('trips/<int:pk>/delete', views.trips_delete, name = 'trips_delete'),
    path('trips/<int:pk>/details', views.trips_details, name = 'trips_details')
]
