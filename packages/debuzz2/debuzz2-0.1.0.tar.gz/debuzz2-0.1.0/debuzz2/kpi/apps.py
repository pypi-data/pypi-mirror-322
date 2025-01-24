# Importierte Module
from django.apps import AppConfig  # Modul zur Konfiguration von Django-Apps


# Konfigurationsklasse für die App "kpi"
class KpiConfig(AppConfig):
    # Standard-Feldtyp für automatisch generierte Primärschlüssel
    default_auto_field = 'django.db.models.BigAutoField'

    # Name der App, wie sie in den Django-Einstellungen referenziert wird
    name = 'kpi'
