# OpenCode host adapter — master plan (pre-intake)

**Status:** draft idea pack (not a backlog story yet).  
**Intent:** operator source document for a later **`/intake`** (first/new/broad).  
**Repo decision:** implement the adapter **in this repository**. Do **not** put a standalone agent runtime in this repo.  
**Related:** standalone runtime (new repo) — `docs/product/standalone-runtime-masterplan.md`.  
**Pack hint for PO:** `first-intake-pack` (**US-0068** / **DEC-0050**). Complete-plan mapping required (**US-0081** / **DEC-0064**).

This file is the operator brief. It is not architecture lock, not a DEC, and not an assigned **US-xxxx**. Intake must allocate IDs, write backlog/acceptance, and produce `handoffs/intake_evidence/*.json`. Do not treat headings below as already-shipped contracts.

---

## How to intake this

1. Run **`/intake`** in a fresh **PO** subagent (**BUG-0006**).
2. Point the PO at this file as the idea source (`docs/product/opencode-adapter-masterplan.md`).
3. Use **`first-intake-pack`**. Map every **plan area** in [Plan-area inventory](#plan-area-inventory-us-0081--dec-0064) to a candidate story or an explicit `deferred_ref`.
4. Do **not** clone US-0001–US-0119 one-for-one. Cursor-tax work is listed under [Drop / do not port](#drop--do-not-port-cursor-tax).
5. Persistence must include `plan_area_inventory`, `plan_area_coverage`, `coverage_complete=true`, or fail closed (`INTAKE_PLAN_COVERAGE_MISSING` under `INTAKE_PERSISTENCE_BLOCKED`).

---

## One-sentence product

Ship **its-magic as a second host pack for stock OpenCode**: same artifact kernel and Python fail-closed gates, with role behavior and `/auto` spawn enforced by **OpenCode permissions + a plugin**, not by Cursor rules/skills/commands hoping the model obeys.

---

## Why (problem)

Cursor is the current host (**vision.md** audience; **US-0001** commands, **US-0002** rules, **US-0003** agents, **US-0005** hooks). That host is a ceiling:

| Pain | Evidence in this kit |
|------|----------------------|
| Rules/skills are advisory | **R-0001**: prompt isolation is not a boundary. **US-0023** / **BUG-0006**: one chat playing every role is forbidden for a reason. |
| Own API keys do not really apply to subagents | **US-0101** / **DEC-0086**: BYOK keys/base URLs are **not** inherited by Cursor subagents. |
| Per-role models are aliases, not vendors | **DEC-0086** `fast` / `inherit` / omit. **US-0102** / **DEC-0087** already asked for real slugs. |
| Native `/auto` is Cursor Task-loop specific | **US-0095** / **DEC-0080**; fallback is already host-agnostic **US-0092** / `scripts/auto_outer_driver.py`. |

Operator goal (this thread): Cursor-independent its-magic; **maximum control** over agents/subagents; **own APIs** (including Chinese providers); **hardcoded** behavior rather than rules files; adapter **in this repo**; standalone runtime **later, other repo**.

Rejected approaches (already argued; do not re-open in v1):

- Convert every function into a VS Code plugin that shells PowerShell.
- Fork OpenCode and implement the kit inside the fork.
- Rebuild OpenCode (TUI, providers, tool loop) inside this repo.
- 1:1 clone of all historical stories including Cursor-taming work.

---

## Design principle — enforce in the host, not in prose

Split every behavior into one of three layers. **Prefer 1, then 2, then 3.**

### Layer 1 — Host-enforced (must be the majority of v1)

These cannot be “forgotten” by the model:

- OpenCode **permissions** per role (`allow` / `ask` / `deny` on `edit`, `bash`, `task`, …).
- OpenCode **plugin** hooks: intercept tool calls, refuse illegal phase work, Task-spawn the **US-0069** role, call Python validators, write isolation evidence.
- Existing **Python validators** and reason codes (unchanged kernel).
- **US-0092** outer-driver state machine (spawn-only loop, stop matrix, ledgers).

### Layer 2 — Agent system prompts (short, role-only)

OpenCode `.opencode/agents/*.md` (or `opencode.json` `agent`) hold **who you are** and **which artifacts you may write**. They are still LLM text. Keep them short. Do **not** dump `.cursor/commands/*.md` into agent prompts.

### Layer 3 — Commands (thin dispatch only)

OpenCode commands (`.opencode/commands/*.md`) may exist as **named entry points** (`/intake`, `/execute`, `/auto`) that:

- select the role agent,
- pass a **short** phase id + artifact path list,
- then **stop**.

They must **not** contain the 200-line Cursor command bodies. If a rule can be a plugin check or a Python CLI, it must not live in a command file.

**Success test:** a model that ignores its prompt still cannot (a) skip spawn isolation, (b) run `/release` after a failing validator, (c) let PO `write` production code if `edit` is `deny`, (d) continue `/auto` without the next role’s fresh session.

---

## In this repo vs not

| Work | Where |
|------|--------|
| OpenCode adapter (template pack, installer, plugin, docs, tests) | **This repo** |
| Keep Cursor pack working | **This repo** (compose, do not delete `.cursor/` in v1) |
| Standalone its-magic agent runtime (own TUI/providers/tool loop) | **New repo, later** — only if plugin APIs cannot enforce **BUG-0006** |
| OpenCode fork | **Out of scope** unless a thin patch is the only way to spawn isolated child sessions |

Installer already copies a kit into consumer repos (**US-0008**). The adapter is another **template tree** (`template/.opencode/`) plus an install mode, analogous to `.cursor/`. Framework metadata stays under **DEC-0045** `its_magic/` in consumer repos; do not dump a desktop app into `its_magic/`.

---

## First-intake topic answers (US-0068)

Distinct answers for PO `topic_coverage` (do not echo one blob onto every key — **BUG-0007**).

### `users_problem`

Operators who want its-magic’s artifact workflow (intake → execute → QA → release) **without** Cursor’s soft rules, BYOK-subagent ceiling, and alias-only models. They need real subagents, own provider keys (including Chinese APIs), and behavior that is enforced by the host.

### `runtime_target_environment`

- **Authoring / CI:** this git repo (Windows + POSIX already supported by installers).
- **Operator runtime:** **stock OpenCode** (TUI / desktop / IDE extension) on the operator machine; **not** a vendored OpenCode binary.
- **Consumer repos:** `its-magic` installer copies `.opencode/` (and optionally still `.cursor/`) into the target project.
- **Headless:** reuse **US-0092** `--invoke-cmd` pointed at OpenCode’s non-interactive/session API when native in-session chain is unavailable (`NATIVE_CHAIN_UNAVAILABLE` analogue).

### `language_framework_runtime`

- Kernel stays **Python 3** validators + existing scripts.
- Adapter plugin is **OpenCode plugin TypeScript/JavaScript** (`@opencode-ai/plugin` or current v1/v2 plugin API).
- Agent/command files are **markdown + JSON** under `.opencode/`.
- No new mandatory npm runtime inside consumer *application* code. Plugin loads from the kit’s template or `its_magic/`-owned adapter folder as architecture will lock.

### `architecture_preference`

**Host-adapter on unmodified OpenCode** (approach A):

- Kernel = artifacts + validators + `auto_outer_driver.py` + phase→role matrix (**US-0069**).
- Host pack = `.opencode/agents`, thin commands, **one orchestrator plugin**.
- Cursor pack remains; OpenCode is additive.
- Per-role `model: provider/slug` implements **US-0101** / **US-0102** without Cursor aliases.

Rejected for v1: OpenCode fork; greenfield runtime in this repo; VS Code+shell rewrite.

### `ui_design_expectations`

No new its-magic GUI in v1. Operators use **OpenCode’s** TUI/desktop/IDE. Kit UX stays **slash-command names** + ASCII/CLI diagnostics (reason codes). Optional later: OpenCode custom command palette labels only.

### `security_compliance`

- Never read `.env` for secrets in plugin logs (**US-0085** posture).
- Provider keys stay in OpenCode’s credential store (`/connect` / `auth.json`), not in git, not in scratchpad vendor slugs in `template/` (**US-0102** volatile-ID rule).
- Plugin must not print API keys.
- Permission deny-lists are the security control for role tools.
- Chinese and Western providers are **operator-chosen**; the kit does not proxy traffic.
- Existing security-review phase (**US-0028** family) stays optional/zero-overhead when disabled.

### `non_functional_priorities`

1. **Enforceability** (spawn, permissions, validators) over prompt completeness.
2. **Cursor coexistence** (no regression of current installer/Cursor path).
3. **Deterministic diagnostics** (reason codes, fail-closed).
4. **Parity** (`template/` vs active; extend `check_intake_template_parity` scopes rather than a third copy-by-hand).
5. Performance/TUI polish are OpenCode’s problem, not v1 kit work.

### `scope_timeline`

- **v1 (this program):** OpenCode adapter in this repo — install pack, 7 roles as agents with permissions, thin commands, orchestrator plugin that Task-spawns + calls validators, per-role models, docs/runbook, contract tests.
- **v1 out of scope:** standalone runtime, OpenCode fork, VS Code contrib rewrite, porting Caveman/native-chain/Cursor browser as primary, full sovereign-loop feature parity on day one.
- **Timeline:** not dated; deliver as **one epic with sliced stories** (see below), not one mega-story. Suggested first vertical slice: install empty `.opencode/` pack + one role (`po`) + plugin that refuses in-process phase work (spawn-only probe) + one validator CLI call.

---

## Target architecture (for `/research` / `/architecture`, not locked)

```
operator
   └─ stock OpenCode
         ├─ .opencode/agents/*.md     role + permissions + model slug
         ├─ .opencode/commands/*.md   thin dispatch (optional)
         └─ plugin (orchestrator)
               ├─ US-0069 resolve phase → role
               ├─ Task/session spawn (BUG-0006)
               ├─ subprocess: python scripts/*_validate.py
               ├─ US-0092 loop / stop matrix / ledgers
               └─ fail-closed reason codes
         │
         └─ repo kernel (unchanged ownership)
               docs/product, docs/engineering, sprints/, handoffs/, decisions/
```

**US-0095** native Cursor chain is **not** ported. On OpenCode, the plugin **is** the native chain. **US-0092** remains headless/CI fallback.

**US-0101 / US-0102 mapping:**

| Cursor today | OpenCode adapter |
|--------------|------------------|
| `model: fast` / `inherit` / omit | `model: deepseek/…`, `moonshot/…`, `zai/…`, `anthropic/…` |
| BYOK broken on subagents | OpenCode `/connect` keys; each agent uses its provider |
| `MODEL_<PHASE>` scratchpad | plugin reads scratchpad **or** agent frontmatter; architecture must pick one source of truth |

Multiple providers at once (DeepSeek, Moonshot, MiniMax, Z.AI/GLM, plus OpenAI-compatible `baseURL` for DashScope/Qwen) are an OpenCode host capability; the adapter only **assigns** them per role.

---

## Role matrix (v1)

Map **US-0003** (+ security) to OpenCode agents. Permissions are illustrative; architecture locks the table.

| Role | Mode | Tools (intent) | Model (intent) |
|------|------|----------------|----------------|
| Orchestrator (`auto`) | primary | no `edit`; `task` allow for role agents only | cheap |
| `po` | subagent | `edit` allow only under `docs/product/**`, `handoffs/po_to_tl.md`; `bash` ask | balanced |
| `tech-lead` | subagent | `edit` allow `docs/engineering/**`, `decisions/**`, `sprints/**`, handoffs | strong |
| `dev` | subagent | `edit` + `bash` allow (existing deny-lists still apply via plugin + **US-0005**-equivalent) | strong |
| `qa` | subagent | `edit` allow `sprints/**`, `handoffs/**`; `bash` allow validators | strong |
| `release` | subagent | `edit` allow release artifacts; publish gated by plugin + existing scripts | balanced |
| `curator` | subagent | `edit` allow state/decisions compaction paths only | cheap |
| `security` | subagent | `edit` deny or findings-only | strong |

Plugin **must** reject orchestrator (or any role) performing another role’s writes in-session (**AUTO_ORCHESTRATOR_PHASE_EXECUTION** / **BUG-0006**).

---

## Drop / do not port (Cursor tax)

Do not create adapter work items whose only job was taming Cursor:

- **US-0002** / **US-0004** as the *enforcement* mechanism (keep kernel docs; do not rely on `.mdc` / Cursor skills).
- **US-0005** Cursor hook JSON as-is (replace with OpenCode plugin + permissions).
- **US-0095** / **BUG-0012** Cursor Task auto-chain prose and IDE-primary drain recipes.
- **US-0101** Cursor-only aliases (`fast`/`inherit`) as the *runtime* mapping (keep tier *names* if useful; resolve to OpenCode slugs).
- **US-0089** / **US-0090** / **BUG-0011** Caveman.
- Cursor browser as **primary** UAT (**UAT_BROWSER_PROBE_MODE=cursor**). HTTP/script probes can stay.
- Triple-copy of 50 full command files into `.opencode/commands/`.

**Keep and compose (kernel):** **US-0001** phase *names* and artifact outputs; **US-0003** roles; **US-0006** artifacts; **US-0023** / **US-0048** / **BUG-0006** isolation; **US-0069** phase→role; **US-0045** status; **US-0081** intake coverage; **US-0092** outer driver; Python validators; installer ownership (**DEC-0045**).

---

## Plan-area inventory (US-0081 / DEC-0064)

Stable ids for intake coverage. Each row must map to `story_ids[]` **xor** `deferred_ref`.

| `plan_area_id` | v1 mapping intent | Defer? |
|----------------|-------------------|--------|
| `opencode-template-pack` | `template/.opencode/**` layout, examples, gitignore for local models/keys | No — story 1 |
| `installer-host-mode` | Install/upgrade/clean for `.opencode/` without breaking `.cursor/` (**US-0008** compose) | No — story 1 or 2 |
| `role-agents-permissions` | Seven roles + orchestrator as OpenCode agents; permission table | No — story 2 |
| `model-slug-routing` | Per-role/per-phase slugs; multi-provider; no vendor IDs in `template/` (**US-0102** rule) | No — story 3 |
| `orchestrator-plugin-spawn` | Plugin spawn-only `/auto`; **US-0069**; isolation evidence; stop matrix | No — story 4 |
| `validator-bridge` | Plugin/CLI invokes existing Python validators; fail-closed; no reimplementation | No — story 4 or 5 |
| `thin-commands` | Optional named commands as dispatch-only (no Cursor command clones) | No — story 5 |
| `docs-runbook-parity` | Runbook + README (user-visible, no leaked DEC in operator sentences per sanitization) + contract tests + parity scopes | No — story 6 |
| `cursor-coexistence` | Cursor path remains default or documented dual-host; no forced migration | Covered by installer + docs stories |
| `headless-invoke-cmd` | Wire **US-0092** `--invoke-cmd` to OpenCode | May slice with story 4 or defer with reason if session CLI unstable |
| `sovereign-loop-on-opencode` | US-0103–US-0110 on OpenCode | **`deferred_ref`**: after v1 spawn+validators work |
| `standalone-runtime` | Own TUI/providers | **`deferred_ref`**: other repository |
| `opencode-fork` | Private OpenCode distro | **`deferred_ref`**: only if spawn isolation impossible on stock OpenCode |
| `vscode-shell-port` | VS Code plugin wrapping ps1 | **`deferred_ref`**: rejected for this program |
| `caveman-voice-port` | Caveman on OpenCode | **`deferred_ref`**: Cursor-tax / optional later |
| `cursor-browser-uat` | Cursor MCP browser probes | **`deferred_ref`**: host-specific |

Intake may merge 1+2 or 4+5 into fewer stories if **US-0051** decomposition says so, but **must not drop an inventory row without `deferred_ref`**.

---

## Suggested story slices (unassigned IDs)

Names for decomposition; PO assigns **US-xxxx**.

1. **Pack + installer** — empty-but-valid `.opencode/` tree; install/upgrade/clean; `--host cursor|opencode|both`; parity tests.
2. **Role agents** — markdown agents + permission table; no orchestrator yet; manual `@po` / Task from operator.
3. **Model routing** — scratchpad or local catalog → agent `model`; examples for DeepSeek / Moonshot / Z.AI / Anthropic; fail-closed unknown slug.
4. **Orchestrator plugin** — spawn-only; cannot write phase artifacts itself; isolation evidence; maps to **US-0092** stop reasons.
5. **Thin commands + validator bridge** — `/intake` etc. set agent + call plugin; Python CLIs remain source of hard gates.
6. **Docs + contract tests** — runbook “OpenCode host”; reason codes `OPENCODE_*` / reuse `NATIVE_CHAIN_UNAVAILABLE`; `test_usXXXX_*`.

**Definition of done for the program (not one story):** an operator with stock OpenCode and `/connect`ed keys can run intake→…→release on a fresh install **without Cursor**, with PO/Dev/QA as **different sessions and optionally different providers**, and with validators blocking persistence the same as today.

---

## Risks

| Risk | Mitigation |
|------|------------|
| OpenCode plugin API cannot spawn isolated child sessions (V2 command `subtask` ignored) | Fail closed with a new/analogue reason code; use session/Task client API; if impossible, **thin fork** or stop — do not silently same-session roleplay (**R-0001**) |
| Dual-host parity cost (`.cursor` + `.opencode`) | Thin commands; do not duplicate 50 files; plugin owns behavior |
| Template drift | New `--scope=opencode-adapter` on existing parity script |
| Operators expect a VS Code-looking product | Docs: UI is OpenCode; kit is the workflow |
| Scope creep into sovereign loop / standalone runtime | Inventory deferrals above |
| Chinese API tool-calling quality | Document as operator model choice; QA/dev default to a tool-reliable slug |

---

## Explicit non-goals (v1)

- Rewriting its-magic as a VS Code extension.
- Forking OpenCode as the product.
- Implementing a new LLM tool loop in Python “because autoflow looks small” (`auto_outer_driver.py` does not call models).
- Porting all Cursor rules into OpenCode `instructions` (that repeats the failure mode).
- Deleting the Cursor kit in the same program.

---

## Operator checklist before `/intake`

Confirm or correct in the intake chat (needed if PO must not assume):

- [x] Adapter lives **in this repo**.
- [x] Standalone runtime is **not** this program.
- [x] Prefer **plugin + permissions + Python** over command/rule prose.
- [x] Multi-provider / Chinese APIs are **required** as a capability (assignment per role), not a kit-operated proxy.
- [x] Cursor pack **stays**.
- [ ] Default install host: `cursor` only until opt-in, vs `both` on fresh OpenCode-first installs — **lock in intake**.
- [ ] Plugin language lock (OpenCode v1 vs v2 plugin API) — **research**.

---

## Next command

**`/intake`** (PO, fresh subagent) with this file as the idea. After persistence: **`/discovery`** then **`/research`** (OpenCode plugin spawn + installer ownership), then **`/architecture`** (companion DEC: host-adapter, no fork, enforce-in-plugin).
