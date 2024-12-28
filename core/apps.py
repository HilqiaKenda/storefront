from django.apps import AppConfig


class StoeCustomConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'core'
    
    def ready(self)-> None:
        from .signals import handlers