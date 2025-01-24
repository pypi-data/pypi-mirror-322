# Importierte Module
import json  # Modul zum Arbeiten mit JSON-Daten
from django.shortcuts import render, get_object_or_404  # Funktionen zum Rendern von Templates und Abrufen von Objekten
from .models import Unternehmenskennzahl, Rentabilitaetskennzahl, Liquiditaetskennzahl, Investitionskennzahl  # Importiert Modelle für Unternehmenskennzahlen

# Funktion zum Rendern der Startseite
def home(request):

    #Zeigt die Startseite von debuzz2 an.

    return render(request, 'kpi/home.html', {
        'title': 'Willkommen bei debuzz2',  # Titel der Seite
        'description': 'Erkunde verschiedene Unternehmenskennzahlen und ihre Bedeutung für den Geschäftserfolg.'  # Beschreibung der Seite
    })

# Funktion zum Laden und Anzeigen kategorisierter Kennzahlen
def kategorisierte_kennzahlen(request):
    # Öffnet die JSON-Datei mit Unternehmenskennzahlen
    with open('data.json', 'r', encoding='utf-8') as file:
        raw_data = json.load(file)  # Lädt die JSON-Daten in ein Python-Objekt

    kategorisierte_kennzahlen = {}  # Initialisiert ein leeres Dictionary für kategorisierte Kennzahlen
    for kategorie, kennzahlen in raw_data.items():  # Iteriert durch die Kategorien und ihre jeweiligen Kennzahlen
        kategorisierte_kennzahlen[kategorie] = []  # Initialisiert eine leere Liste für jede Kategorie
        for k in kennzahlen:  # Iteriert durch jede Kennzahl in der Kategorie
            if kategorie == "Rentabilität":
                # Erstellt eine Rentabilitätskennzahl
                kennzahl = Rentabilitaetskennzahl(
                    kuerzel=k.get('kürzel') or k.get('Kürzel'),  # Kürzel der Kennzahl
                    name=k.get('name', 'Unbekannt'),  # Name der Kennzahl
                    definition=k.get('definition', 'Keine Definition vorhanden'),  # Definition der Kennzahl
                    berechnungsformel=k.get('berechnungsformel'),  # Berechnungsformel der Kennzahl
                    return_on=k.get('return_on')  # Zusätzlicher Wert für Rentabilität
                )
            elif kategorie == "Liquidität":
                # Erstellt eine Liquiditätskennzahl
                kennzahl = Liquiditaetskennzahl(
                    kuerzel=k.get('kürzel') or k.get('Kürzel'),
                    name=k.get('name', 'Unbekannt'),
                    definition=k.get('definition', 'Keine Definition vorhanden'),
                    berechnungsformel=k.get('berechnungsformel'),
                    cashflow=k.get('cashflow')  # Cashflow-Wert
                )
            elif kategorie == "Investition":
                # Erstellt eine Investitionskennzahl
                kennzahl = Investitionskennzahl(
                    kuerzel=k.get('kürzel') or k.get('Kürzel'),
                    name=k.get('name', 'Unbekannt'),
                    definition=k.get('definition', 'Keine Definition vorhanden'),
                    berechnungsformel=k.get('berechnungsformel'),
                    abzinsungssatz=k.get('abzinsungssatz')  # Abzinsungssatz
                )
            else:
                # Erstellt eine allgemeine Unternehmenskennzahl
                kennzahl = Unternehmenskennzahl(
                    kuerzel=k.get('kürzel') or k.get('Kürzel'),
                    name=k.get('name', 'Unbekannt'),
                    definition=k.get('definition', 'Keine Definition vorhanden'),
                    berechnungsformel=k.get('berechnungsformel'),
                    kategorie=kategorie  # Kategoriezugehörigkeit
                )
            kategorisierte_kennzahlen[kategorie].append(kennzahl)  # Fügt die Kennzahl zur Kategorie hinzu

    return render(request, 'kpi/kategorisierte_kennzahlen.html', {
        'kennzahlen_kategorisiert': kategorisierte_kennzahlen  # Übergibt die kategorisierten Kennzahlen an das Template
    })

# Funktion für den Taschenrechner
def taschenrechner(request):
    # Eingabewerte und Operation aus der Anfrage abrufen
    wert1 = request.GET.get('wert1', '')  # Erster Eingabewert
    wert2 = request.GET.get('wert2', '')  # Zweiter Eingabewert
    wert3 = request.GET.get('wert3', '')  # Dritter Eingabewert (optional)
    operation = request.GET.get('operation', '')  # Angeforderte Operation
    ergebnis = None  # Initialisiert das Ergebnis

    # Standard-Labels
    labels = {
        "wert1": "Wert 1",  # Standardbezeichnung für den ersten Wert
        "wert2": "Wert 2",  # Standardbezeichnung für den zweiten Wert
        "wert3": "Wert 3"   # Standardbezeichnung für den dritten Wert
    }

    # Labels für spezifische Operationen zuweisen
    if operation == 'ROI':
        labels["wert1"] = "Gewinn"
        labels["wert2"] = "Kapital"
    elif operation == 'EBIT':
        labels["wert1"] = "Jahresüberschuss"
        labels["wert2"] = "Steueraufwand"
        labels["wert3"] = "Zinsaufwand"
    elif operation == 'LCR':
        labels["wert1"] = "Liquide Mittel"
        labels["wert2"] = "Kurzfristige Verbindlichkeiten"
    elif operation == 'Break-Even Point':
        labels["wert1"] = "Fixkosten"
        labels["wert2"] = "Preis"
        labels["wert3"] = "Variable Kosten pro Einheit"
    elif operation == 'EPS':
        labels["wert1"] = "Gewinn"
        labels["wert2"] = "Aktienanzahl"
    elif operation == 'EKQ':
        labels["wert1"] = "Eigenkapital"
        labels["wert2"] = "Gesamtkapital"
    elif operation == 'ROE':
        labels["wert1"] = "Gewinn"
        labels["wert2"] = "Eigenkapital"
    elif operation == 'EVA':
        labels["wert1"] = "NOPAT"
        labels["wert2"] = "(Kapital x Kapitalkostensatz)"
    elif operation == 'OCF':
        labels["wert1"] = "EBIT"
        labels["wert2"] = "Abschreibungen"
        labels["wert3"] = "Steuern"
    elif operation == 'FCF':
        labels["wert1"] = "OCF"
        labels["wert2"] = "Investitionsausgaben"
    elif operation == 'CM':
        labels["wert1"] = "Umsatz"
        labels["wert2"] = "Variable Kosten"

    # Berechnungslogik
    try:
        if operation == 'ROI' and wert1 and wert2:
            ergebnis = (float(wert1) / float(wert2)) * 100  # Berechnung der Kapitalrendite (ROI)
        elif operation == 'EBIT' and wert1 and wert2 and wert3:
            ergebnis = float(wert1) - float(wert2) - float(wert3)  # Berechnung des EBIT
        elif operation == 'EPS' and wert1 and wert2:
            ergebnis = float(wert1) / float(wert2)  # Berechnung des Gewinns pro Aktie
        elif operation == 'ROE' and wert1 and wert2:
            ergebnis = (float(wert1) / float(wert2)) * 100  # Berechnung der Eigenkapitalrendite (ROE)
        elif operation == 'EVA' and wert1 and wert2:
            ergebnis = float(wert1) - float(wert2)  # Berechnung des Economic Value Added (EVA)
        elif operation == 'CM' and wert1 and wert2:
            ergebnis = float(wert1) - float(wert2)  # Berechnung der Deckungsbeitragsmarge
        elif operation == 'OCF' and wert1 and wert2 and wert3:
            ergebnis = float(wert1) + float(wert2) - float(wert3)  # Berechnung des operativen Cashflows (OCF)
        elif operation == 'LCR' and wert1 and wert2:
            ergebnis = float(wert1) / float(wert2)  # Berechnung der Liquiditätskennzahl (LCR)
        elif operation == 'FCF' and wert1 and wert2:
            ergebnis = float(wert1) - float(wert2)  # Berechnung des Free Cashflows (FCF)
        elif operation == 'Break-Even Point' and wert1 and wert2 and wert3:
            ergebnis = float(wert1) / (float(wert2) - float(wert3))  # Berechnung des Break-Even Points
        elif operation == 'EKQ' and wert1 and wert2:
            ergebnis = (float(wert1) / float(wert2)) * 100  # Berechnung der Eigenkapitalquote (EKQ)
    except ValueError:
        ergebnis = "Ungültige Eingabe"  # Fehlerbehandlung für ungültige Eingaben

    # Kontext für das Template
    context = {
        "operation": operation,  # Angeforderte Operation
        "labels": labels,  # Labels für die Eingabewerte
        "wert1": wert1,  # Erster Wert
        "wert2": wert2,  # Zweiter Wert
        "wert3": wert3,  # Dritter Wert (optional)
        "ergebnis": ergebnis  # Berechnetes Ergebnis
    }
    return render(request, 'kpi/taschenrechner.html', context)  # Rendert das Template mit dem Kontext