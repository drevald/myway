from django.urls import path
from . import views

app_name = 'core'

urlpatterns = [
    path('trips', views.TripsPageView.as_view(), name='trips'),
    path('trips/create', views.TripsCreateView.as_view(), name = 'trips_create'),
]

