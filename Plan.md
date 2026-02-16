# Cursor-its-magic-Team Kit – Masterplan (Template + Setup + Workflow + Voice + CI/CD)

> Zweck dieses Dokuments: Du (eine andere AI) sollst daraus ein **drop-in “Cursor-its-magic-Team Kit”** bauen, das die **its-magic-Herangehensweise** (Intake → Rückfragen → Specs → Plan → Execute → Verify) mit einem **AI-Dev-Team** (PO, Tech Lead, Dev, QA, Release, Curator) kombiniert – **Cursor-native** mit **Commands, Rules, Skills, Subagents und Hooks**.  
> Zusatzanforderungen:  
> 1) **Sprachsteuerung** für möglichst viele Sprachen (multilingual STT)  
> 2) **Automatisierte Tests + CI/CD** (lokal über Hooks + remote über GitHub Actions Templates)  
> Fokus: **nur Cursor** (kein n8n).  
> Priorität: **Context-Erneuerung/Anti-Code-Rot**, Pausieren/Resuming ohne Chaos, verlässliche Handoffs/Artefakte.

---

## 1) Ziele & Nicht-Ziele

### Ziele
- User muss **nur die Idee schildern** (optional per Sprache).
- Danach kommen **gezielte Rückfragen** (wie bei its-magic), bis die erste **User Story** + **Acceptance Criteria** stehen.
- Architektur/Design/Beispiele (Website-Inspiration, Grafik/UX) werden **systematisch erfasst** und als Artefakte gespeichert.
- Danach läuft der Prozess weitgehend automatisch:
  - Plan → Tasks → Umsetzung → Tests → Fixes → Release-Vorbereitung
- **Großprojekte** möglich:
  - jederzeit **pausieren/resumen**
  - Änderungen ohne Chaos
- Kein Wissensverlust:
  - Subagents arbeiten getrennt, aber **alles Wichtige wird in Files persistiert**
  - Curator sorgt für **kompaktes, aktuelles Context Pack** (Anti-Code-Rot)
- Eskalationslogik:
  - bei gravierenden Auswirkungen wird automatisch eine **Decision** erzeugt und der User zur Entscheidung aufgefordert.
- **Automatisierte Qualität**
  - lokal: Hooks (Tests/Checks, Kontext-Gates)
  - remote: CI/CD Templates (GitHub Actions), Command-gesteuert über Runbook

### Nicht-Ziele (out of scope)
- n8n / Webhooks / externe Orchestrierung
- “Freies Agenten-Geplapper” ohne Artefakt-Handoffs
- Vollautomatisches Production-Deploy ohne Decision/Approval-Gate

---

## 2) Grundprinzipien (Anti-Code-Rot)

1. **Repo ist Gedächtnis** – nicht die Chat-Historie.
2. **Context Pack** wird kontinuierlich gepflegt (Verdichtung statt Aufblähen).
3. **Jede Rolle schreibt Handoffs**: Ergebnisse landen in Dateien.
4. **Gates/Checks erzwingen Persistenz**
   - nach relevanten Änderungen müssen `state.md`/Handoffs/Sprint-Summary aktualisiert sein
   - Tests/Lint/Typecheck als Qualitäts-Gate (wo möglich)
5. **Pause/Resume = First-Class**
   - Pause schreibt Checkpoint
   - Resume lädt nur Kontext-Pack + Sprint-Artefakte (frischer Kontext)
6. **Voice ist nur ein Input-Layer**
   - STT tippt Text in Cursor (wie Tastatur)
   - Workflow bleibt identisch (Commands/Artefakte)

---

## 3) Deliverables (was implementiert werden soll)

### A) Template-Repo-Inhalte
- `.cursor/commands/*.md` (Slash Commands)
- `.cursor/rules/*.mdc` (Rules mit Globs/Frontmatter)
- `.cursor/skills/<skill>/SKILL.md` + Templates
- `.cursor/agents/*.mdc` (Subagent-Definitionen)
- `.cursor/hooks.json` + Hook-Dispatcher Script
- `docs/*`, `sprints/*`, `handoffs/*`, `decisions/*` (Artefakte)

### B) Voice-Input Enablement (multilingual)
- Dokumentation im README: Voice-Optionen
- Optional: Empfehlung “Text Expander” Pattern für zuverlässige Slash-Commands

### C) CI/CD Templates (optional, aber enthalten)
- `.github/workflows/ci.yml` (Tests/Lint/Typecheck) – liest Commands aus `docs/engineering/runbook.md`
- `.github/workflows/deploy.yml` (staging/prod manuell startbar) – liest Deploy Commands aus Runbook
- Runbook muss Command-Keys enthalten (siehe Abschnitt 7)

### D) Optional: Installer/Updater Script
- kopiert Kit in bestehende Repos (idempotent, nicht blind überschreiben)
- nur Setup/Upgrade – nicht Laufzeit-Orchestrierung

---

## 4) Ziel-Ordnerstruktur (Soll)

.
├─ .cursor/
│ ├─ commands/
│ │ ├─ intake.md
│ │ ├─ discovery.md
│ │ ├─ architecture.md
│ │ ├─ sprint-plan.md
│ │ ├─ execute.md
│ │ ├─ qa.md
│ │ ├─ release.md
│ │ ├─ pause.md
│ │ ├─ resume.md
│ │ └─ refresh-context.md
│ ├─ rules/
│ │ ├─ core.mdc
│ │ ├─ quality.mdc
│ │ ├─ handoffs.mdc
│ │ └─ escalation.mdc
│ ├─ skills/
│ │ └─ its-magic/
│ │ ├─ SKILL.md
│ │ └─ templates/
│ │ ├─ story.md
│ │ ├─ acceptance.md
│ │ ├─ architecture.md
│ │ ├─ decision.md
│ │ ├─ sprint.md
│ │ └─ handoff.md
│ ├─ agents/
│ │ ├─ po.mdc
│ │ ├─ tech-lead.mdc
│ │ ├─ dev.mdc
│ │ ├─ qa.mdc
│ │ ├─ release.mdc
│ │ └─ curator.mdc
│ ├─ hooks.json
│ ├─ scratchpad.md
│ └─ hooks/
│ ├─ hook.py
│ └─ README.md
├─ docs/
│ ├─ product/
│ │ ├─ vision.md
│ │ ├─ backlog.md
│ │ └─ acceptance.md
│ └─ engineering/
│ ├─ architecture.md
│ ├─ decisions.md
│ ├─ state.md
│ └─ runbook.md
├─ sprints/
│ └─ S0001/
│ ├─ sprint.md
│ ├─ tasks.md
│ ├─ progress.md
│ ├─ qa-findings.md
│ └─ summary.md
├─ decisions/
│ └─ DEC-0001.md
├─ handoffs/
│ ├─ po_to_tl.md
│ ├─ tl_to_dev.md
│ ├─ dev_to_qa.md
│ ├─ qa_to_dev.md
│ ├─ release_notes.md
│ └─ resume_brief.md
└─ .github/
└─ workflows/
├─ ci.yml
└─ deploy.yml


---

## 5) Rollenmodell (AI-Dev-Team)

User ist:
- **Customer / Entscheider / Mastermind / PO-Support**
- greift ein, wenn Decision-Gate triggert.

Subagents:
1) PO: Rückfragen, Story, Acceptance, Backlog
2) Tech Lead: Architektur, Plan, Risiken, Tasks
3) Dev: Implementierung task-weise + Summary/Handoffs + state update
4) QA: Testplan, Tests, Findings, Verify
5) Release: Release Notes, Versioning, Deploy-Schritte, Runbook
6) Curator: Kontext verdichten, Anti-Code-Rot, Entscheidungen/State sauber

---

## 6) Artefakte (Single Source of Truth)

### Produkt
- `docs/product/vision.md`
- `docs/product/backlog.md`
- `docs/product/acceptance.md`

### Engineering
- `docs/engineering/architecture.md`
- `docs/engineering/decisions.md`
- `docs/engineering/state.md`
- `docs/engineering/runbook.md`

### Sprint
- `sprints/Sxxxx/sprint.md`
- `sprints/Sxxxx/tasks.md`
- `sprints/Sxxxx/progress.md`
- `sprints/Sxxxx/qa-findings.md`
- `sprints/Sxxxx/summary.md`

### Decisions
- `decisions/DEC-xxxx.md`

### Handoffs
- `handoffs/*.md`

---

## 7) Runbook-Keys (für Automatisierung)

In `docs/engineering/runbook.md` sollen folgende Keys (optional) unterstützt werden:

- `TEST_COMMAND: <...>`
- `LINT_COMMAND: <...>`
- `TYPECHECK_COMMAND: <...>`
- `DEPLOY_STAGING_COMMAND: <...>`
- `DEPLOY_PROD_COMMAND: <...>`

Regeln:
- Wenn Commands nicht gesetzt sind, läuft alles **fail-open** (kein unnötiges Blocken).
- Hooks/CI/CD sollen Commands nur ausführen, wenn sie plausibel gesetzt sind (nicht Template-Platzhalter).

---

## 8) Workflow (End-to-End)

### Phase 0: Intake (User → PO)
1) User beschreibt Idee (Text oder Voice).
2) PO stellt Rückfragen, bis klar:
   - Zielgruppe/Nutzen
   - Scope in/out
   - Constraints
   - Erfolgskriterien
3) PO schreibt/aktualisiert:
   - `vision.md`, `backlog.md` (US-0001), `acceptance.md`
   - `handoffs/po_to_tl.md`
4) Decision Gate falls nötig.

### Phase 1: Discovery (Design/UX/Inspiration)
- sammelt Referenzen/Pattern, dokumentiert:
  - in `vision.md` (Look/Feel/UX)
  - ggf. neue Stories im Backlog
- Decision Gate falls nötig.

### Phase 2: Architecture (TL)
- Architektur kurz + Risiken + Tradeoffs:
  - `architecture.md`, `decisions.md`, `state.md`

### Phase 3: Sprint Plan (TL)
- sprint anlegen (Sxxxx) + atomic tasks:
  - `sprint.md`, `tasks.md`, `progress.md`, `handoffs/tl_to_dev.md`

### Phase 4: Execute (Dev)
- pro Task:
  - Code ändern
  - `summary.md` + `state.md` aktualisieren
  - ggf. `dev_to_qa.md`

### Phase 5: QA Loop (QA ↔ Dev)
- `qa-findings.md` + `qa_to_dev.md`
- Dev fixt → QA verifiziert → schließen
- `state.md` updaten

### Phase 6: Release + Context Refresh
- Release: `release_notes.md`, Runbook updaten
- Curator: `/refresh-context`

### Pause/Resume jederzeit
- Pause: state/progress/resume_brief aktualisieren
- Resume: nur Kontext-Pack + Sprint + offene Decisions laden und weiter

---

## 9) Eskalationslogik (Decision Gate)

Trigger:
- Scope-Änderung / Acceptance nicht erfüllbar
- Security/Auth/Permissions
- Datenmigration/Datenverlust-Risiko
- neue große Dependency/Plattformwechsel
- Architekturwechsel/Refactor groß
- Breaking changes/API
- unknown unknowns / hoher Aufwand / unklare Machbarkeit

Vorgehen:
1) Erzeuge `decisions/DEC-xxxx.md` (2–3 Optionen + Impact + Empfehlung)
2) Frage an User (A/B/C)
3) Stop bis Entscheidung
4) Danach `decisions.md` kurz aktualisieren

---

## 10) Cursor-Integration: Was genau zu bauen ist

### A) Commands (`.cursor/commands/*`)
Erstelle 10 Slash-Commands:
- `intake`
- `discovery`
- `architecture`
- `sprint-plan`
- `execute`
- `qa`
- `release`
- `pause`
- `resume`
- `refresh-context`

Jeder Command:
- sagt, welche Subagents genutzt werden
- welche Artefakte zu lesen/schreiben sind
- welche Stop-Conditions gelten (Decision Gate / Missing Handoff)

### B) Rules (`.cursor/rules/*.mdc`)
- `core.mdc` – Phasenworkflow + Context Pack Pflicht
- `quality.mdc` – kleine Schritte + Tests/Checks
- `handoffs.mdc` – Handoffs/State Pflicht, kein hidden context
- `escalation.mdc` – Decision Gate

### C) Skills (`.cursor/skills/its-magic/`)
- `SKILL.md` beschreibt Workflow + Artefakte
- Templates (story, acceptance, architecture, decision, sprint, handoff)

### D) Subagents (`.cursor/agents/*.mdc`)
- po, tech-lead, dev, qa, release, curator
- Jeder Subagent:
  - klare Inputs/Outputs (Dateien)
  - Artefaktpflicht: nichts nur im Chat lassen
  - kurze, strukturierte Updates

### E) Hooks (`.cursor/hooks.json` + Hook-Dispatcher Script)
Minimalziele:
1) beforeShellExecution: blocke eindeutig gefährliche Commands
2) beforeReadFile: frage bei Secret-artigen Dateien nach
3) afterFileEdit: tracke “Code geändert vs Context refreshed”
4) stop: optionaler Followup-Loop
   - erinnert an Context Refresh, wenn Code geändert aber Docs nicht aktualisiert
   - optional: “loop until tests green” (wenn TEST_COMMAND gesetzt)

Konfiguration über `.cursor/scratchpad.md`:
- `its-magic_CONTEXT_STRICT=1`
- `LOOP_UNTIL_GREEN=0/1`
- `RUN_TESTS_ON_EDIT=0/1` (optional, kann teuer sein)
- `DONE` beendet Loops

---

## 11) Voice Input (multilingual) – Anforderungen & Integration

### Ziel
User kann in beliebiger Sprache sprechen. Das Ergebnis ist **Text in Cursor**, der den normalen `/*` Workflow startet.

### Architektur-Prinzip
Voice ist ein **Input-Layer**, kein Workflow-Layer:
- STT → Text → Cursor Agent Chat/Composer → `/intake` etc.

### Unterstützte Strategien (dokumentieren im README)
**Option A: OS-Diktat**
- funktioniert ohne Setup, aber Sprachumfang variiert je OS.

**Option B: Cursor Voice (wenn vorhanden/stabil)**
- direkt in Cursor sprechen.

**Option C: Open-Source Local STT (empfohlen für “möglichst alle Sprachen”)**
- Whisper/whisper.cpp-basierte Dictation-App
- Hotkey → Transkription → Text ins aktive Feld / Clipboard → Paste in Cursor

### “Slash-Command Reliability” Pattern (empfohlen)
Damit STT nicht “/intake” kaputt erkennt:
- Nutze einen Text-Expander/Hotkey, der `/intake ` einfügt
- User diktiert nur den Inhalt (in beliebiger Sprache)

Dokumentiere das Pattern, ohne zwingend ein Tool vorzuschreiben.

---

## 12) CI/CD Templates (GitHub Actions)

### CI
- `.github/workflows/ci.yml`
- Trigger: push auf main + PR
- Liest aus `runbook.md`:
  - TEST_COMMAND, LINT_COMMAND, TYPECHECK_COMMAND
- Führt aus, wenn gesetzt (kein Platzhalter)
- Falls nichts gesetzt: job endet erfolgreich mit Hinweis

### CD
- `.github/workflows/deploy.yml`
- Trigger: workflow_dispatch
- Input: environment = staging|prod
- Liest aus `runbook.md`:
  - DEPLOY_STAGING_COMMAND, DEPLOY_PROD_COMMAND
- Fail, wenn Command fehlt (damit Deploy nicht “scheinbar” passiert)

---

## 13) Akzeptanzkriterien (Definition of Done für das Kit)

Das Kit ist “fertig”, wenn:
- User kann `/intake` starten (auch via Voice-Text) und bekommt Rückfragen
- Story + Acceptance wird in Docs geschrieben
- Sprint Plan erzeugt `sprints/Sxxxx/*` + Handoffs
- Execute/QA/Release funktionieren über Artefakte
- Pause/Resume funktioniert ohne Drift
- Decision Gate erzeugt `DEC-xxxx.md` und stoppt bis Entscheidung
- Curator hält `state.md` & `decisions.md` kurz
- Hooks funktionieren fail-open und blocken nur klar Gefährliches
- CI/CD Workflows existieren und nutzen Runbook-Commands

---

## 14) Implementierungs-Checkliste (für die andere AI)

1) Repo-Struktur gemäß Abschnitt 4 erstellen
2) 10 Commands schreiben (inkl. IO + Stop-Conditions)
3) 4 Rules `.mdc` schreiben (mit Globs)
4) Skill + Templates anlegen
5) 6 Subagents definieren (IO-klar, artefaktpflichtig)
6) Hooks:
   - `.cursor/hooks.json`
   - `.cursor/hooks/hook.py` Dispatcher
   - `.cursor/scratchpad.md` Flags
7) Docs-Templates in `docs/*` + Sprint Starter anlegen
8) CI/CD:
   - `.github/workflows/ci.yml`
   - `.github/workflows/deploy.yml`
   - Runbook-Keys ergänzen (Abschnitt 7)
9) README erweitern:
   - Quick Start
   - Voice Optionen + Slash-Command Pattern
   - CI/CD Nutzung über Runbook-Commands

---

## 15) Ende

> Implementiere nun das komplette “Cursor-its-magic-Team Kit” als Template-Repo gemäß diesem Plan (inkl. Voice-Dokumentation und CI/CD Templates).
