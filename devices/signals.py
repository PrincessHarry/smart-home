# from django.db.models.signals import post_save
# from django.dispatch import receiver
# from devices.models import MotionSensor, SmartLight

# @receiver(post_save, sender=MotionSensor)
# def handle_motion_sensor_update(sender, instance, **kwargs):
#     lights = SmartLight.objects.all()

#     if instance.is_motion_detected:
#         # Turn on all lights if motion is detected
#         for light in lights:
#             if not light.state:
#                 light.turn_on()
#                 print(f"Light '{light.name}' turned ON due to motion detected.")
#     else:
#         # Turn off all lights if no motion is detected
#         if not any(sensor.is_motion_detected for sensor in MotionSensor.objects.all()):
#             for light in lights:
#                 if light.state:
#                     light.turn_off()
#                     print(f"Light '{light.name}' turned OFF due to no motion detected.")
