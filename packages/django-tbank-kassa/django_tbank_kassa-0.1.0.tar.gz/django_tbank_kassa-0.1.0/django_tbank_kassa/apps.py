from django.apps import AppConfig


class ApiConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'django_tbank_kassa'

    def ready(self) -> None:
        from django.core.checks import Tags, register

        from .checks import settings_variables_check

        register(settings_variables_check, Tags.compatibility)
