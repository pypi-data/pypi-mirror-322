from setuptools import setup, find_packages

# Abhängigkeiten aus requirements.txt lesen
with open("requirements.txt") as f:
    requirements = f.read().splitlines()

setup(
    name="debuzz2",  # Der Paketname
    version="0.1.0",  # Version des Pakets
    description="Ein Django-basiertes Tool zur Verwaltung von Unternehmenskennzahlen",
    long_description=open("README.md", "r", encoding="utf-8").read(),  # Beschreibung aus der README
    long_description_content_type="text/markdown",  # Format der README-Datei
    author="Dein Name",  # Dein Name
    author_email="deine.email@example.com",  # Deine E-Mail
    url="https://github.com/benutzername/debuzz2",  # URL zum Repository
    packages=find_packages(),  # Alle Python-Pakete im Projekt
    include_package_data=True,  # Zusätzliche Dateien (z. B. statische Dateien) einbinden
    install_requires=requirements,  # Abhängigkeiten aus requirements.txt
    classifiers=[
        "Programming Language :: Python :: 3",
        "Framework :: Django",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",  # Mindestversion von Python
)
