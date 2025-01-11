from apscheduler.schedulers.background import BackgroundScheduler
from datetime import datetime


def execute_schedule():
    
    from .models import SmartLight, Thermostat, Schedule
    
    now = datetime.now().time()
    schedules = Schedule.objects.filter(time__lte=now)

    for schedule in schedules:
        if "Light" in schedule.device_name:
            light = SmartLight.objects.get(name=schedule.device_name)
            if schedule.action == "turn_on":
                light.turn_on()
            elif schedule.action == "turn_off":
                light.turn_off()
            elif schedule.action == "adjust_brightness":
                light.adjust_brightness(schedule.brightness)
            elif schedule.action == "change_color":
                light.change_color(schedule.color)
        elif "Thermostat" in schedule.device_name:
            thermostat = Thermostat.objects.get(name=schedule.device_name)
            if schedule.action == "set_temperature":
                thermostat.adjust_temperature(schedule.temperature)

        # Optional: Delete the schedule after execution if it's a one-time action
        schedule.delete()
def execute_automation():
    
    from .models import MotionSensor, SmartLight
     
    sensors = MotionSensor.objects.filter(is_motion_detected=True)
    lights = SmartLight.objects.all()

    for sensor in sensors:
        for light in lights:
            if not light.state:
                light.turn_on()
def start_scheduler():
    scheduler = BackgroundScheduler()
    scheduler.add_job(execute_schedule, "interval", seconds=60)  
    scheduler.add_job(execute_automation, "interval", seconds=30)
    scheduler.start()
