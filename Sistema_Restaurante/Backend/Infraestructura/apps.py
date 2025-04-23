from django.apps import AppConfig

class InfraestructuraConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'Backend.Infraestructura'  # Ensure this matches the app's directory structure
    verbose_name = 'Infraestructura'

    def ready(self):
        """
        Importa señales y modelos al iniciar la aplicación
        """
        # Avoid importing models here
