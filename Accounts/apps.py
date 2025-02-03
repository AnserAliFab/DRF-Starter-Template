from django.apps import AppConfig


class AccountsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'Accounts'

    def ready(self):
        # Import signals
        from . import signals
        from .scheduler import start_scheduler