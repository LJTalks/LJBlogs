# For userProfile user_profile app when it exists
# ensure that a UserProfile is automatically created 
# whenever a new user registers

from django.apps import AppConfig


class LjtalksConfig(AppConfig):
    name = 'ljtalks'

    def ready(self):
        import ljtalks.signals  # Import signals to make them active
