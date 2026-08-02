# T3Diag

> Open-source diagnostics, analysis and data logging platform for classic Volkswagen vehicles.

> Open-Source-Plattform für Diagnose, Analyse und Datenaufzeichnung klassischer Volkswagen-Fahrzeuge.

---

# 🇩🇪 Deutsch

## Projektziel

T3Diag ist ein langfristig angelegtes Open-Source-Projekt zur Entwicklung einer professionellen Diagnose-, Analyse- und Logging-Plattform für klassische Volkswagen-Fahrzeuge.

Der Schwerpunkt liegt zunächst auf dem Volkswagen T3 mit 2E-Motor und Digifant-Steuergerät (037 906 022 AM). Die Architektur wird von Beginn an modular entwickelt und soll später weitere Steuergeräte und Fahrzeugplattformen unterstützen.

## Geplante Funktionen

- K-Line Kommunikation
- vollständige KWP1281-Implementierung
- Steuergeräte erkennen
- Fehlercodes lesen und löschen
- Messwertblöcke auslesen
- Live-Diagnose
- GPS-Anbindung
- SQLite-Datenbank
- CSV-Export
- Datenlogger
- automatische Beschleunigungsmessung
- Diagramme
- Dashboard
- Weboberfläche

## Entwicklungsgrundsätze

- saubere Architektur
- vollständige Dokumentation
- keine Protokolle raten
- reproduzierbare Messungen
- Hardware und Software strikt trennen
- Unit-Tests
- Type Hints
- PEP8

---

# 🇬🇧 English

## Project Goal

T3Diag is a long-term open-source project to build a professional diagnostics, analysis and data logging platform for classic Volkswagen vehicles.

The first supported vehicle is the Volkswagen T3 with the 2E engine and Digifant ECU (037 906 022 AM). The software is designed with a modular architecture to support additional ECUs in the future.

## Planned Features

- Native K-Line communication
- Complete KWP1281 implementation
- ECU identification
- Read and clear fault codes
- Read measuring blocks
- Live diagnostics
- GPS integration
- SQLite database
- CSV export
- Data logger
- Automatic acceleration measurements
- Charts
- Dashboard
- Web interface

## Development Principles

- Clean Architecture
- Complete Documentation
- No undocumented assumptions
- Reproducible measurements
- Separation of hardware and software
- Unit Tests
- Type Hints
- PEP8

---

## Repository Structure

```text
docs/           Documentation
hardware/       Hardware documentation
firmware/       ESP32 firmware
src/            Python source code
tests/          Unit tests
scripts/        Utility scripts
data/           Measurement data
logs/           Log files
```

---

## License

MIT License
