from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator


# Smart Light Model
class SmartLight(models.Model):
    name = models.CharField(max_length=100)
    state = models.BooleanField(default=False)  # True = ON, False = OFF
    brightness = models.IntegerField(
        default=100,
        validators=[
            MinValueValidator(0),  # Minimum brightness is 0
            MaxValueValidator(100),  # Maximum brightness is 100
        ]
    )
    color = models.CharField(max_length=20, default='White')  # Light color

    def turn_on(self):
        self.state = True
        self.save()

    def turn_off(self):
        self.state = False
        self.save()

    def adjust_brightness(self, level):
        if 0 <= level <= 100:
            self.brightness = level
            self.save()

    def change_color(self, color):
        self.color = color
        self.save()

    def __str__(self):
        return self.name


# Thermostat Model
class Thermostat(models.Model):
    name = models.CharField(max_length=100)
    current_temperature = models.FloatField(default=22.0)  # Current room temperature
    target_temperature = models.FloatField(default=22.0)  # Desired temperature

    def adjust_temperature(self, new_temp):
        self.target_temperature = new_temp
        self.save()

    def __str__(self):
        return f"{self.name} (Current: {self.current_temperature}°C, Target: {self.target_temperature}°C)"


# Motion Sensor Model
class MotionSensor(models.Model):
    name = models.CharField(max_length=100)
    is_motion_detected = models.BooleanField(default=False)  # True if motion detected

    def detect_motion(self):
        self.is_motion_detected = True
        self.save()

    def stop_motion(self):
        self.is_motion_detected = False
        self.save()

    def __str__(self):
        return self.name
class Schedule(models.Model):
    ACTION_CHOICES = [
        ("turn_on", "Turn On"),
        ("turn_off", "Turn Off"),
        ("adjust_brightness", "Adjust Brightness"),
        ("change_color", "Change Color"),
        ("set_temperature", "Set Temperature"),
    ]

    device_name = models.CharField(max_length=100)
    action = models.CharField(max_length=20, choices=ACTION_CHOICES)
    time = models.TimeField()
    brightness = models.IntegerField(null=True, blank=True)  # For lights
    color = models.CharField(max_length=20, null=True, blank=True)  # For lights
    temperature = models.FloatField(null=True, blank=True)  # For thermostats

    def __str__(self):
        return f"{self.device_name} - {self.action} at {self.time}"
    