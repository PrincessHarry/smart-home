from django.core.management.base import BaseCommand
from devices.models import SmartLight, MotionSensor

class Command(BaseCommand):
    help = "Manages smart lights based on motion sensor input."

    def handle(self, *args, **kwargs):
        lights = SmartLight.objects.all()
        sensors = MotionSensor.objects.all()

        for sensor in sensors:
            if sensor.is_motion_detected:
                for light in lights:
                    if not light.state:
                        light.turn_on()
                        self.stdout.write(f"Light '{light.name}' turned ON due to motion detected.")

        for light in lights:
            if not any(sensor.is_motion_detected for sensor in sensors):
                if light.state:
                    light.turn_off()
                    self.stdout.write(f"Light '{light.name}' turned OFF due to no motion detected.")
