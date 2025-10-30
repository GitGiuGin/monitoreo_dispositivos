from django.apps import AppConfig


class RegionalConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'apps.regional'

    def ready(self):
        import apps.regional.signals