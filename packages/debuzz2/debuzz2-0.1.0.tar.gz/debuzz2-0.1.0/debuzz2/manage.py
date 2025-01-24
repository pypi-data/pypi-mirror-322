#!/usr/bin/env python
"""Django's command-line utility for administrative tasks."""

# Importiert die notwendigen Module
import os  # Modul zum Arbeiten mit Betriebssystemfunktionen wie Umgebungsvariablen
import sys  # Modul zum Arbeiten mit System-spezifischen Parametern und Funktionen

# Hauptfunktion des Skripts
def main():
    """
    Führt administrative Aufgaben für Django aus.
    """
    # Setzt die Umgebungsvariable für die Django-Einstellungen, falls nicht bereits gesetzt
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'debuzz2.settings')

    try:
        # Importiert die Funktion zum Ausführen von Befehlen aus der Kommandozeile
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        # Behandelt den Fehler, wenn Django nicht importiert werden kann
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc  # Gibt den ursprünglichen Fehler weiter

    # Führt den Befehl aus, der von der Kommandozeile übergeben wurde
    execute_from_command_line(sys.argv)

# Startpunkt des Skripts
if __name__ == '__main__':
    main()  # Ruft die Hauptfunktion auf
