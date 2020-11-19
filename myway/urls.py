from django.urls import path
import myway.views as views

app_name = 'myway'

urlpatterns = [
    path('', views.index),
    path('trips/', views.trips_list, name = 'trips'),
    path('trips/create', views.trips_create, name = 'create'),
    path('trips/<int:pk>/delete', views.trips_delete, name = 'delete'),
    path('trips/<int:pk>/details', views.trips_details, name = 'details')
]