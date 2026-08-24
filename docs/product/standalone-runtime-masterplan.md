# Standalone its-magic runtime — master plan (pre-intake)

**Status:** draft idea pack (not a backlog story yet).  
**Intent:** operator source document for a later **`/intake`** (first/new/broad).  
**Repo decision:** implement the **runtime in a new repository**. Do **not** build the agent engine inside this kit repo. This file may live here as the idea source until that repo exists.  
**Related:** OpenCode adapter (this repo) — `docs/product/opencode-adapter-masterplan.md`.  
**Pack hint for PO:** `first-intake-pack` (**US-0068** / **DEC-0050**). Complete-plan mapping required (**US-0081** / **DEC-0064**).

This file is the operator brief. It is not architecture lock, not a DEC, and not an assigned **US-xxxx**. Intake must allocate IDs, write backlog/acceptance, and produce `handoffs/intake_evidence/*.json`. Do not treat headings below as already-shipped contracts.

**Intake location (lock in PO chat):** either (A) intake the *program* here with most plan areas `deferred_ref` to the sibling repo, or (B) create the sibling repo first and run `/intake` there against a copy of this brief. Do not grow a second 100-story Cursor-shaped backlog inside `gsd_cursor` for a product that will not run here.

---

## How to intake this

1. Run **`/intake`** in a fresh **PO** subagent (**BUG-0006**), preferably **in the new runtime repo** once it exists.
2. Point the PO at this file as the idea source (`docs/product/standalone-runtime-masterplan.md` in *this* kit, or the copy in the sibling repo).
3. Use **`first-intake-pack`**. Map every **plan area** in [Plan-area inventory](#plan-area-inventory-us-0081--dec-0064) to a candidate story or an explicit `deferred_ref`.
4. Do **not** clone US-0001–US-0119 one-for-one. Cursor-tax and “tame the host” work is listed under [Drop / do not port](#drop--do-not-port).
5. Persistence must include `plan_area_inventory`, `plan_area_coverage`, `coverage_complete=true`, or fail closed (`INTAKE_PLAN_COVERAGE_MISSING` under `INTAKE_PERSISTENCE_BLOCKED`).
6. If intake runs **in this kit repo**, the only in-repo story should be a **consume contract** (how the runtime calls this kernel). All engine stories belong in the sibling backlog.

---

## One-sentence product

Ship a **Cursor-independent its-magic agent host**: own sessions, subagents, multi-provider APIs (including Chinese), and **code-enforced** phase/role gates — consuming this kit’s artifact kernel and Python validators, not re-prompting 50 Cursor command files.

---

## Why (problem)

The kernel already exists in this repo. What is missing is a **host we own**:

| Pain | Why a standalone (not only OpenCode adapter) |
|------|-----------------------------------------------|
| Rules/skills are advisory | **R-0001**. A host we own can make spawn, permissions, and “no next phase without artifacts” **code**, not markdown. |
| Cursor BYOK/subagent ceiling | **US-0101** / **DEC-0086**. We pick providers and keys per role with no Cursor billing middle layer. |
| OpenCode is still someone else’s engine | Adapter is faster, but plugin APIs, compaction, and session semantics can block **BUG-0006**. Standalone is the escape hatch and the “maximum control” path. |
| `auto_outer_driver.py` is not an LLM loop | **US-0092** / **DEC-0078**: spawn-only state machine. The expensive part (tools, streaming, isolation) is the runtime. |

Operator goal (this thread): own tool; hardcoded behavior; own APIs; real subagents and `/auto`; **not** a VS Code+shell wrapper; **not** an OpenCode fork as the product; **not** a 1:1 story clone.

**Relationship to the adapter:** the OpenCode adapter is the **near-term host**. Standalone is the **owned host**. They share the **same kernel**. They are not two copies of the workflow. Build adapter first unless research proves stock OpenCode cannot isolate sessions; then accelerate standalone.

---

## Design principle — we own Layer 1

Same three layers as the adapter brief. In a standalone, **Layer 1 is our code**, not OpenCode’s.

### Layer 1 — Host-enforced (the product)

Must be implemented as runtime code (not prompts):

- **Session isolation:** each phase is a new session with empty chat memory; only artifacts + a bounded context pack (**US-0023** / **US-0048** / **BUG-0006** / **R-0001**).
- **Tool permissions** per role (`allow` / `ask` / `deny` on edit, bash, spawn, web, …) with path globs.
- **Orchestrator** that Task-spawns the **US-0069** role and **refuses** to execute phase work itself (`AUTO_ORCHESTRATOR_PHASE_EXECUTION`).
- **Provider router:** many API keys live at once; each role/phase uses `provider/slug` (**US-0101** / **US-0102** semantics without Cursor aliases).
- **Validator bridge:** subprocess to this kit’s Python CLIs; fail-closed reason codes unchanged.
- **Stop matrix / ledgers:** reuse **US-0092** loop ideas (cycles, block-retry, drain); implementation may call `auto_outer_driver.py` or a ported library — architecture locks which.

### Layer 2 — Short role system prompts

Role files are **who you are** + **which artifact paths you write**. No 200-line Cursor command dumps. If it can be a permission or a validator, it is not prompt text.

### Layer 3 — Thin commands

Named phases (`intake`, `execute`, `auto`) only: set `phase_id` + spawn role. Command bodies are not the workflow engine.

**Success test:** a model that ignores its prompt still cannot skip isolation, skip validators, edit outside its glob, or continue `/auto` in the same session as the previous role.

**Honesty check:** a “Python loop + LiteLLM + bash” demo is **not** v1 done. v1 done means isolation + permissions + multi-provider + orchestrator + validator bridge are **enforced**. UI can be CLI-first (vision.md: CLI-first, slash-command driven).

---

## In this repo vs not

| Work | Where |
|------|--------|
| Artifact kernel, validators, installer for Cursor/OpenCode packs | **This kit repo** (`gsd_cursor` / `its-magic`) |
| OpenCode adapter | **This kit repo** — see sibling masterplan |
| Standalone runtime (sessions, tools, providers, orchestrator, CLI/TUI) | **New repo** (working name: `its-magic-runtime` — lock at intake) |
| Kernel consume contract (how runtime invokes validators / reads scratchpad / phase matrix) | **Small story in this kit** *or* a published package extracted later |
| Fork of OpenCode as the product | **Out of scope.** Optional later: vendor a thin patch or use OpenCode as a library if license/API allows — research, not v1 default |
| VS Code extension wrapping the CLI | **Deferred.** CLI/TUI first; IDE is a client of the same server |

**DEC-0045:** consumer projects keep `its_magic/` as kit metadata. The runtime binary/app is **not** installed into `its_magic/`. The runtime operates *on* a project that already has (or gets) the kernel artifacts.

---

## First-intake topic answers (US-0068)

Distinct answers for PO `topic_coverage` (do not echo one blob onto every key — **BUG-0007**).

### `users_problem`

Operators who want its-magic’s team workflow with **maximum host control**: real isolated subagents, own API keys (Western + Chinese), behavior that cannot be skipped by ignoring a rules file, and no dependency on Cursor or (long-term) on OpenCode plugin limits.

### `runtime_target_environment`

- **Engine repo:** new git repository (Windows + POSIX).
- **Operator machine:** local CLI first; optional TUI; optional later desktop/IDE client.
- **Target of work:** a project repo that contains the its-magic **kernel** (docs/sprints/handoffs/scripts), installed via existing `its-magic` installer or a runtime bootstrap that *calls* that installer.
- **CI/headless:** same engine, non-interactive; compose with **US-0092** stop/exit codes.
- **Not:** Cursor Agent panel; not “commands that shell into Cursor.”

### `language_framework_runtime`

Lock in architecture (research compares). Default **proposal** (not locked):

- **Orchestrator + permissions + sessions:** one language (candidate: TypeScript on Bun/Node, or Go, or Python). Do not mix three engines in v1.
- **LLM I/O:** existing SDK stack (e.g. Vercel AI SDK / OpenAI-compatible clients) so Chinese OpenAI-compatible endpoints (DeepSeek, Moonshot, Z.AI, DashScope `baseURL`) work without a custom protocol per vendor.
- **Kernel:** remains **Python 3** in the kit; runtime **subprocesses** validators — do not rewrite validators in the runtime language in v1.
- **Config:** YAML/JSON for providers, roles, permissions; no Cursor `.mdc`.

### `architecture_preference`

**Owned harness + consumed kernel** (approach A):

```
its-magic-runtime (new repo)
  ├─ cli / tui
  ├─ session store (isolated per phase)
  ├─ provider catalog (N keys at once)
  ├─ tool runtime (edit, bash, grep, spawn) + permission engine
  └─ orchestrator (US-0069 spawn-only)
        └─ subprocess → kit Python validators
        └─ read/write kernel artifacts in the *project* worktree

its-magic kit (this repo)
  └─ artifacts, scripts, phase matrix, outer-driver semantics
```

Rejected for v1:

- Runtime inside `gsd_cursor` (mixes kit installer identity with an agent product).
- 1:1 port of all Cursor commands/rules.
- VS Code+PowerShell as the host.
- Full OpenCode fork as the deliverable.
- Reimplementing validators in a second language.

**OpenCode reuse:** allowed as *reference* (patterns, MIT). Vendoring OpenCode or depending on it as the engine is an architecture option only if we explicitly choose “thin wrapper” — that would collapse standalone into the adapter. Default: **independent engine**.

### `ui_design_expectations`

Vision.md: **CLI-first**, slash-command names, ASCII diagnostics, reason codes. v1 = terminal:

- `itsm` (name TBD) `auto` | `intake` | `execute` | …
- Role/session visible in the prompt (which role, which model, which phase).
- Approval prompts for `ask` permissions.

No requirement for a VS Code lookalike in v1. Optional TUI (OpenCode-like) is a later slice, not the first vertical.

### `security_compliance`

- API keys: OS user store or env / gitignored local config; **never** commit; **never** log (**US-0085**).
- No vendor slugs in *kit* templates; runtime local config is gitignored (same **US-0102** volatile-ID idea).
- Path-scoped write permissions per role.
- Bash allowlists/denylists in code (replacement for **US-0005** hooks).
- The runtime does not proxy operator traffic through our servers in v1 (BYOK only).
- Optional `/security-review` phase remains a **role + artifacts**, not a new compliance product.

### `non_functional_priorities`

1. **Correct isolation and permissions** (wrong host = the original bug).
2. **Multi-provider reliability** (including OpenAI-compatible Chinese APIs).
3. **Fail-closed diagnostics** (reason codes; no silent PASS).
4. **Kernel compatibility** (same validators as Cursor/OpenCode paths).
5. TUI polish, IDE, sovereign-loop parity — after v1.

### `scope_timeline`

- **v0 (spike, not a release):** one role, one provider, isolated session, one validator call. Proves the harness, not the product.
- **v1 program:** CLI + session isolation + permission engine + N providers + 7 roles + spawn-only `/auto` + validator bridge + docs. Enough to run intake→execute→qa on a sample repo **without Cursor and without OpenCode**.
- **v1 out of scope:** IDE extension, full sovereign loop (**US-0103–US-0110**), Caveman, Cursor browser UAT, installer npm/choco/brew for the *runtime* as mature as **US-0009** (can ship a single-platform binary first).
- **Timeline:** not dated. **Do not** start standalone in parallel with the adapter unless the adapter is blocked on spawn isolation. Suggested order: adapter v1 in this repo → standalone v0 spike in new repo → standalone v1.

---

## Target architecture (for `/research` / `/architecture`, not locked)

```
operator
  └─ its-magic-runtime CLI
        ├─ config: providers[], roles[], permissions[]
        ├─ orchestrator (no file edits)
        │     └─ spawn session(role, model, phase)
        ├─ session N (fresh)
        │     ├─ tools: read/edit/bash/grep  [permission gated]
        │     └─ writes kernel artifacts in project/
        └─ python scripts/*_validate.py     [fail-closed]

project worktree
  └─ docs/, sprints/, handoffs/, decisions/, scripts/   [kit kernel]
```

**Models:** many providers connected **at once**; **one model per session/request**; different roles ⇒ different APIs. Same as the adapter capability target, implemented in *our* router.

**US-0095** is irrelevant (no Cursor Task loop). **US-0092** stop/ledger semantics should be preserved so CI and operators keep the same exit codes where possible.

---

## Role matrix (v1)

Same intent as the adapter brief; enforcement is **our** permission engine.

| Role | Session | Write glob (intent) | Model tier |
|------|---------|---------------------|------------|
| Orchestrator | primary, no `edit` | none | cheap |
| `po` | fresh | `docs/product/**`, `handoffs/po_to_tl.md` | balanced |
| `tech-lead` | fresh | `docs/engineering/**`, `decisions/**`, `sprints/**`, TL handoffs | strong |
| `dev` | fresh | code + sprint summary + `handoffs/dev_to_qa.md` | strong |
| `qa` | fresh | `sprints/**`, QA handoffs | strong |
| `release` | fresh | release artifacts; publish via existing scripts only | balanced |
| `curator` | fresh | compaction paths only | cheap |
| `security` | fresh | findings-only or narrow | strong |

---

## Drop / do not port

**Cursor tax (do not rebuild):**

- **US-0002** / **US-0004** as enforcement.
- **US-0005** Cursor `hooks.json`.
- **US-0095** / **BUG-0012** in-Cursor auto-chain.
- **US-0101** `fast`/`inherit` aliases as runtime.
- **US-0089** / **US-0090** / **BUG-0011** Caveman.
- Cursor browser UAT as primary.
- Active vs `template/.cursor` parity as a runtime concern.
- Fifty full command markdown files.

**Do not rebuild in the runtime repo:**

- Intake evidence validators, bug routing, triad hot-surface, README feature coverage — **call the kit**.
- npm/Chocolatey/Homebrew *kit* distribution (**US-0009**) — stays in this repo.
- A second copy of `docs/product/backlog.md` history.

**Keep as contracts to *satisfy*, not files to copy:** **US-0001** phase names and outputs; **US-0003** roles; **US-0006** artifacts; **US-0023** isolation; **US-0069** matrix; **US-0045** status; **US-0081** if the *runtime repo* has its own intake; **US-0092** loop/exit semantics.

---

## Plan-area inventory (US-0081 / DEC-0064)

Stable ids. Each row → `story_ids[]` **xor** `deferred_ref`.

| `plan_area_id` | v1 mapping intent | Defer? |
|----------------|-------------------|--------|
| `sibling-repo-bootstrap` | New repo, license MIT, README, CI smoke | No — story 1 (runtime repo) |
| `kernel-consume-contract` | How runtime finds project root, invokes kit Python, version skew policy | No — story 1 or kit-side tiny story |
| `session-isolation` | Fresh session per phase; no chat carry; isolation evidence analogue **US-0048** | No — story 2 |
| `tool-permission-engine` | Path globs, bash policy, ask/allow/deny, audit log | No — story 2 |
| `provider-router` | N keys; OpenAI-compatible; DeepSeek/Moonshot/Z.AI/MiniMax/Anthropic/custom `baseURL` | No — story 3 |
| `role-runtime` | Seven roles + orchestrator config; models per role | No — story 3 |
| `orchestrator-auto` | Spawn-only `/auto`; **US-0069**; stop matrix; **US-0092** exit codes | No — story 4 |
| `cli-surface` | Commands as argv/slash; reason codes on stderr | No — story 4 or 5 |
| `validator-bridge` | Fail-closed subprocess; do not reimplement | No — story 5 |
| `docs-operator-guide` | How to run without Cursor; key storage; role models | No — story 6 |
| `tui` | OpenCode-like terminal UI | **`deferred_ref`**: after CLI v1 |
| `ide-client` | VS Code/OpenCode-style IDE | **`deferred_ref`**: client of the CLI/server |
| `sovereign-loop` | US-0103–US-0110 | **`deferred_ref`**: after spawn+validators |
| `opencode-adapter` | Host pack in *this* kit | **`deferred_ref`**: other program (`opencode-adapter-masterplan.md`) |
| `opencode-fork` | Distro of OpenCode | **`deferred_ref`**: rejected as product; spike only if isolation blocked |
| `in-kit-engine` | Build runtime inside `gsd_cursor` | **`deferred_ref`**: rejected |
| `vscode-ps-host` | VS Code + PowerShell as agent host | **`deferred_ref`**: rejected |
| `kit-installer-parity` | Triple installer for the *runtime* binary | **`deferred_ref`**: single binary first |
| `caveman-voice` | Terse voice | **`deferred_ref`**: optional later |

---

## Suggested story slices (unassigned IDs)

For the **runtime repo** backlog. Kit repo gets at most the consume-contract story.

1. **Repo + hello harness** — spawn one isolated session, one model, edit one file under a glob, refuse out-of-glob writes.
2. **Permissions + isolation evidence** — analogue of **US-0048** tuple; fail closed if orchestrator writes.
3. **Provider router + roles** — multi-key; per-role model; Chinese OpenAI-compatible documented.
4. **Orchestrator `/auto`** — phase matrix; fresh spawn; stop reasons; optional call into `auto_outer_driver` semantics.
5. **Validator bridge** — intake/release gates via kit Python; same reason-code families.
6. **CLI + operator docs** — non-interactive CI mode; key handling; “not Cursor” runbook.

**Definition of done for the program:** an operator with only the runtime CLI + kit-installed project + BYOK keys can complete a story lifecycle **without Cursor and without OpenCode**, with PO/Dev/QA as **separate sessions and optionally separate APIs**, and with validators blocking the same classes of error as today.

**Not done:** a demo that switches system prompts in one process and calls bash.

---

## Risks

| Risk | Mitigation |
|------|------------|
| Underestimating the harness (“autoflow is already Python”) | v0 spike gated: no product intake of engine stories until isolation+permissions exist |
| Duplicate kernel / drifted validators | Consume kit scripts; pin kit version; no copy-paste of validators |
| Building a worse OpenCode | Prefer adapter until spawn isolation *fails* on stock OpenCode; standalone then has a proven gap |
| Two backlogs, two products, no users | Sequence: adapter in this repo first |
| Provider tool-calling gaps (some Chinese models) | Permission engine still holds; document model fitness; default strong roles to a tool-reliable slug |
| Scope: TUI/IDE/sovereign | Inventory deferrals |
| Intake in the wrong repo | PO uses [Intake location](#standalone-its-magic-runtime--master-plan-pre-intake) |

---

## Explicit non-goals (v1)

- Implementing the engine inside this kit repo.
- Forking OpenCode as the named product.
- VS Code plugin that only runs PowerShell.
- Cloning all historical **US-xxxx** into the new backlog.
- Feature parity with Cursor-native chain, Caveman, or sovereign loop on day one.
- Replacing the kit’s Python validators with prompt-only checks.

---

## Operator checklist before `/intake`

Confirm or correct in the intake chat:

- [x] Runtime lives in a **new repo**, not `gsd_cursor`.
- [x] Kernel stays in **this** repo; runtime **calls** it.
- [x] Layer 1 is **our code** (sessions, permissions, spawn, providers).
- [x] Multi-provider / Chinese APIs required as capability.
- [x] Not a 1:1 story clone; Cursor tax dropped.
- [x] OpenCode adapter is a **separate** program (sibling masterplan).
- [ ] Working name of the sibling repo / CLI — **lock in intake**.
- [ ] Implementation language (TS/Go/Python) — **research**, not this brief.
- [ ] Start standalone **after** adapter vs **in parallel** — **lock in intake** (recommendation: after, unless adapter blocked).

---

## Next command

If the sibling repo **does not exist yet:** do **not** dump engine tasks into this kit’s backlog. Either:

- **`/intake`** here a **single** bounded story: “publish kernel consume contract / bootstrap sibling repo,” with remaining plan areas `deferred_ref`, **or**
- Create the empty sibling repo, copy this brief, then **`/intake`** there.

If the sibling repo **exists:** **`/intake`** (PO, fresh) with this file, then **`/discovery`** / **`/research`** (session isolation + provider SDK + kit invoke), then **`/architecture`** (companion DEC: owned harness, consume kernel, no in-kit engine, no command-file enforcement).
