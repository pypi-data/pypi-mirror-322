from django.apps import AppConfig
from django.conf import settings
from .validator import validate_env_variables


class DjangoEnvValidatorConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "django_env_validator"

    def ready(self):
        if hasattr(settings, "ENV_VALIDATOR_RULES"):
            validate_env_variables(settings.ENV_VALIDATOR_RULES)
