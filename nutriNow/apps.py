from django.apps import AppConfig
import sys

class NutrinowConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'nutriNow'

    def ready(self):
        # Evita importar os signals durante o comando de migração
        if 'runserver' in sys.argv or 'gunicorn' in sys.argv:
            import nutriNow.signals