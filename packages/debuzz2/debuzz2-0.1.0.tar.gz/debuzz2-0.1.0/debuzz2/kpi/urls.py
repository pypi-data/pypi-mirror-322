#Urls

from django.urls import path # Importiert die path-Funktion, um URL-Routen zu definieren
from . import views # Importiert die Views aus der aktuellen Anwendung, um sie mit Routen zu verbinden

urlpatterns = [
    path('', views.home, name='home'),  # Startseite der Anwendung, erreichbar über die Basis-URL
    path('kategorien/', views.kategorisierte_kennzahlen, name='kategorisierte_kennzahlen'), # URL-Pfad, der die Ansicht zur Anzeige kategorisierter Unternehmenskennzahlen aufruft
    path('taschenrechner/', views.taschenrechner, name='taschenrechner'),  # URL-Pfad, der die Ansicht für den Taschenrechner zur Berechnung von Kennzahlen aufruft

]


