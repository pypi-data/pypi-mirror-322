from django.core.management.base import BaseCommand
from django.conf import settings
import subprocess
from django.core.management import call_command
import polib
import json
import os
import requests
from django_transfiles.utils import generate_translations

class Command(BaseCommand):
    help = "Muestra las configuraciones de i18n definidas en settings.py."

    def handle(self, *args, **kwargs):
        # Obtener las configuraciones de i18n
        languages = settings.LANGUAGES
        default_language = settings.LANGUAGE_CODE

        locale_dir = settings.LOCALE_PATHS[0]

        self.stdout.write(f"Idioma predeterminado: {default_language}")

        generate_translations(self,'es', locale_dir)

        for code, name in languages:
            if code != default_language:
                generate_translations(self,code, locale_dir)

            
        call_command('compilemessages')