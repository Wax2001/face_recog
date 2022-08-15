from django.apps import AppConfig


class FaceprocessingConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'apps.processing'

# runs signals
    def ready(self):
        from apps.processing import signals