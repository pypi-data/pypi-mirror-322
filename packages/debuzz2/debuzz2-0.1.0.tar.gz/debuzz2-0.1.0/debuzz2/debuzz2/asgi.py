"""
ASGI config for debuzz2 project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.1/howto/deployment/asgi/
"""

import os  # Modul zum Arbeiten mit Betriebssystemfunktionen

from django.core.asgi import get_asgi_application  # Funktion zum Abrufen der ASGI-Anwendung

# Setzt die Standardumgebungsvariable für die Django-Einstellungen
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'debuzz2.settings')

# Initialisiert die ASGI-Anwendung, die für asynchrone Server benötigt wird
application = get_asgi_application()