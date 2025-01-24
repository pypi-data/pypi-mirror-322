# Importierte Module
from django.db import models  # Django-Modul für die Arbeit mit Datenbankmodellen
import json  # Modul für JSON-Datenverarbeitung

# Basisklasse für Unternehmenskennzahlen
class Unternehmenskennzahl:

    #Repräsentiert eine Unternehmenskennzahl.

    def __init__(self, kuerzel, name, definition, berechnungsformel=None, kategorie=None):
        self.kuerzel = kuerzel  # Kürzel der Kennzahl
        self.name = name  # Name der Kennzahl
        self.definition = definition  # Beschreibung/Definition der Kennzahl
        self.berechnungsformel = berechnungsformel  # Formel zur Berechnung der Kennzahl
        self.kategorie = kategorie  # Kategorie, zu der die Kennzahl gehört

    def __str__(self):
        # Gibt die Kennzahl als String aus, z. B. "Name (Kürzel)"
        return f"{self.name} ({self.kuerzel})"

# Kindklasse für Rentabilitätskennzahlen
class Rentabilitaetskennzahl(Unternehmenskennzahl):
    def __init__(self, kuerzel, name, definition, berechnungsformel=None, return_on=None):
        super().__init__(kuerzel, name, definition, berechnungsformel, kategorie="Rentabilität")  # Initialisiert die Basisklasse
        self.return_on = return_on  # Spezifisches Attribut für Rentabilitätskennzahlen

    def berechne_rendite(self, gewinn, kapital):
        # Berechnet die Rendite basierend auf Gewinn und Kapital
        if kapital == 0:
            return "Kapital darf nicht 0 sein"  # Fehlerbehandlung für Division durch Null
        return (gewinn / kapital) * 100  # Rendite in Prozent

# Kindklasse für Liquiditätskennzahlen

class Liquiditaetskennzahl(Unternehmenskennzahl):
    def __init__(self, kuerzel, name, definition, berechnungsformel=None, cashflow=None):
        super().__init__(kuerzel, name, definition, berechnungsformel, kategorie="Liquidität")  # Initialisiert die Basisklasse
        self.cashflow = cashflow  # Spezifisches Attribut für Liquiditätskennzahlen

    def berechne_liquiditaet(self, liquide_mittel, kurzfristige_verbindlichkeiten):
        # Berechnet die Liquidität basierend auf liquiden Mitteln und kurzfristigen Verbindlichkeiten
        if kurzfristige_verbindlichkeiten == 0:
            return "Keine kurzfristigen Verbindlichkeiten"  # Fehlerbehandlung für Division durch Null
        return (liquide_mittel / kurzfristige_verbindlichkeiten) * 100  # Liquidität in Prozent

# Kindklasse für Investitionskennzahlen
class Investitionskennzahl(Unternehmenskennzahl):
    def __init__(self, kuerzel, name, definition, berechnungsformel=None, abzinsungssatz=None):
        super().__init__(kuerzel, name, definition, berechnungsformel, kategorie="Investition")  # Initialisiert die Basisklasse
        self.abzinsungssatz = abzinsungssatz  # Spezifisches Attribut für Investitionskennzahlen

    def berechne_npv(self, cashflows, abzinsungssatz):
        # Berechnet den Nettobarwert (NPV) basierend auf den Cashflows und dem Abzinsungssatz
        npv = sum(cf / (1 + abzinsungssatz)**i for i, cf in enumerate(cashflows))  # Abzinsung der Cashflows
        return npv  # Rückgabe des berechneten NPV

# Beispiel einer Unternehmenskennzahl
beispiel_kennzahl = Unternehmenskennzahl(
    kuerzel="CM",  # Kürzel für "Contribution Margin"
    name="Contribution Margin",  # Name der Kennzahl
    definition="Zeigt, wie viel Umsatz zur Deckung der Fixkosten beiträgt.",  # Beschreibung der Kennzahl
    berechnungsformel="Deckungsbeitrag = Umsatz - variable Kosten",  # Formel zur Berechnung
    kategorie="Rentabilität"  # Kategorie der Kennzahl
)
