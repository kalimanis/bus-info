from django.urls import path
from . import views

urlpatterns = [
    path('', views.live_bus_info, name='live_bus_info'),
]