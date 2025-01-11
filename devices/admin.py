from django.contrib import admin
from .models import SmartLight, Thermostat, MotionSensor

@admin.register(SmartLight)
class SmartLightAdmin(admin.ModelAdmin):
    list_display = ('name', 'state', 'brightness', 'color')
    list_filter = ('state', 'color')

@admin.register(Thermostat)
class ThermostatAdmin(admin.ModelAdmin):
    list_display = ('name', 'current_temperature', 'target_temperature')
    list_filter = ('current_temperature',)

@admin.register(MotionSensor)
class MotionSensorAdmin(admin.ModelAdmin):
    list_display = ('name', 'is_motion_detected')
    list_filter = ('is_motion_detected',)
