# urls.py

from django.urls import path
from . import views

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    # path('control_lights/', views.control_lights, name='control_lights'),
    # path('control_thermostats/', views.control_thermostats, name='control_thermostats'),
    # path('control_motion_sensors/', views.control_motion_sensors, name='control_motion_sensors'),
     
    path('lights/', views.manage_lights, name='manage_lights'),
    path('thermostats/', views.manage_thermostats, name='manage_thermostats'),
    path('motion_sensors/', views.manage_motion_sensors, name='manage_motion_sensors'),
    path('scheduling/', views.scheduling_page, name='scheduling'),
    path('add_device/', views.add_device, name='add_device'),
]
