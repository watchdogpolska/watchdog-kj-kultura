from django.apps import AppConfig


class UsersConfig(AppConfig):
    name = 'watchdog_kj_kultura.users'
    verbose_name = "Users"

    def ready(self):
        """Override this to put in:
            Users system checks
            Users signal registration
        """
        pass
