import os

from django.apps import AppConfig


class MatchesConfig(AppConfig):
    name = 'apps.matches'

    def ready(self):
        if os.environ.get('SCHEDULER_ENABLED') == '1':
            from apps.matches.scheduler import start
            start()
