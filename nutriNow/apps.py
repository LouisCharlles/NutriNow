from django.apps import AppConfig
import sys

class NutrinowConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'nutriNow'

    def ready(self):
        # Evita importar os signals durante o comando de migração
        if not any(cmd in sys.argv for cmd in ['makemigrations', 'migrate', 'collectstatic', 'shell']):
            import nutriNow.signals