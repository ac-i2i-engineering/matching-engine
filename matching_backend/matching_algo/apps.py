from django.apps import AppConfig

class MatchingAlgoConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'matching_algo'
    verbose_name = 'Matching Algorithm'

    def ready(self):
        """Import signals and perform any other initialization."""
        pass