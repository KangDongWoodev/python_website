import os
import subprocess
from django.core.management.base import BaseCommand

class Command(BaseCommand):
    help = "Run Daphne server with Django ASGI application"

    def handle(self, *args, **options):
        os.environ.setdefault("DJANGO_SETTINGS_MODULE", "group_project.settings")
        
        # subprocess로 daphne 명령 실행
        subprocess.run([
            "daphne",
            "-p", "8000",
            "group_project.asgi:application"
        ], env=os.environ.copy())
