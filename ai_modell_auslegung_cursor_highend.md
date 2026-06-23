# AI-Modell-Auslegung für Cursor / Coding-Agenten

Stand: 2026-06-23  
Ziel: Rollenbasierte Modellwahl für Cursor, Coding-Agenten und komplexe bis extrem anspruchsvolle Softwareentwicklung.

> Snapshot-Hinweis: Modellpreise und Verfügbarkeit ändern sich schnell. Dieses Dokument ist eine praktische Arbeitsgrundlage, keine dauerhaft gültige Preisliste.

---

## Kurzfazit

Die beste Strategie ist nicht, immer das teuerste Modell zu nutzen, sondern Modelle nach Rolle einzusetzen:

> **Qwen3.7 Plus für günstige Masse, Composer 2.5 Standard für Cursor-DEV, Kimi K2.7 Code für schwieriges Coding, GLM-5.2 für Architektur/QA/Release und Claude/GPT/Gemini als High-End-Gates.**

Für super anspruchsvolle Projekte:

> **Claude Opus / GPT-5.5 / Gemini Pro / GLM-5.2 nicht als Dauer-DEV verheizen, sondern als Chief Architect, Reviewer, QA-Gate und Release-Gate einsetzen.**

---

## Grundprinzip

- Nicht ein Modell für alles verwenden.
- DEV verbraucht die meisten Tokens und sollte deshalb günstig bleiben.
- PO, SA, QA und Release sind Qualitäts-Gates.
- Premium-Modelle dort einsetzen, wo Fehler später teuer werden.
- Cursor Auto vermeiden, wenn reproduzierbare Qualität wichtig ist.
- Composer 2.5 Standard ist weiterhin stark.
- Composer 2.5 Fast nur bewusst nutzen, weil du hauptsächlich Geschwindigkeit bezahlst.
- Für sehr komplexe Projekte immer mindestens zwei unterschiedliche Modellfamilien gegeneinander prüfen lassen.

---

## Modell-Klassen

| Klasse | Modelle | Einsatz |
|---|---|---|
| Günstige Worker | Qwen3.7 Plus, Composer 2.5 Standard, GLM-4.7, DeepSeek V4 Flash | DEV, kleine Fixes, Tests, Routine |
| Starke Coding-Agenten | Kimi K2.7 Code, GLM-5.2, Qwen3.7 Plus, Grok Build | schwierige DEV-Tickets, Refactors, Long-Horizon-Coding |
| Architektur / QA / Release | GLM-5.2, Claude Sonnet, Claude Opus, GPT-5.5, Gemini Pro | Systemdenken, Reviews, Risikoanalyse, Freigaben |
| Premium-Gatekeeper | Claude Opus, GPT-5.5, GPT-5.5 Pro, Gemini Pro | kritische Architektur, Security, Release-Go/No-Go |
| Cost-Scale-Modelle | DeepSeek V4 Pro/Flash, Qwen3.7 Plus, GLM-5.2 | große Mengen, Backfills, viele Agent-Runs |

---

## Modell-Einschätzung

| Modell | Einschätzung | Beste Rolle |
|---|---|---|
| Qwen3.7 Plus | Sehr gute Preis/Leistung, stark für Coding, Agenten, Tool-Use, Vision und GUI-nahe Aufgaben | DEV, QA-Basis, Browser-/GUI-Tests, kleine/mittlere Apps |
| Composer 2.5 Standard | Sehr gutes Cursor-DEV-Modell, günstig und gut integriert | DEV in Cursor |
| Kimi K2.7 Code | Sehr stark für schwieriges Coding und längere Agent-Aufgaben | DEV schwierig, Refactor, Code-Review |
| GLM-5.2 | Sehr stark für lange Kontexte, Architektur, QA, Release und Projekt-Level-Engineering | SA, QA, Release, Long-Horizon-Agent |
| GLM-4.7 | Günstig und solide für Routineaufgaben | kleine Apps, einfache PO/QA/Release-Aufgaben |
| DeepSeek V4 Pro | Extrem günstige API für große Mengen, gute Option für Scale-Workloads | Massentasks, zweite Meinung, Low-Cost-Agent |
| DeepSeek V4 Flash | Sehr günstig, eher für Routine/Backfills als für kritische Architektur | einfache DEV-/Analyse-Masse |
| Grok 4.3 | Stark bei Tool-Use, agentischem Reasoning und schneller Iteration | Tool-Agent, Recherche-/Agent-Routing, zweite Meinung |
| Grok Build | Speziell für agentische Coding-Workflows | Coding-Agent, schneller DEV-Worker |
| Gemini 3.1 Pro | Stark bei Multimodalität, großen Kontexten, Synthese und strukturiertem Reasoning | Research, Produkt-/UX, Multimodal-QA, Long-Context |
| Claude Sonnet | Teurer, aber stark bei PO, QA, Reviews und komplexen Anforderungen | PO, QA, Release-Gate |
| Claude Opus | Sehr stark bei tiefem Reasoning, Architektur, Coding-Reviews und anspruchsvoller Analyse | Chief Architect, Principal Reviewer |
| GPT-5.5 | Sehr stark als Allround-Frontier-Modell für komplexe Planung, Agenten, Coding, Computer-Use und wissenschaftliche/strategische Analyse | Final Gate, Chief Architect, Strategist |
| GPT-5.5 Pro | Maximalmodell für besonders kritische Entscheidungen, aber extrem teuer | Nur für finale High-Risk-Reviews |

---

## Rollen

| Rolle | Aufgabe | Empfohlene Modelle |
|---|---|---|
| Customer / Idee | Idee schärfen, Nutzen, Zielgruppe, grober Scope | Qwen3.7 Plus, Kimi K2.7 Code, Claude Sonnet, Gemini Pro |
| PO | Epics, User Stories, Acceptance Criteria, Priorisierung | GLM-5.2, Claude Sonnet, Claude Opus |
| SA | Architektur, Modulgrenzen, Datenmodell, Schnittstellen, DEV-Vorgaben | GLM-5.2, Claude Opus, GPT-5.5, Gemini Pro |
| DEV | Umsetzung, Refactoring, Bugfixes, kleine Tests | Qwen3.7 Plus, Composer 2.5 Standard, DeepSeek V4 Pro |
| DEV schwierig | schwere Bugs, größere Refactors, agentisches Coding über viele Schritte | Kimi K2.7 Code, GLM-5.2, Claude Opus |
| QA | Tests, Edge Cases, manuelle Browser-Flows, Risikoanalyse | GLM-5.2, Claude Sonnet, Claude Opus, Qwen3.7 Plus |
| Security / Red Team | Bedrohungsmodell, Abuse Cases, Secrets, Rechte, Datenflüsse | GPT-5.5, Claude Opus, Gemini Pro |
| Release | Changelog, Migrationen, Rollback, Deployment-Check, Security-Freigabe | GLM-5.2, Claude Sonnet, GPT-5.5 |
| Final Go/No-Go | finale Entscheidung bei hohem Risiko | GPT-5.5, Claude Opus, GPT-5.5 Pro |

---

# Projektgrößen

## Kleine unkomplizierte Apps

Beispiele: kleines Tool, CRUD-App, Dashboard, Bot, Single-Service, kleine React/Rust/Node-App.

| Rolle | Modell |
|---|---|
| Customer | Qwen3.7 Plus / GLM-4.7 |
| PO | Qwen3.7 Plus / GLM-4.7 |
| SA | GLM-5.2 oder Kimi K2.7 Code |
| DEV | Qwen3.7 Plus oder Composer 2.5 Standard |
| QA | Qwen3.7 Plus |
| Release | GLM-4.7 / Qwen3.7 Plus |

### Empfehlung

Für kleine Apps ist Qwen3.7 Plus der Sweet Spot. Composer 2.5 Standard ist in Cursor ebenfalls sehr gut.

---

## Komplexere Apps

Beispiele: mehrere Services, Datenbank, Auth, Rollen/Rechte, Frontend + Backend, Docker, API, Worker, Queue, Monitoring.

| Rolle | Modell |
|---|---|
| Customer | Kimi K2.7 Code / Qwen3.7 Plus |
| PO | GLM-5.2 / Claude Sonnet |
| SA | GLM-5.2 |
| DEV normal | Qwen3.7 Plus / Composer 2.5 Standard |
| DEV schwierig | Kimi K2.7 Code |
| QA | GLM-5.2 / Claude Sonnet |
| Browser-/GUI-QA | Qwen3.7 Plus |
| Release | GLM-5.2, bei kritisch Claude Sonnet oder GPT-5.5 |

### Empfehlung

Nicht den DEV teuer machen. Günstig coden lassen und mit GLM-5.2, Claude oder GPT reviewen.

---

## Mega-komplexe Software / möglicher Monolith

Beispiele: Cortana/Hermes-System, Trading-System, Finanzplattform, große Plattformen, modulare Monolithen, mehrere Teams/Rollen.

| Rolle | Primärmodell | Review / Gate |
|---|---|---|
| Customer | Claude Sonnet / GPT-5.5 / GLM-5.2 | Gemini Pro |
| PO | Claude Sonnet / GLM-5.2 | GPT-5.5 |
| SA | GLM-5.2 / GPT-5.5 | Claude Opus |
| DEV normal | Qwen3.7 Plus / Composer 2.5 Standard | Kimi K2.7 Code |
| DEV schwierig | Kimi K2.7 Code | GLM-5.2 / Claude Opus |
| QA | GLM-5.2 / Claude Sonnet | GPT-5.5 |
| Security | Claude Opus / GPT-5.5 | Gemini Pro |
| Release | GLM-5.2 / Claude Sonnet | GPT-5.5 |

### Empfehlung

Bei Mega-Projekten ist Rollen-Trennung wichtiger als das einzelne Modell. Architektur, QA, Security und Release müssen getrennte Gates sein.

---

# Super-High-Sophisticated Projects

Diese Kategorie ist für Projekte, bei denen Fehler sehr teuer werden können oder die über lange Zeit wachsen:

- große modulare Monolithen
- eigene Plattformen
- Agenten-Systeme
- AI-Betriebssysteme / lokale Assistenten
- Trading-/Finanzsysteme
- kritische Infrastruktur
- Systeme mit Security-, Privacy- oder Datenbankrisiko
- Multi-Service-Architekturen
- autonome oder semi-autonome Agenten
- Systeme mit langfristiger Wartbarkeit

## Beste Modelle am Markt für diese Kategorie

| Modell | Warum relevant | Hauptrolle |
|---|---|---|
| Claude Opus 4.8 | Sehr stark bei tiefem Reasoning, Architektur, Code-Review, kritischem Denken und anspruchsvoller Analyse | Principal Architect, Principal Reviewer |
| GPT-5.5 | Sehr stark als universelles Frontier-Modell für Planung, Coding, Agenten, Computer-Use und komplexe Problemlösung | Chief Architect, Final Gate |
| GPT-5.5 Pro | Extrem teuer, aber sinnvoll für finale Hochrisiko-Entscheidungen | Final Safety/Architecture Gate |
| Gemini 3.1 Pro | Sehr stark bei Multimodalität, Long-Context, Synthese, Produkt-/UX-Analyse und strukturiertem Reasoning | Research, Product Strategy, Multimodal QA |
| GLM-5.2 | Herausragendes Preis/Leistungsmodell für Long-Horizon-Coding, 1M-Kontext und projektweite Engineering-Aufgaben | Long-Horizon SA/QA/Agent |
| Kimi K2.7 Code | Stark für lange Coding-Aufgaben, Refactoring, Agentic Coding und Multi-Step-DEV | Senior DEV Agent |
| Qwen3.7 Plus | Günstig, stark bei Coding, Tool-Use, Vision und GUI-naher Agentik | High-Volume DEV / GUI-QA |
| Grok 4.3 | Gute Option für Tool-Agenten, Routing, schnelle Analyse und zweite Meinung | Agentic Tool Orchestrator |
| DeepSeek V4 Pro | Sehr günstige Option für große Mengen und zusätzliche Review-/DEV-Durchläufe | Cost-Scale Agent |
| Claude Sonnet | Nicht immer absolut beste Qualität, aber sehr gutes Praxis-Gate für PO/QA/Release | Balanced Gatekeeper |

---

## High-End-Rollenmatrix

| Rolle | Max-Quality | Preis/Leistung | Low-Cost Scale |
|---|---|---|---|
| Product Vision | GPT-5.5 / Claude Opus | Gemini Pro / Claude Sonnet | Qwen3.7 Plus |
| PO / ACs | Claude Opus / GPT-5.5 | Claude Sonnet / GLM-5.2 | Qwen3.7 Plus |
| Chief Architect | GPT-5.5 / Claude Opus | GLM-5.2 / Gemini Pro | Kimi K2.7 Code |
| Domain Modelling | Claude Opus / GPT-5.5 | GLM-5.2 | Qwen3.7 Plus |
| Data Model / DB | GPT-5.5 / Claude Opus | GLM-5.2 / Kimi K2.7 Code | DeepSeek V4 Pro |
| API Design | Claude Opus / GPT-5.5 | GLM-5.2 / Kimi K2.7 Code | Qwen3.7 Plus |
| DEV normal | Kimi K2.7 Code / Claude Opus | Qwen3.7 Plus / Composer 2.5 Standard | DeepSeek V4 Pro |
| DEV schwierig | Claude Opus / GPT-5.5 | Kimi K2.7 Code / GLM-5.2 | Qwen3.7 Plus |
| Code Review | Claude Opus / GPT-5.5 | GLM-5.2 / Claude Sonnet | DeepSeek V4 Pro |
| QA Strategy | GPT-5.5 / Claude Opus | GLM-5.2 / Claude Sonnet | Qwen3.7 Plus |
| Browser-/GUI-QA | Gemini Pro / Claude Opus | Qwen3.7 Plus | Qwen3.7 Plus |
| Security Review | GPT-5.5 / Claude Opus | Claude Sonnet / Gemini Pro | GLM-5.2 |
| Release Gate | GPT-5.5 / Claude Opus | GLM-5.2 / Claude Sonnet | DeepSeek V4 Pro |
| Final Go/No-Go | GPT-5.5 Pro / GPT-5.5 / Claude Opus | Claude Opus / GPT-5.5 | nicht empfohlen |

---

## Empfohlene High-End-Kombinationen

### 1. Max-Quality Setup

Für Projekte, bei denen Qualität wichtiger als Kosten ist.

| Rolle | Modell |
|---|---|
| Customer / Vision | GPT-5.5 |
| PO | Claude Opus |
| SA | GPT-5.5 + Claude Opus Gegenprüfung |
| DEV normal | Kimi K2.7 Code / Composer 2.5 Standard |
| DEV schwierig | Claude Opus / GPT-5.5 |
| QA | Claude Opus |
| Security | GPT-5.5 |
| Release | GPT-5.5 |
| Final Gate | GPT-5.5 Pro, nur bei wirklich kritischen Entscheidungen |

### 2. Elite Balanced Setup

Sehr hohe Qualität, aber wirtschaftlicher.

| Rolle | Modell |
|---|---|
| Customer / Vision | Gemini Pro / Claude Sonnet |
| PO | Claude Sonnet |
| SA | GLM-5.2 |
| Architektur-Gegenprüfung | Claude Opus |
| DEV normal | Qwen3.7 Plus / Composer 2.5 Standard |
| DEV schwierig | Kimi K2.7 Code |
| QA | GLM-5.2 / Claude Sonnet |
| Security | Claude Opus oder GPT-5.5 punktuell |
| Release | GLM-5.2 |
| Final Gate | Claude Opus oder GPT-5.5 |

### 3. Frontier-Open / Cost-Control Setup

Für viele Runs, gute Qualität und starke Kostenkontrolle.

| Rolle | Modell |
|---|---|
| Customer / Vision | Qwen3.7 Plus |
| PO | GLM-5.2 |
| SA | GLM-5.2 |
| DEV normal | Qwen3.7 Plus / DeepSeek V4 Pro |
| DEV schwierig | Kimi K2.7 Code |
| QA | GLM-5.2 |
| Security | GLM-5.2 + punktuell Claude/GPT |
| Release | GLM-5.2 |
| Final Gate | Claude Opus oder GPT-5.5 nur bei Risiko |

---

## Super-High-Projektworkflow

### Phase 1: Vision

Modell: GPT-5.5, Claude Opus oder Gemini Pro

Ergebnis:

- Zielbild
- Nicht-Ziele
- Zielgruppe
- Kernnutzen
- Risiken
- Produktgrenzen
- Business- und Technikannahmen

### Phase 2: PO / Requirements

Modell: Claude Sonnet, Claude Opus oder GLM-5.2

Ergebnis:

- Epics
- User Stories
- Acceptance Criteria
- Prioritäten
- Abhängigkeiten
- offene Fragen
- Testbarkeit

### Phase 3: Architektur

Modell: GLM-5.2 + Claude Opus/GPT-5.5 Gegenprüfung

Ergebnis:

- Modulgrenzen
- Datenmodell
- API-Verträge
- Deployment-Architektur
- Security-Konzept
- Logging/Monitoring
- Skalierungsstrategie
- Migrationsstrategie

### Phase 4: DEV

Modell normal: Qwen3.7 Plus / Composer 2.5 Standard  
Modell schwierig: Kimi K2.7 Code / GLM-5.2

Ergebnis:

- kleine Patches
- Tests
- Migrationen
- Feature-Implementierung
- Refactors nur mit Architekturfreigabe

### Phase 5: QA

Modell: GLM-5.2 / Claude Sonnet / Claude Opus

Ergebnis:

- Testmatrix
- Unit-Tests
- Integrationstests
- Browser-Flows
- Edge Cases
- Regressionstests
- Security-Testfälle

### Phase 6: Security / Risk Review

Modell: GPT-5.5 / Claude Opus / Gemini Pro

Ergebnis:

- Threat Model
- Secret-Handling
- Auth/AuthZ-Risiken
- Datenflussprüfung
- Missbrauchsszenarien
- Abhängigkeiten/Supply Chain
- Rechte- und Netzwerkprüfung

### Phase 7: Release

Modell: GLM-5.2 + GPT-5.5/Claude Opus Gate

Ergebnis:

- Changelog
- Deployment-Plan
- Rollback-Plan
- DB-Migration-Check
- Config-Check
- Observability-Check
- Go/No-Go

---

## Multi-Modell-Gate für kritische Architektur

Für sehr wichtige Entscheidungen niemals nur ein Modell fragen.

### Ablauf

1. SA erstellt Architektur mit GLM-5.2.
2. Claude Opus kritisiert Architektur.
3. GPT-5.5 prüft Risiken, blinde Flecken und langfristige Wartbarkeit.
4. Kimi K2.7 Code prüft Umsetzbarkeit aus DEV-Sicht.
5. Finale Entscheidung wird als Architecture Decision Record dokumentiert.

### Ergebnisformat

```md
# ADR-0001: Entscheidungstitel

## Kontext

## Optionen

## Entscheidung

## Begründung

## Konsequenzen

## Risiken

## Gegenmaßnahmen

## Offene Punkte

## Review durch Modelle
- GLM-5.2:
- Claude Opus:
- GPT-5.5:
- Kimi K2.7 Code:
```

---

## Wann welches High-End-Modell?

| Situation | Beste Wahl |
|---|---|
| Tiefes Architekturdenken | Claude Opus / GPT-5.5 |
| Langfristige Systemplanung | GPT-5.5 / GLM-5.2 |
| Riesige Codebase verstehen | GLM-5.2 / Gemini Pro |
| Schwieriger Refactor | Kimi K2.7 Code / Claude Opus |
| Viele günstige Agent-Runs | Qwen3.7 Plus / DeepSeek V4 Pro |
| Browser-/GUI-nahe Analyse | Qwen3.7 Plus / Gemini Pro |
| Multimodale Produktanalyse | Gemini Pro / Qwen3.7 Plus |
| Security-/Risk-Gate | GPT-5.5 / Claude Opus |
| Final Release Gate | GPT-5.5 / Claude Opus |
| Absolutes Max-Accuracy-Gate | GPT-5.5 Pro, falls Kosten egal sind |

---

## Wann sich teure Modelle lohnen

Teure Modelle lohnen sich für:

- Architekturentscheidungen
- Security-Reviews
- Datenmodell-Entscheidungen
- Release-Freigaben
- schwer reproduzierbare Bugs
- kritische Refactors
- rechtlich/finanziell relevante Software
- Agenten mit autonomen Aktionen
- Multi-Service-Systeme
- langfristige Plattformentscheidungen

Teure Modelle lohnen sich meistens nicht für:

- einfache UI-Fixes
- kleine CRUD-Änderungen
- einfache Tests
- Formatierungen
- Boilerplate
- einfache SQLs
- simple Refactors
- Routine-Dokumentation

---

# Beste Preis/Leistungs-Variante

| Rolle | Modell |
|---|---|
| Customer | Qwen3.7 Plus |
| PO | GLM-5.2 |
| SA | GLM-5.2 |
| DEV | Qwen3.7 Plus / Composer 2.5 Standard |
| DEV schwierig | Kimi K2.7 Code |
| QA | GLM-5.2 |
| Browser-QA | Qwen3.7 Plus |
| Release | GLM-5.2 |

---

# Balanced-Setup

| Rolle | Modell |
|---|---|
| Customer | Kimi K2.7 Code |
| PO | Claude Sonnet oder GLM-5.2 |
| SA | GLM-5.2 |
| DEV | Qwen3.7 Plus oder Composer 2.5 Standard |
| DEV schwierig | Kimi K2.7 Code |
| QA | Claude Sonnet / GLM-5.2 |
| Release | GLM-5.2, bei kritisch Claude Sonnet |

---

# High-End-Setup

| Rolle | Modell |
|---|---|
| Customer | GPT-5.5 / Claude Opus |
| PO | GPT-5.5 / Claude Opus |
| SA | GPT-5.5 + Claude Opus Gegenprüfung |
| DEV normal | Qwen3.7 Plus / Composer 2.5 Standard |
| DEV schwierig | Kimi K2.7 Code / Claude Opus |
| QA | GPT-5.5 / Claude Opus / GLM-5.2 |
| Security | GPT-5.5 / Claude Opus |
| Release | GPT-5.5 |
| Final Gate | GPT-5.5 Pro, nur bei maximaler Kritikalität |

---

# Cursor-Prompt-Vorlagen

## Customer

```text
Rolle: Customer / Ideengeber.
Schärfe die Idee, erkenne Nutzen, Zielgruppe, Risiken und Scope.
Erstelle keine technische Lösung, sondern ein klares Produktziel.
```

## PO

```text
Rolle: Product Owner.
Erstelle Epics, User Stories und Acceptance Criteria.
Achte auf testbare Formulierungen, Priorität und fachliche Vollständigkeit.
Keine technische Implementierung.
```

## SA

```text
Rolle: Software Architect.
Erstelle Modulgrenzen, Datenflüsse, APIs, DB-Struktur, Risiken und DEV-ready Aufgaben.
Kein produktiver Code außer Interfaces, Pseudocode oder Dateistruktur.
```

## Chief Architect

```text
Rolle: Chief Software Architect.
Bewerte die Architektur für ein langfristig wachsendes, komplexes System.
Finde versteckte Kopplungen, Skalierungsrisiken, Datenmodell-Probleme, Security-Risiken und Wartbarkeitsprobleme.
Erstelle konkrete Architecture Decision Records und DEV-ready Vorgaben.
```

## DEV

```text
Rolle: DEV.
Setze nur das konkrete Ticket um.
Keine Architekturentscheidungen.
Keine breite Codebase-Suche ohne Rückfrage.
Minimaler Patch.
Tests ergänzen, wenn direkt relevant.
```

## DEV schwierig

```text
Rolle: Senior DEV / Refactor Agent.
Analysiere nur den relevanten Bereich.
Erstelle einen kurzen Änderungsplan.
Setze danach kleine, sichere Schritte um.
Keine großen Architekturänderungen ohne Rückfrage.
Nach jeder Änderung Tests oder statische Checks ausführen.
```

## QA

```text
Rolle: QA.
Prüfe Umsetzung gegen Acceptance Criteria.
Erstelle Unit-, Integration- und Browser-Testfälle.
Suche Edge Cases, Race Conditions, Security- und Regressionsrisiken.
```

## Browser-QA

```text
Rolle: Browser-/GUI-QA.
Simuliere manuelle Tests im Browser.
Prüfe sichtbare UI-Zustände, Fehlermeldungen, Ladezustände, Navigation und Edge Cases.
Erstelle reproduzierbare Testschritte mit Erwartung und Ergebnis.
```

## Security Reviewer

```text
Rolle: Security Reviewer.
Prüfe Authentifizierung, Autorisierung, Secrets, Datenflüsse, Netzwerkgrenzen, Dependency-Risiken, Injection-Risiken und Missbrauchsszenarien.
Gib konkrete Findings mit Schweregrad, Auswirkung und Gegenmaßnahme aus.
```

## Release

```text
Rolle: Release Manager.
Prüfe Changelog, Migrationen, Rollback, Config, Security, Deployment und bekannte Risiken.
Erstelle eine klare Go/No-Go-Empfehlung.
```

---

# Praktischer Workflow

1. Customer-Idee formulieren.
2. PO erstellt Epics, User Stories und Acceptance Criteria.
3. SA zerlegt in Architektur, Module, Schnittstellen und DEV-ready Aufgaben.
4. DEV setzt nur kleine Tickets um.
5. QA prüft gegen ACs und ergänzt Tests.
6. Security prüft Risiken, Rechte, Datenflüsse und Secrets.
7. Release prüft Migration, Rollback, Config und Deployment.
8. Premium-Modell nur als Gate verwenden, nicht für jeden Code-Schritt.

---

# Merksätze

## Allgemein

Billig coden lassen, teuer planen und prüfen lassen.

## Für normale Projekte

Qwen3.7 Plus und Composer 2.5 Standard übernehmen die Masse.  
Kimi K2.7 Code übernimmt schwieriges Coding.  
GLM-5.2 übernimmt Architektur, QA und Release.  
Claude/GPT nur für kritische Gates einsetzen.

## Für super anspruchsvolle Projekte

Claude Opus und GPT-5.5 sind keine Worker, sondern Chef-Reviewer.  
GLM-5.2 ist der starke Long-Horizon-Architekt.  
Kimi K2.7 Code ist der Senior-DEV-Agent.  
Qwen3.7 Plus ist der günstige Massenarbeiter.  
DeepSeek V4 ist der günstige Scale-Agent.  
Gemini Pro ist stark für Multimodalität, Synthese und große Kontextarbeit.

---

# Quellen / Preisprüfung

Vor produktivem Einsatz immer aktuelle Preise und Verfügbarkeit prüfen bei:

- OpenAI API Pricing
- Anthropic Claude API Pricing
- Google Gemini API Pricing
- Z.AI / GLM Pricing
- Kimi API Pricing
- DeepSeek API Pricing
- xAI API Models & Pricing
- OpenRouter Modellseiten
