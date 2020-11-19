from django.urls import path
import myway.views as views

urlpatterns = [
    path('', views.index),
    path('trips/', views.trips_list),
    path('trips/create', views.trips_create),
    path('trips/<int:pk>/delete', views.trips_delete),
    path('trips/<int:pk>/details', views.trips_details)
]