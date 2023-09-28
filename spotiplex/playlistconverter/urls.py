from django.urls import path
from . import views

urlpatterns = [
    path('playlistconverter/', views.homepage, name='playlistconverter'),
    path('convert/', views.convert, name='convert'),

]