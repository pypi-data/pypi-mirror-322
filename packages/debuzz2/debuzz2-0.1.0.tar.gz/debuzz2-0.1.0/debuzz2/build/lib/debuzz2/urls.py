"""
URL configuration for debuzz2 project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views  # Importiert Funktionen aus einer App
    2. Add a URL to urlpatterns:  path('', views.home, name='home')  # Verknüpft eine URL mit einer Funktions-View
Class-based views
    1. Add an import:  from other_app.views import Home  # Importiert eine Klassen-basierte View
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')  # Verknüpft eine URL mit einer Klassen-basierten View
Including another URLconf
    1. Import the include() function: from django.urls import include, path  # Ermöglicht das Einfügen von weiteren URL-Konfigurationen
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))  # Verlinkt eine andere URL-Konfigurationsdatei
"""

# Importiert erforderliche Module
from django.contrib import admin  # Admin-Modul für Django
from django.urls import path, include  # Funktionen zum Verwalten von URLs und Einfügen von weiteren URL-Konfigurationen

# URL-Muster der Anwendung
urlpatterns = [
    path('admin/', admin.site.urls),  # URL für die Admin-Oberfläche von Django
    path('kpi/', include('kpi.urls')),  # URL, die die kpi-App mit ihren eigenen Routen einbindet
]

