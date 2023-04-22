
from django.contrib import admin
from django.urls import path, include
from . import views

from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [

    # Testing URL
    path('upload', views.uploadAudio, name="upload"),   
    path('upload1', views.uploadAudio1, name="upload1"),  

    path('summary', views.sendSummary, name="summary"),   

    # Index Page 
    path('', views.index, name="index"),    
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
