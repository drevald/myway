import debug_toolbar
from django.conf import settings
from django.urls import path
from django.urls import include

urlpatterns = [
    path('', include('myway.core.urls')),
    path('__debug__/', include(debug_toolbar.urls)),
] 

