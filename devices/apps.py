from django.apps import AppConfig


class DevicesConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "devices"

    def ready(self):
        from .scheduler import start_scheduler
        start_scheduler()

