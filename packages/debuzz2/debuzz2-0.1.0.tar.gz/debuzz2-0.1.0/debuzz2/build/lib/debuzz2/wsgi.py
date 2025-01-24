"""
WSGI config for debuzz2 project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.1/howto/deployment/wsgi/
"""

import os  # Modul zum Arbeiten mit Betriebssystemfunktionen

from django.core.wsgi import get_wsgi_application  # Funktion zum Abrufen der WSGI-Anwendung

# Setzt die Standardumgebungsvariable für die Django-Einstellungen
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'debuzz2.settings')

# Initialisiert die WSGI-Anwendung, die für den Deployment-Server benötigt wird
application = get_wsgi_application()