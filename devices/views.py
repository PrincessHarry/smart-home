from django.shortcuts import render, redirect
from .models import *
from django.utils import timezone
from django.http import JsonResponse



def add_device(request):
   
    if request.method == "POST":
        device_type = request.POST.get("device_type")
        response = {}

        # Add a Smart Light
        if device_type == "light":
            brightness = request.POST.get("brightness", 100)  # Default to 100 if empty
            if brightness == "":
                brightness = 100  
                
            light = SmartLight.objects.create(
                name=request.POST.get("name"),
                brightness=int(brightness),
                color=request.POST.get("color", "White")
            )
            response = {
                "status": "success",
                "message": f"Smart Light '{light.name}' added successfully!",
                "device": {
                    "name": light.name,
                    "brightness": light.brightness,
                    "color": light.color,
                }
            }

        # Add a Thermostat
        elif device_type == "thermostat":
            current_temp = request.POST.get("current_temperature", 22.0)
            target_temp = request.POST.get("target_temperature", 22.0)
            # Convert the temperatures to float
            current_temp = float(current_temp) if current_temp else 22.0
            target_temp = float(target_temp) if target_temp else 22.0
            
            thermostat = Thermostat.objects.create(
                name=request.POST.get("name"),
                current_temperature=current_temp,
                target_temperature=target_temp
            )
            response = {
                "status": "success",
                "message": f"Thermostat '{thermostat.name}' added successfully!",
                "device": {
                    "name": thermostat.name,
                    "current_temperature": thermostat.current_temperature,
                    "target_temperature": thermostat.target_temperature,
                }
            }

        # Add a Motion Sensor
        elif device_type == "motion_sensor":
            sensor = MotionSensor.objects.create(
                name=request.POST.get("name"),
                is_motion_detected=False
            )
            response = {
                "status": "success",
                "message": f"Motion Sensor '{sensor.name}' added successfully!",
                "device": {
                    "name": sensor.name,
                    "motion_detected": sensor.is_motion_detected,
                }
            }

        return JsonResponse(response)
    if request.headers.get("X-Requested-With") == "XMLHttpRequest":  # AJAX GET request
        # Fetch all devices for the live table
        lights = list(SmartLight.objects.values("name", "brightness", "color"))
        thermostats = list(Thermostat.objects.values("name", "current_temperature", "target_temperature"))
        motion_sensors = list(MotionSensor.objects.values("name", "is_motion_detected"))

        return JsonResponse({
            "lights": lights,
            "thermostats": thermostats,
            "motion_sensors": motion_sensors,
        })


    return render(request, "add_device.html")
    
def dashboard(request):
    # Collect data for dashboard summary
    lights = SmartLight.objects.count()
    thermostats = Thermostat.objects.count()
    motion_sensors = MotionSensor.objects.count()
    
    # Compute additional stats if needed
    # total_lights = lights.count()
    # lights_on = lights.filter(state=True).count()

    # total_thermostats = thermostats.count()
    # if total_thermostats > 0:
    #     min_temp = thermostats.aggregate(min_temp=models.Min('current_temperature'))['min_temp']
    #     max_temp = thermostats.aggregate(max_temp=models.Max('current_temperature'))['max_temp']
    # else:
    #     min_temp, max_temp = None, None

    # total_sensors = motion_sensors.count()
    # active_sensors = motion_sensors.filter(is_motion_detected=True).count()

    context = {
        'lights': lights,
      
        'thermostats': thermostats,
       
        'motion_sensors': motion_sensors,
      
    }

    return render(request, 'dashboard.html', context)
# Manage Lights
def manage_lights(request):
    if request.method == "POST":
        action = request.POST.get("action")

        if action == "turn_all_on":
            SmartLight.objects.update(state=True, color="yellow")  # Default to yellow when turned on
        elif action == "turn_all_off":
            SmartLight.objects.update(state=False, color="black")  # Default to black when turned off
        elif action == "delete_light":
            light_id = request.POST.get("light_id")
            SmartLight.objects.get(id=light_id).delete()
        elif action == "turn_on":
            light = SmartLight.objects.get(id=request.POST.get("light_id"))
            light.turn_on()
            light.change_color("yellow")  # Color set to yellow when turned on
        elif action == "turn_off":
            light = SmartLight.objects.get(id=request.POST.get("light_id"))
            light.turn_off()
            light.change_color("black")  # Color set to black when turned off
        elif action == "adjust_brightness":
            light = SmartLight.objects.get(id=request.POST.get("light_id"))
            light.adjust_brightness(int(request.POST.get("brightness")))
        elif action == "change_color":
            light = SmartLight.objects.get(id=request.POST.get("light_id"))
            new_color = request.POST.get("color")
            light.change_color(new_color)  # Update color based on user's selection

        return redirect("manage_lights")

    lights = SmartLight.objects.all()
    return render(request, "manage_lights.html", {"lights": lights})

# Manage Thermostats
def manage_thermostats(request):
    if request.method == "POST":
        action = request.POST.get("action")

        if action == "set_all_temps":
            bulk_temp = float(request.POST.get("bulk_temp"))
            Thermostat.objects.update(target_temperature=bulk_temp)
        elif action == "delete_thermostat":
            thermostat_id = request.POST.get("thermostat_id")
            Thermostat.objects.get(id=thermostat_id).delete()

        return redirect("manage_thermostats")

    thermostats = Thermostat.objects.all()
    return render(request, "manage_thermostats.html", {"thermostats": thermostats})

# Manage Motion Sensors
def manage_motion_sensors(request):
    if request.method == "POST":
        sensor_id = request.POST.get("sensor_id")
        action = request.POST.get("action")
        sensor = MotionSensor.objects.get(id=sensor_id)

        # Detect or stop motion
        if action == "detect_motion":
            sensor.detect_motion()
            # Turn on all lights when motion is detected
            SmartLight.objects.filter(state=False).update(state=True)
        elif action == "stop_motion":
            sensor.stop_motion()
            # Turn off lights if no motion is detected by any sensor
            if not MotionSensor.objects.filter(is_motion_detected=True).exists():
                SmartLight.objects.filter(state=True).update(state=False)

        # Return JSON response for AJAX
        return JsonResponse({
            "status": "success",
            "sensor_name": sensor.name,
            "is_motion_detected": sensor.is_motion_detected,
        })

    # For a regular GET request, render the template
    motion_sensors = MotionSensor.objects.all()
    return render(request, "manage_motion_sensors.html", {"motion_sensors": motion_sensors})
def scheduling_page(request):
    if request.method == "POST":
        device_name = request.POST.get("device_name")
        action = request.POST.get("action")
        time = request.POST.get("time")
        brightness = request.POST.get("brightness", None)
        color = request.POST.get("color", None)
        temperature = request.POST.get("temperature", None)

        # Save the schedule
        Schedule.objects.create(
            device_name=device_name,
            action=action,
            time=time,
            brightness=brightness,
            color=color,
            temperature=temperature,
        )
        return redirect("scheduling")

    schedules = Schedule.objects.all()
    lights = SmartLight.objects.all()
    thermostats = Thermostat.objects.all()

    return render(request, "scheduling.html", {
        "schedules": schedules,
        "lights": lights,
        "thermostats": thermostats,
    })