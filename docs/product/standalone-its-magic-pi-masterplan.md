# Standalone its-magic Agent on Pi — Master Plan

**Status:** implementation-oriented pre-intake / research source document  
**Date:** 2026-09-05  
**Product direction:** build a **standalone its-magic coding-agent runtime** in a new repository, with **Pi embedded through its TypeScript SDK as a replaceable agent kernel**.  
**Source framework snapshot:** current `vision.md`, `acceptance.md`, and `backlog.md` supplied by the operator, including the lifecycle, full-autonomy, browser-UAT, model-routing, sovereign-loop, OpenCode-adapter, convergence, closure, and critic-model work through **US-0130**.  
**Prior plan relationship:** supersedes/refines `standalone-runtime-masterplan.md` and `pi-sdk-owned-runtime-masterplan.md` for the standalone product. The existing Cursor and OpenCode hosts remain compatibility paths, not the primary runtime.

---

## 0. Executive decision

Build **its-magic-agent** (working name) as an owned runtime with this boundary:

> **its-magic owns the product and all correctness-critical behavior. Pi supplies the LLM agent loop, model/provider/auth plumbing, streaming, and session primitives.**

The product is **not**:

- a Pi extension pack whose behavior depends on markdown prompts,
- a wrapper around the Pi CLI,
- an OpenCode fork,
- a clone of Cursor's Agent panel,
- a rewrite of the existing its-magic Python validators,
- a second copy of the current 130-story backlog.

The product **is**:

- an owned orchestrator,
- an owned role/phase runtime,
- an owned tool and permission broker,
- an owned context and code-intelligence layer,
- an owned app/process runtime,
- an owned browser/UAT runtime,
- an owned audit/evidence layer,
- an owned CLI/TUI/control API,
- using Pi behind a narrow `AgentKernel` adapter.

### Recommended technology split

| Area | Technology | Why |
|---|---|---|
| Runtime/orchestrator | TypeScript on Node/Bun | Pi SDK is TypeScript; easiest integration and event streaming |
| Agent kernel | `@earendil-works/pi-coding-agent` + `pi-ai` | Avoid rebuilding model streaming/tool loop/session plumbing |
| Existing workflow kernel | Current Python scripts/validators | Already shipped and heavily contract-tested |
| Code intelligence v1 | AFT Rust backend behind our adapter | Warm indexed search, semantic search, Tree-sitter, LSP, call graph |
| Code intelligence later | optional own Rust `its-indexd` | Full sovereignty if AFT becomes limiting |
| Browser/UAT | Playwright + optional Chrome CDP backend | Reproducible isolated CI plus real logged-in developer-browser mode |
| Process/runtime | Node child-process + pluggable local/Docker/SSH/WSL backend | App launch, logs, health, restart, remote execution |
| Persistent runtime metadata | SQLite initially | Sessions/runs/tool audit/cache metadata; repo artifacts stay canonical project memory |
| Project memory | existing repo artifacts | Preserve artifact-first design; chat/session is not source of truth |

---

## 1. Product statement

Ship a **standalone autonomous software-development agent** that can take an idea or bug from intake through closure, using real isolated specialist agents, multiple AI providers including Codex OAuth, a Cursor-like code intelligence layer, automatic application launch, browser-based UAT, deterministic quality gates, and the complete its-magic artifact memory model.

One operator command should be able to run:

```text
idea / bug
   ↓
intake
   ↓
discovery
   ↓
research
   ↓
architecture
   ↓
sprint-plan
   ↓
plan-verify
   ↓
execute
   ↓
qa
   ↓
verify-work / browser UAT
   ↓
release
   ↓
closure
   ↓
refresh-context
```

with delivery-mode compression where the existing framework allows it.

The central promise remains the original its-magic promise:

> **The repository is the durable memory. Agents are disposable workers.**

---

## 2. What the current its-magic framework already solved

Do not redesign these problems from first principles. They are mature product contracts to **consume, enforce, or host-port**.

### 2.1 Artifact-first project memory

Keep:

- `docs/product/vision.md`
- `docs/product/backlog.md`
- `docs/product/acceptance.md`
- `docs/engineering/architecture.md`
- `docs/engineering/decisions.md`
- `docs/engineering/research.md`
- `docs/engineering/state.md`
- archive/hot-surface behavior
- `decisions/DEC-xxxx.md`
- `sprints/**`
- `handoffs/**`
- release queue/release notes
- traceability and evidence artifacts
- `work/US-xxxx/pack.json` and active-context behavior where delivery mode uses them
- sovereign memory and decision ledgers

Pi session history must **never** become an alternative canonical project memory.

### 2.2 Deterministic lifecycle

The current framework has a defined lifecycle and later added:

- strict phase→role routing,
- fresh subagent context per phase,
- strict runtime proof,
- configurable phase selection,
- full-autonomy drain,
- bulk execution,
- delivery modes,
- work-kind routing,
- autonomy presets,
- explicit closure after release.

These become **runtime state-machine behavior**, not prompt instructions.

### 2.3 Quality and release contracts

Preserve the existing meaning of:

- check-in tests,
- QA evidence,
- UAT evidence,
- release gate ordering,
- README/runbook/project-doc integrity,
- release queue,
- changelog/version release docs,
- backlog/acceptance/state reconciliation,
- closure verification,
- decision gates,
- fail-closed reason codes.

### 2.4 Runtime QA and application operation

The framework already contains contracts for:

- stack-aware app startup,
- health/connectivity checks,
- log inspection,
- bounded debug retries,
- generated test scaffolding,
- local/Docker/remote execution,
- dev-environment auto-launch,
- browser UAT,
- console/network evidence.

The standalone runtime should provide the **actual host implementation** for these contracts.

### 2.5 Multi-model and sovereign features

Preserve semantics for:

- model tiers and direct model slugs,
- role-based model catalogs,
- operator-pinned critic model,
- cross-model adversarial critic,
- AI decision ledger / plan fidelity,
- sovereign memory,
- role-behavior manifest,
- sovereign-loop generation/deferrals,
- parallel DEV instances/worktrees,
- self-healing deploy,
- goal convergence,
- convergence critic/smoke fixes.

The standalone runtime is a better place to enforce these than Cursor rules or host prompts.

---

## 3. Host-specific features: keep semantics, replace implementation

### 3.1 Cursor-specific mechanisms to remove from the standalone runtime

Do not make these runtime dependencies:

- `.cursor/commands/*.md` as workflow engine,
- `.mdc` rules as enforcement,
- Cursor hooks as security boundary,
- Cursor Task native auto-chain,
- Cursor model aliases such as `fast` / `inherit`,
- Cursor browser MCP as primary UAT backend,
- Cursor Agent-panel availability as role capability,
- Cursor scratchpad markdown parsing as the long-term config mechanism.

They remain in the existing kit for Cursor compatibility.

### 3.2 OpenCode-specific mechanisms to keep only as compatibility host

The shipped US-0121..US-0126 OpenCode path is useful and should remain supported, but the standalone agent must not depend on:

- `.opencode/agents`,
- OpenCode permissions,
- OpenCode task/subtask APIs,
- OpenCode plugin lifecycle,
- `/connect` as the only credential mechanism.

### 3.3 Standalone replacements

| Existing host mechanism | Standalone implementation |
|---|---|
| Cursor/OpenCode subagent | owned `SessionSupervisor` creates Pi SDK session |
| Cursor/OpenCode permission | owned `PolicyEngine` + `ToolBroker` |
| Cursor native auto-chain | owned `WorkflowEngine` |
| outer-driver shell invocation | owned scheduler; existing stop-matrix semantics preserved |
| Cursor browser | owned `BrowserRuntime` |
| `.cursor/dev-environment.json` | typed runtime profile + legacy adapter |
| scratchpad flags | typed `RuntimeConfig`; legacy scratchpad compatibility reader |
| model alias | `ModelRouter` → real Pi `provider/model` |
| `@browser` / agent panel | `itsm browser ...` + QA-owned tools |
| manual isolation marker | runtime-generated attestation bound to real Pi session id |
| map-codebase only | persistent `CodeIntelligence` + derived codebase map |

---

## 4. Why Pi is the right kernel candidate

Current Pi capabilities relevant to this design:

- programmatic `createAgentSession()` SDK,
- explicit `SessionManager` creation/open/continue APIs,
- model runtime with provider discovery,
- stored API-key and OAuth credentials,
- built-in ChatGPT Plus/Pro Codex subscription login,
- custom providers and custom OAuth providers,
- custom tools,
- disabling built-in tools while keeping custom tools,
- custom resource loading/system prompts,
- streaming lifecycle/tool events,
- interactive and RPC modes,
- MIT license,
- example subagent implementation proving isolated separate contexts are viable.

### Architectural caveat

Pi deliberately has **no built-in sandbox/permission boundary**. This is acceptable only because the standalone runtime will **not expose raw Pi tools**. OS-level isolation remains a separate execution-backend concern.

---

## 5. North-star architecture

```text
┌───────────────────────────────────────────────────────────────────────┐
│                         Operator surfaces                             │
│                                                                       │
│ CLI/TUI     JSON-RPC/daemon     later Web/Android/Watch/IDE client   │
└───────────────────────────────┬───────────────────────────────────────┘
                                │
                                ▼
┌───────────────────────────────────────────────────────────────────────┐
│                     its-magic-agent runtime                           │
│                         OWNED PRODUCT                                 │
│                                                                       │
│  ┌────────────────┐   ┌────────────────────┐   ┌──────────────────┐  │
│  │ Command Router │──▶│ Workflow Engine    │──▶│ Run State Store  │  │
│  │ /auto /ask ... │   │ phases / stop /    │   │ SQLite + repo    │  │
│  └────────────────┘   │ retry / drain      │   └──────────────────┘  │
│                       └──────────┬─────────┘                         │
│                                  │                                   │
│             ┌────────────────────┼───────────────────────┐           │
│             ▼                    ▼                       ▼           │
│    ┌─────────────────┐  ┌─────────────────┐   ┌──────────────────┐  │
│    │ Role/Session    │  │ Context Engine  │   │ Gate Engine      │  │
│    │ Supervisor      │  │ artifacts+index │   │ validator bridge │  │
│    └───────┬─────────┘  └────────┬────────┘   └────────┬─────────┘  │
│            │                     │                     │            │
│            ▼                     ▼                     ▼            │
│    ┌─────────────────┐  ┌─────────────────┐   ┌──────────────────┐  │
│    │ PiKernelAdapter │  │ CodeIntelligence│   │ Python kernel    │  │
│    │ replaceable     │  │ AFT -> own Rust │   │ existing scripts │  │
│    └───────┬─────────┘  └─────────────────┘   └──────────────────┘  │
│            │                                                          │
│            ▼                                                          │
│    ┌─────────────────┐                                               │
│    │ Pi SDK sessions │                                               │
│    │ LLM loop only   │                                               │
│    └───────┬─────────┘                                               │
│            │ custom tool calls only                                  │
│            ▼                                                          │
│  ┌────────────────────────────────────────────────────────────────┐  │
│  │                 ToolBroker / PolicyEngine                      │  │
│  │ read | edit | shell | git | index | app | browser | deploy     │  │
│  └───────┬──────────────┬─────────────┬──────────────┬─────────────┘  │
│          │              │             │              │                │
│          ▼              ▼             ▼              ▼                │
│   filesystem/git   Execution      Browser UAT    Remote/Deploy        │
│                    Backend        Playwright/CDP Docker/SSH/etc       │
└───────────────────────────────────────────────────────────────────────┘
```

---

## 6. Non-negotiable architectural rules

### R1 — Pi is behind an adapter

No Pi imports outside `packages/pi-kernel`.

### R2 — No raw Pi mutation tools in production sessions

Create sessions with Pi built-ins disabled (`noTools: "builtin"` or equivalent SDK configuration) and register only owned `itsm_*` tools.

### R3 — Every phase is a real fresh session

A new Pi `AgentSession` is created for every producer phase and every execute↔QA/rework iteration unless the current its-magic contract explicitly defines a same-phase continuation.

### R4 — Orchestrator cannot implement

The orchestrator has no source-write tool and no unrestricted shell tool.

### R5 — Artifact memory is canonical

Cross-phase context comes from artifacts + bounded context packs + index results, never previous role transcript carry-over.

### R6 — Validators remain authoritative

The runtime does not reimplement shipped Python validator semantics in TypeScript during v1.

### R7 — Browser/App runtime is owned

Browser and app-launch capability cannot depend on Cursor or Pi community plugins.

### R8 — Third-party index is replaceable

AFT is a backend, not an architectural dependency visible to workflow code.

### R9 — Config is code-parsed, not prompt-parsed

Autonomy/model/delivery/security switches are resolved by a typed config engine.

### R10 — Security hard gates cannot be relaxed

Preserve the current autonomy-stop rule that `security_hard` conditions are not softened by autonomy presets.

---

## 7. `AgentKernel` boundary

```ts
export interface AgentKernel {
  createSession(spec: AgentSessionSpec): Promise<AgentSessionHandle>;
  run(session: AgentSessionHandle, input: AgentInput): Promise<AgentRunResult>;
  steer(session: AgentSessionHandle, input: AgentInput): Promise<void>;
  abort(session: AgentSessionHandle): Promise<void>;
  dispose(session: AgentSessionHandle): Promise<void>;
  getRuntimeInfo(): Promise<AgentKernelRuntimeInfo>;
}
```

Pi implementation:

```text
packages/pi-kernel/
  model-runtime.ts
  auth.ts
  session-factory.ts
  resource-loader.ts
  event-bridge.ts
  tool-adapter.ts
  pi-kernel.ts
```

No workflow module should know about `AgentSession`, `ModelRuntime`, Pi resource paths, or Pi events directly.

---

## 8. Pi resource isolation

Do **not** let a random target repository silently control our runtime through normal Pi project discovery.

Default standalone policy:

- do not auto-load project `.pi/extensions`,
- do not auto-load arbitrary project Pi packages,
- do not auto-load project Pi prompt templates,
- do not treat project `AGENTS.md` as an enforcement source,
- do not load third-party mutation tools outside our allowlist.

Provide an explicit compatibility flag later:

```text
PI_COMPAT_RESOURCES=off     # default
PI_COMPAT_RESOURCES=trusted
```

Even in trusted mode, tool permissions still go through our ToolBroker.

---

## 9. Sessions and real isolation proof

### 9.1 Session model

```text
Run auto-20260905-01

orchestrator runtime
  ├─ session po/intake            pi_session=A
  ├─ session po/discovery         pi_session=B
  ├─ session tl/research          pi_session=C
  ├─ session tl/architecture      pi_session=D
  ├─ session qa/plan-verify       pi_session=E
  ├─ session dev/execute#1        pi_session=F
  ├─ session qa/qa#1              pi_session=G
  ├─ session dev/execute#2        pi_session=H
  ├─ session qa/verify-work       pi_session=I
  ├─ session release/release      pi_session=J
  ├─ session qe/closure           pi_session=K
  └─ session curator/refresh      pi_session=L
```

### 9.2 Runtime-generated attestation

The runtime, not the model, creates an attestation at spawn/start/end:

```json
{
  "orchestrator_run_id": "auto-...",
  "phase_id": "execute",
  "role_id": "dev",
  "kernel": "pi",
  "kernel_session_id": "...",
  "kernel_process_instance": "...",
  "model_id": "openai-codex/...",
  "context_pack_hash": "sha256:...",
  "policy_hash": "sha256:...",
  "created_at": "...",
  "parent_phase_session_id": null,
  "fresh": true
}
```

Existing US-0048 / US-0056 required fields remain populated exactly as expected. Add standalone-specific attestation as a sidecar first so legacy validators are not broken.

### 9.3 Fail conditions

Fail closed on:

- repeated session id across phase boundary,
- role mismatch,
- context pack containing prior-role transcript,
- missing runtime attestation,
- attestation hash mismatch,
- expired strict proof,
- orchestrator issuing a phase-owned mutation.

---

## 10. Role runtime

### 10.1 Core roles

Preserve current semantic roles and add runtime-only service roles where needed:

| Role | Main objective | Default mutability |
|---|---|---|
| orchestrator | schedule only | no project writes |
| po | problem/value/spec | product docs + PO handoffs |
| tech-lead | research/architecture/plan | engineering docs/decisions/sprints |
| dev | implementation | code/tests/dev artifacts |
| qa | independent validation | QA/UAT/test evidence, no production-code fix by default |
| release | release artifacts/publish orchestration | release surfaces only |
| qe/closure | deterministic story closure | backlog/acceptance/closure evidence only |
| curator | compact/reconcile context | context/archives/state surfaces |
| security | findings/review | findings only unless explicit remediation mode |
| critic | adversarial independent review | findings only |
| scout | read-only code reconnaissance | none |

`closure` should follow the current contract: prefer `qe`; deterministic curator fallback only when the kernel contract allows it.

### 10.2 Role prompts are intentionally short

Role prompt contains only:

- identity/objective,
- target phase,
- input artifacts,
- expected output artifacts,
- concise quality constraints,
- current task/AC.

It does **not** contain:

- full permission matrix,
- validator algorithms,
- stop matrix,
- path deny lists,
- full command markdown,
- provider routing logic.

Those are code.

### 10.3 Sovereign role manifest

Load the existing role-behavior manifest through a typed parser and inject only the bounded `objective_function` / review focus required for that role. Runtime enforces the canonical phase→role matrix separately.

---

## 11. ToolBroker and PolicyEngine

### 11.1 Tool surface exposed to Pi

Recommended canonical tools:

```text
itsm_read
itsm_search
itsm_outline
itsm_symbol
itsm_references
itsm_callers
itsm_impact
itsm_edit
itsm_write
itsm_patch
itsm_shell
itsm_git
itsm_test
itsm_validate
itsm_app_start
itsm_app_stop
itsm_app_logs
itsm_app_health
itsm_browser
itsm_deploy
itsm_spawn_review
```

The exact set per role is computed before session creation.

### 11.2 Policy decision tuple

Every potentially consequential tool request is evaluated against:

```text
role
phase
story
sprint
cwd/worktree
path(s)
command
execution backend
autonomy mode
permission mode
security classification
operator approvals
```

Result:

```text
ALLOW
ASK
DENY
```

### 11.3 Path ownership

Implement the current cross-phase ownership philosophy as code:

- PO cannot write production source.
- QA cannot silently patch production source during independent QA.
- Release cannot mark a story DONE.
- Closure cannot modify release artifacts.
- Orchestrator cannot do phase-owned writes.
- Curator cannot rewrite product intent.

### 11.4 Shell policy

Parse and classify shell actions:

- safe read-only,
- build/test,
- local process control,
- package install,
- git mutation,
- destructive filesystem,
- network/deploy,
- privileged command.

Apply role/autonomy/backend policy. Keep explicit deny rules for secret files.

### 11.5 Audit

Every write/shell/browser/deploy action writes a compact runtime audit row with:

- run/phase/session/tool id,
- normalized action,
- policy decision,
- duration,
- result,
- evidence ref,
- no secret payloads.

---

## 12. Authentication and model/provider routing

### 12.1 Pi `ModelRuntime` as transport/auth engine

Use Pi's model runtime behind `ModelRouter`.

Support:

- ChatGPT Plus/Pro Codex OAuth,
- API-key OpenAI,
- Anthropic,
- Google,
- OpenRouter,
- DeepSeek,
- Moonshot/Kimi,
- Z.AI/GLM,
- MiniMax,
- DashScope/Qwen via custom/OpenAI-compatible provider,
- LM Studio / Ollama / vLLM / local OpenAI-compatible gateways,
- custom corporate gateways/proxies.

### 12.2 Standalone auth UX

Target UX:

```text
itsm auth list
itsm auth login openai-codex
itsm auth login anthropic
itsm auth set openrouter
itsm models list
itsm models test <provider/model>
```

Implementation can initially reuse Pi's default auth storage during the spike. Before stable release, use a standalone-owned credential path/store while continuing to use Pi's provider auth implementations.

Never copy OAuth tokens into project files.

### 12.3 Model resolution precedence

Preserve current its-magic semantics, but resolve to actual Pi models:

```text
CLI explicit model
  > phase-specific local override
  > role catalog override
  > critic override (for critic only)
  > tier/catalog mapping
  > runtime default
```

Typed config replaces prompt-level interpretation.

### 12.4 Thinking level

Treat thinking level as a separate axis from model slug and token profile:

```yaml
roles:
  po:
    model: openai-codex/...
    thinking: medium
  tech_lead:
    model: anthropic/...
    thinking: high
  dev:
    model: openai-codex/...
    thinking: high
  qa:
    model: zai/...
    thinking: high
```

### 12.5 Critic collision

Preserve current same-model degraded behavior: if critic resolves to same slug as producer, mark degraded single-model/multi-lens mode instead of falsely claiming cross-model independence.

---

## 13. Typed configuration and legacy scratchpad migration

### 13.1 Goal

The standalone runtime must not repeatedly parse behavior from markdown comments.

Create a typed config model for:

- delivery mode,
- token profile,
- work-kind routing,
- phase policy,
- model mapping,
- autonomy preset,
- stop policy,
- test/retry caps,
- browser policy,
- dev-environment profile,
- remote targets,
- security/compliance modes,
- sovereign features.

### 13.2 Compatibility adapter

For existing its-magic repos:

```text
LegacyScratchpadAdapter
  reads existing flags
  validates them
  maps into RuntimeConfig
  emits migration diagnostics
```

Do not require the operator to migrate before first use.

### 13.3 Precedence

Research/architecture should lock an exact precedence, recommended:

```text
CLI one-run overrides
  > local project runtime config (gitignored)
  > shared project runtime config
  > legacy scratchpad compatibility values
  > framework defaults
```

Secrets never enter shared project config.

---

## 14. Workflow Engine

### 14.1 Canonical phase graph

Standard lifecycle includes current closure semantics:

```text
intake
→ discovery
→ research
→ architecture
→ sprint-plan
→ plan-verify
→ execute
↔ qa                 bounded rework loop
→ verify-work
→ release
→ closure
→ refresh-context
```

Security/review hooks are supplementary, not role substitutions.

### 14.2 Phase→role contract

Preserve the current canonical mapping and alternates. Resolve one expected role before spawn. No unrelated fallback.

### 14.3 Command router

Slash commands are programmatic entry points:

```text
/intake
/discovery
/research
/architecture
/sprint-plan
/plan-verify
/execute
/qa
/verify-work
/release
/closure
/refresh-context
/auto
/quick
/ask
/memory-audit
/map-codebase
/security-review
```

Each command:

1. resolves target and config,
2. validates preconditions,
3. resolves role/model/tools/context,
4. spawns fresh session if agent work is required,
5. runs hard validators,
6. records evidence,
7. returns next-state intent.

No 200-line prompt body is the workflow engine.

### 14.4 `/auto`

Implement the current full-autonomy semantics as runtime state:

```text
while run active:
  determine target work item
  classify work kind / delivery mode
  resolve phase plan
  preflight role + model + policy
  create fresh session
  run phase
  validate evidence
  run critic/review hooks if enabled
  apply bounded repair/retry policy
  advance phase or execute↔qa loop
  on release -> closure -> refresh
  if drain policy allows -> next OPEN story/bug
  stop on deterministic terminal condition
```

### 14.5 Stop matrix

Do not hardcode divergent stop semantics in multiple languages.

Recommended migration:

**v0/v1:** runtime calls existing helper/validator surfaces and mirrors current reason-code behavior.  
**v1.x:** extract a versioned, machine-readable canonical workflow/stop manifest from the kit repo, consumed by Cursor/OpenCode/standalone adapters.

### 14.6 Autonomy presets

Port US-0119 into the runtime config resolver. The runtime expands preset to per-feature settings before execution; models never decide whether a hard stop is relaxable.

---

## 15. Delivery modes and work-kind routing

Preserve current axes as separate concepts:

```text
DELIVERY_MODE      -> lifecycle shape
TOKEN_PROFILE      -> context/token breadth
CAVEMAN / voice    -> response style only
AUTONOMY_PRESET    -> operator intervention level
WORK_KIND_ROUTING  -> recommended lifecycle route
```

### Standard

Full canonical lifecycle.

### Ultra lean

Preserve existing macro semantics and layered memory, while adding the separate closure responsibility into the ship macro as required by current framework behavior.

### Mega quick

Use enhanced quick flow for eligible bounded work, with tests and acceptance evidence mandatory.

### Work-kind classifier

Existing doc/mini/code classification becomes a library invoked by `WorkflowEngine`, not an agent guess.

---

## 16. Kernel bridge to the current its-magic repo

### 16.1 Do not copy Python validators

Create:

```text
KernelBridge
  locateProjectKernel()
  getKernelVersion()
  runValidator(name,args)
  readContractManifest()
  resolveArtifactPaths()
  runUatPlanner()
  runStatusReconcile()
```

### 16.2 Version handshake

Standalone must fail closed when the project kit is incompatible:

```text
KERNEL_NOT_FOUND
KERNEL_VERSION_UNSUPPORTED
KERNEL_VALIDATOR_MISSING
KERNEL_CONTRACT_MISMATCH
```

### 16.3 Compatibility policy

Runtime package declares:

```text
runtime version -> supported kernel contract range
```

Never infer compatibility from filenames alone.

### 16.4 Long-term kernel extraction

After the standalone agent works, consider extracting a small host-neutral package from the existing repo:

```text
its-magic-kernel/
  contracts/
  manifests/
  python validators/
  schemas/
  reason-codes/
```

Do not block v1 on that refactor.

---

## 17. Cursor-like code intelligence

### 17.1 Requirement

The agent must answer questions such as:

```text
Where is subscription restart recovery implemented?
Who calls it?
What tests cover it?
What interfaces and decisions are related?
What would break if I change this symbol?
```

without brute-force whole-repo reads.

### 17.2 `CodeIntelligenceProvider` interface

```ts
interface CodeIntelligenceProvider {
  status(): Promise<IndexStatus>;
  search(q: CodeQuery): Promise<SearchHit[]>;
  outline(path: string): Promise<FileOutline>;
  symbol(ref: SymbolRef): Promise<SymbolInfo>;
  references(ref: SymbolRef): Promise<Reference[]>;
  callers(ref: SymbolRef): Promise<CallEdge[]>;
  callees(ref: SymbolRef): Promise<CallEdge[]>;
  impact(ref: SymbolRef): Promise<ImpactReport>;
  diagnostics(scope: Scope): Promise<Diagnostic[]>;
  refresh(changes?: Path[]): Promise<void>;
}
```

### 17.3 AFT as v1 backend

AFT is a strong first implementation because it already provides:

- Rust backend,
- persistent warm process,
- trigram/text index,
- semantic search,
- Tree-sitter structure,
- symbol outline/zoom,
- AST-aware search,
- LSP diagnostics,
- call graph,
- file mutation features.

**Production rule:** do not load AFT's direct edit/write overrides into Pi sessions unless they are wrapped by our PolicyEngine. Prefer using AFT as a read/code-intelligence service through an adapter.

### 17.4 Future `its-indexd`

If AFT becomes limiting, implement a drop-in Rust service:

```text
its-indexd
  filesystem watcher
  gitignore parser
  Tantivy/trigram lexical index
  Tree-sitter parser cache
  symbol graph
  import graph
  call/reference graph
  LSP bridge
  semantic embeddings
  git/change metadata
  SQLite index metadata
  RPC/NDJSON protocol
```

The agent should not notice the backend change.

### 17.5 `code_context(task)` fusion

Context engine should combine:

```text
semantic search
+ lexical exact search
+ symbols
+ call graph
+ references
+ tests
+ git diff/history signal
+ current story/AC
+ architecture/decision refs
```

then rank and build a bounded context pack.

### 17.6 Existing `/map-codebase`

Keep `docs/engineering/codebase-map.md` as a human/agent-friendly **derived architecture map**, not the primary index database.

On fresh repos:

- index automatically,
- generate/refresh map when missing or stale,
- record map/index version and coverage,
- do not require repeated full-map reads for every phase.

### 17.7 Benchmark against Cursor

Create a repeatable benchmark suite:

1. find implementation by natural language,
2. find exact symbol,
3. find callers,
4. find related tests,
5. impact analysis,
6. cross-language symbol reference,
7. recently changed code,
8. large monorepo response latency,
9. tokens required to solve task,
10. stale-index recovery.

The goal is not marketing parity; it is measured agent usefulness.

---

## 18. Context Engine

### 18.1 Inputs

Per phase, build context from:

- target work item,
- AC/task pack,
- phase handoff,
- relevant state/resume refs,
- relevant architecture/decisions,
- code-index retrieval,
- sovereign memory digest when enabled,
- role objective/review focus,
- current diff/test failures when relevant.

### 18.2 Forbidden context

Do not inject:

- previous role transcript,
- entire backlog by default,
- entire architecture history by default,
- `.env`, credentials, auth tokens,
- unrelated sprint history,
- giant static command markdown.

### 18.3 Layered memory

Reuse current hot/warm/cold ideas:

```text
HOT   active-context / current handoff / current run state
WARM  work pack / current story / selected decisions / sovereign digest
COLD  targeted sections / archives / semantic index retrieval
```

### 18.4 Context evidence

Store context-pack hash and selected source refs for reproducibility/debugging without storing secrets or full duplicated content.

---

## 19. Application Runtime / Dev Environment Manager

This is a **v1 requirement**, not polish.

### 19.1 Goals

The agent can:

- detect the project stack,
- start the app,
- keep the process alive,
- watch logs,
- wait for readiness,
- restart/rebuild after changes,
- stop cleanly,
- connect to local/Docker/SSH/WSL targets,
- expose resolved URL/ports to browser QA.

### 19.2 Service model

```ts
interface AppRuntime {
  discover(): Promise<AppProfile[]>;
  start(profileId: string): Promise<AppHandle>;
  stop(handle: AppHandle): Promise<void>;
  restart(handle: AppHandle): Promise<AppHandle>;
  health(handle: AppHandle): Promise<HealthResult>;
  logs(handle: AppHandle, opts: LogQuery): Promise<LogChunk>;
}
```

### 19.3 Process manager

Track:

- pid/container/service id,
- command/cwd,
- port/url,
- readiness state,
- start time,
- log ring buffer,
- crash/restart count,
- owning run/phase.

### 19.4 Execution backends

```text
ExecutionBackend
  ├─ local
  ├─ docker-local
  ├─ WSL
  ├─ SSH
  ├─ remote Docker
  └─ sandbox/micro-VM later
```

Current remote contracts remain input compatibility surfaces; the runtime owns execution.

### 19.5 Bounded self-debug

On startup/health failure:

1. capture logs,
2. classify failure,
3. spawn fresh DEV remediation session if policy allows,
4. patch,
5. rebuild/restart,
6. retry under cap,
7. fail with deterministic reason when exhausted.

---

## 20. Browser and UAT Runtime

This is also a **v1 requirement**.

### 20.1 Two browser modes

#### Isolated automation

Playwright-managed browser/context:

- reproducible,
- CI/headless,
- fresh cookies/profile,
- screenshots/traces,
- ideal for regression tests.

#### Authorized developer browser

Chrome/Chromium over CDP:

- existing logged-in session,
- browser extensions,
- internal/admin applications,
- operator-authorized only.

### 20.2 Browser API exposed to QA

```text
browser_open
browser_navigate
browser_snapshot
browser_click
browser_type
browser_select
browser_wait
browser_screenshot
browser_console
browser_network
browser_download
browser_upload
browser_accessibility
```

Prefer one structured `itsm_browser` tool with typed actions to avoid dozens of exposed schemas if that is more efficient for the model.

### 20.3 UAT planner composition

Reuse existing `uat_probe_lib.py` / UAT artifact semantics initially:

```text
acceptance step
   ↓
existing probe classifier/planner
   ↓
process_health | cli_smoke | browser_smoke | api probe | manual judgment
   ↓
standalone executor
   ↓
uat.json probe_results[] + evidence refs
```

### 20.4 Evidence

Per browser probe capture as applicable:

- screenshot path,
- DOM/accessibility snapshot summary,
- console error summary,
- failed network requests,
- final URL,
- trace zip,
- duration,
- browser backend,
- app-runtime handle/ref.

Keep existing fail-closed UAT reason families.

### 20.5 Credential rule

Browser agent must **not** read `.env` or type raw credentials from project files.

Authenticated flows should use:

- existing authorized browser profile,
- pre-provisioned test account via external secret injection that the model cannot read,
- operator approval step.

### 20.6 Exploratory → regression test

Optional but valuable:

```text
QA explores flow successfully
  ↓
QA proposes stable test steps
  ↓
DEV/QA writes Playwright regression spec
  ↓
subsequent runs execute deterministically
```

### 20.7 Visual QA later

Add baseline screenshot/layout diff only after stable functional browser UAT. Do not block core v1 on pixel-perfect infrastructure.

---

## 21. Tests and quality execution

### 21.1 Keep stack-aware test scaffolding

Preserve current behavior for Node, Python, Go, Java, .NET and unknown-stack fallback.

### 21.2 Runtime-owned execution

All tests execute through `ExecutionBackend` and produce structured evidence:

```json
{
  "command": "...",
  "backend": "local",
  "exit_code": 0,
  "duration_ms": 1234,
  "stdout_ref": "...",
  "stderr_ref": "..."
}
```

### 21.3 Output compression

Large build/test logs should be stored to evidence files and summarized to the model. Do not burn model context on megabytes of successful output.

---

## 22. Cross-model critic and role reviews

### 22.1 Producer/critic separation

At configured boundaries:

```text
producer session
  ↓ artifact output
fresh critic session using different model if possible
  ↓ findings
bounded producer rework if blocking
```

### 22.2 Three lenses

Preserve Challenger / Architect / Subtractor semantics.

### 22.3 Role-behavior review graph

Runtime dispatches existing manifest obligations as separate review sessions. A review session never substitutes the producer phase role.

### 22.4 Model pinning

Respect current critic precedence and degraded collision semantics.

---

## 23. Parallel DEV / worktree arbitrage

Standalone is an ideal host for US-0108 behavior.

### 23.1 Flow

```text
Task
 ├─ worktree A -> DEV model A
 ├─ worktree B -> DEV model B
 └─ worktree C -> DEV model C
           ↓
       independent tests
           ↓
       QA arbiter
           ↓
  choose/merge best candidate
```

### 23.2 Resource guard

Bound:

- max instances,
- max tokens/cost,
- CPU/RAM,
- worktree count,
- concurrent browsers/tests,
- timeout.

### 23.3 Policy

Parallel agents get isolated worktrees and cannot mutate main working tree until arbiter/merge step.

---

## 24. Sovereign runtime

### 24.1 Decision ledger

Continue writing current append-only decision evidence; runtime can automatically capture model/session/run identifiers more reliably than Cursor.

### 24.2 Sovereign memory

Inject bounded digest only; never full memory store.

### 24.3 Deferrals and drain-generate

Owned scheduler handles open deferrals and candidate generation. Mandatory decision-gate semantics remain.

### 24.4 Goal convergence

Evaluate convergence as code between cycles. Do not let the model self-declare convergence without evidence.

### 24.5 Convergence fixes

Include current semantics:

- only blocking open critic findings block critic convergence,
- non-blocking same-run findings can be auto-resolved according to current contract,
- docs/contract-test slices can use the established smoke surrogate rather than fake browser PASS.

---

## 25. Release, deploy, self-healing and closure

### 25.1 Release

Release role owns release artifacts and publish decisions only.

### 25.2 Deploy

Publish/deploy through typed target adapters:

```text
ReleaseTarget
  ├─ git/github
  ├─ npm
  ├─ SSH command
  ├─ Docker
  ├─ custom command
  └─ later provider adapters
```

### 25.3 Self-healing deploy

After deploy:

1. run smoke probe,
2. capture runtime/browser evidence,
3. if failure is remediable and policy allows, spawn fresh DEV fix session,
4. rebuild/release/redeploy under bounded cap,
5. append deferral on exhaustion according to current contract.

### 25.4 Closure is separate

After successful release:

```text
release
  ↓
closure
  - verify release evidence
  - backlog OPEN -> DONE
  - acceptance unchecked -> checked
  - write closure-verification
  - write runtime/isolation evidence
  ↓
refresh-context
```

Release agent must not perform closure as a side effect.

---

## 26. Security architecture

### 26.1 Pi is not the sandbox

Pi runs with the OS user's permissions. Treat this as an explicit assumption.

### 26.2 Two distinct protection layers

```text
Layer A: its-magic semantic policy
  role/tool/path/phase/approval controls

Layer B: OS execution isolation
  local user / container / VM / micro-VM / remote sandbox
```

Both are needed for unattended high-autonomy operation.

### 26.3 Execution profiles

```yaml
execution_profiles:
  trusted_local:
    backend: local
  isolated_dev:
    backend: docker
    network: restricted
  untrusted_repo:
    backend: sandbox
    workspace_mount: copy
```

### 26.4 Secret handling

- never inject `.env` into LLM context,
- never log provider tokens,
- redact Authorization/Cookie headers from browser/network evidence,
- project config may reference secret names, not values,
- provider OAuth/API credentials live outside repo,
- remote/deploy auth references resolve inside execution layer.

### 26.5 Third-party extension policy

Default-deny arbitrary Pi extensions/packages inside standalone runtime. Every loaded extension is code execution.

---

## 27. Persistence and state ownership

### 27.1 Repo artifacts remain authoritative for project lifecycle

Do not move backlog/acceptance/decisions/sprint state into SQLite.

### 27.2 SQLite stores runtime-operational state

Examples:

- run index,
- live session handles,
- model usage/cost,
- tool audit,
- process handles,
- browser run metadata,
- code-index metadata,
- cached retrieval results,
- ephemeral approval state.

### 27.3 Crash recovery

On runtime restart:

1. inspect repo `resume_brief` / state / active work item,
2. inspect last runtime run record,
3. validate no phase was only “claimed” complete,
4. discard orphaned Pi sessions,
5. reconstruct next schedulable phase,
6. spawn fresh session.

No resumed phase should inherit an old role conversation by default.

---

## 28. Observability

### 28.1 Operator status line

Show:

```text
project | story | sprint | phase | role | model | backend | app health | index | browser | tokens/cost
```

### 28.2 Run timeline

```text
14:01 intake        PO      PASS
14:04 discovery     PO      PASS
14:09 architecture  TL      PASS
14:16 execute       DEV     PASS
14:23 qa            QA      FAIL -> rework
14:31 execute#2     DEV     PASS
14:38 qa#2          QA      PASS
14:41 browser UAT   QA      PASS
...
```

### 28.3 Metrics

Track:

- input/output/cache tokens,
- cost by role/model/provider,
- time by phase,
- tool calls,
- index search count/latency,
- files read/written,
- test duration,
- browser probe duration,
- retries,
- context-pack size.

Compose with existing token-cost evidence rather than creating conflicting accounting.

---

## 29. CLI/TUI and future control plane

### 29.1 v1 CLI

```text
itsm
itsm auto
itsm intake
itsm ask "..."
itsm status
itsm resume
itsm models
itsm auth
itsm index status
itsm app status
itsm browser status
```

Interactive mode supports slash equivalents.

### 29.2 TUI

Use Pi TUI components or its interactive primitives where useful, but keep TUI as a client of runtime services.

Panels:

- conversation,
- active phase/role,
- phase timeline,
- tool activity,
- changed files,
- app/log status,
- browser screenshot/evidence indicator,
- model/tokens/cost.

### 29.3 Control protocol from day one

Define a stable event/command protocol even if only local CLI uses it initially:

```text
RuntimeCommand
RuntimeEvent
ApprovalRequest
RunStateChanged
ToolStarted/Finished
BrowserEvidence
AgentTextDelta
```

This enables later:

- Android client,
- Galaxy Watch voice trigger,
- web dashboard,
- VS Code extension,
- remote Debian always-on daemon,

without moving workflow logic into those clients.

---

## 30. Recommended repository layout

```text
its-magic-agent/
├─ apps/
│  ├─ cli/
│  ├─ tui/
│  └─ daemon/                 # thin/local initially
│
├─ packages/
│  ├─ runtime-core/
│  │  ├─ workflow/
│  │  ├─ runs/
│  │  ├─ stop-matrix/
│  │  └─ recovery/
│  │
│  ├─ pi-kernel/
│  ├─ auth-models/
│  ├─ role-runtime/
│  ├─ policy-engine/
│  ├─ tool-broker/
│  ├─ context-engine/
│  ├─ code-intelligence/
│  ├─ aft-adapter/
│  ├─ kernel-bridge/
│  ├─ execution-runtime/
│  ├─ dev-environment/
│  ├─ browser-uat/
│  ├─ release-runtime/
│  ├─ sovereign-runtime/
│  ├─ config/
│  ├─ observability/
│  └─ protocol/
│
├─ crates/
│  └─ its-indexd/             # deferred; AFT first
│
├─ tests/
│  ├─ unit/
│  ├─ contract/
│  ├─ integration/
│  ├─ e2e/
│  ├─ security/
│  └─ fixtures/
│     ├─ node-webapp/
│     ├─ dotnet-webapp/
│     ├─ python-api/
│     └─ multi-repo/
│
├─ docs/
│  ├─ architecture/
│  ├─ operator/
│  └─ compatibility/
│
└─ package.json
```

---

## 31. Current framework capability migration matrix

| Current capability | Standalone disposition | Main owner |
|---|---|---|
| US-0001 lifecycle commands | **PORT semantics** | CommandRouter/WorkflowEngine |
| US-0002 rules | **DROP as enforcement** | runtime code/validators |
| US-0003 roles | **KEEP semantics** | RoleRuntime |
| US-0005 Cursor hooks | **REPLACE** | PolicyEngine/ToolBroker |
| US-0006 artifacts | **KEEP** | existing kernel |
| US-0023 fresh subagents | **HARD PORT** | SessionSupervisor |
| US-0024 memory audit | **KEEP + improve with index** | KernelBridge/CodeIntelligence |
| US-0027 UAT lifecycle | **KEEP** | BrowserUAT/KernelBridge |
| US-0028 security review | **KEEP** | Security role |
| US-0029 research/knowledge | **KEEP** | ContextEngine |
| US-0039 release gate chain | **KEEP** | GateEngine |
| US-0045 canonical status | **KEEP** | kernel/Closure |
| US-0048 isolation audit | **STRENGTHEN** | runtime attestation |
| US-0053 context compaction | **KEEP/PORT** | ContextEngine |
| US-0056 strict runtime proof | **STRENGTHEN** | runtime attestation |
| US-0064 remote contract | **KEEP compatibility** | ExecutionRuntime |
| US-0065 runtime QA | **PORT to actual runtime** | AppRuntime |
| US-0066 test scaffolding | **KEEP** | DEV/QA + KernelBridge |
| US-0069 phase role enforcement | **HARD PORT** | RoleRuntime |
| US-0070 phase selection | **PORT** | WorkflowEngine |
| US-0072 hot-surface compaction | **KEEP** | kernel/ContextEngine |
| US-0082 codebase map | **KEEP as derived artifact** | CodeIntelligence |
| US-0084/0086 remote execution | **PORT** | ExecutionRuntime |
| US-0092 full autonomy | **PORT core semantics** | WorkflowEngine |
| US-0093 Cursor browser UAT | **REPLACE backend, KEEP contract** | BrowserUAT |
| US-0095 Cursor native chain | **DROP host implementation** | owned scheduler |
| US-0096 delivery modes | **PORT** | WorkflowEngine/ContextEngine |
| US-0098/0099 dev auto-launch | **PORT and own** | DevEnvironment |
| US-0101/0102 model routing | **PORT and improve** | ModelRouter/Pi ModelRuntime |
| US-0103 decision ledger | **KEEP** | SovereignRuntime |
| US-0104 critic | **PORT** | ReviewScheduler |
| US-0105 memory | **KEEP** | ContextEngine/SovereignRuntime |
| US-0106 role behavior manifest | **KEEP/parse** | RoleRuntime |
| US-0107 sovereign loop | **PORT scheduler semantics** | SovereignRuntime |
| US-0108 parallel dev | **PORT** | WorktreeScheduler |
| US-0109 self-healing deploy | **PORT** | ReleaseRuntime |
| US-0110 convergence | **PORT evaluator** | SovereignRuntime |
| US-0111 release triggers | **KEEP/PORT adapters** | ReleaseRuntime |
| US-0112 catalogs | **MIGRATE to runtime catalog** | Config/ModelRouter |
| US-0118 work-kind routing | **PORT** | WorkflowEngine |
| US-0119 autonomy presets | **PORT** | Config/WorkflowEngine |
| US-0120 closure phase | **PORT exactly** | ClosureService |
| US-0121..0126 OpenCode | **KEEP separate compatibility host** | current kit repo |
| US-0127 critic convergence fix | **PORT current semantics** | SovereignRuntime |
| US-0128 smoke surrogate | **KEEP current semantics** | UAT/GateEngine |
| US-0129 architecture rollover guard | **KEEP kernel guard** | KernelBridge |
| US-0130 critic model pin | **PORT** | ModelRouter |

---

## 32. Development roadmap

### Phase 0 — contract inventory and spike

Goal: prove that the architecture is viable before building the product shell.

Deliver:

1. New repo bootstrap.
2. Pin tested Pi SDK versions.
3. `PiKernelAdapter` with one fresh session.
4. Codex OAuth/model-runtime authentication proof.
5. One custom tool with built-ins disabled.
6. Role/path denial proof.
7. Two isolated role sessions with different models/providers.
8. One existing Python validator invocation.
9. AFT read-only search proof.
10. Playwright starts a fixture app and captures screenshot/console evidence.

**Go/No-Go:** all ten pass without model-prompt trust.

### Phase 1 — kernel bridge + role/session security

Deliver:

- KernelLocator/version handshake,
- RoleCatalog,
- SessionSupervisor,
- real runtime attestation,
- ToolBroker,
- PolicyEngine,
- file/shell/git tools,
- audit log,
- typed config baseline,
- legacy scratchpad reader.

### Phase 2 — code intelligence + context engine

Deliver:

- AFT adapter,
- index lifecycle/watcher,
- search/outline/symbol/ref/callgraph/diagnostics,
- code-context fusion,
- current-work context builder,
- map-codebase integration,
- context-pack hashes,
- Cursor comparison benchmark.

### Phase 3 — canonical lifecycle

Deliver:

- command router,
- phase graph,
- role enforcement,
- standard lifecycle from intake through refresh,
- execute↔QA bounded loop,
- decision gates,
- release gate chain,
- closure phase,
- crash/resume.

### Phase 4 — app runtime + browser UAT

Deliver:

- stack discovery,
- ProcessManager,
- health/log/restart,
- local/Docker backend,
- remote SSH backend,
- Playwright browser,
- CDP authorized browser mode,
- UAT probe executor,
- evidence capture,
- bounded debug retry.

### Phase 5 — model/provider productization

Deliver:

- standalone auth commands,
- per-role/model catalog,
- thinking levels,
- Chinese/custom OpenAI-compatible providers,
- critic pinning,
- provider/model health tests,
- cost/usage collection.

### Phase 6 — autonomy and delivery parity

Deliver:

- `/auto`,
- drain,
- phase selection,
- delivery modes,
- work-kind routing,
- autonomy presets,
- stop/repair ledgers,
- bulk story/bug execution,
- quiet mode/operator authority.

### Phase 7 — sovereign parity

Deliver:

- decision ledger,
- sovereign memory,
- role review obligations,
- cross-model critic,
- parallel DEV/worktrees,
- deferral/drain-generate,
- self-healing deploy,
- goal convergence and current fixes.

### Phase 8 — operator product surface

Deliver:

- polished CLI/TUI,
- run timeline,
- status dashboards,
- JSON-RPC/control protocol,
- daemon mode,
- installation/update flow,
- docs/migration from existing Cursor/OpenCode repos.

### Phase 9 — optional sovereignty upgrades

Potential:

- own `its-indexd`,
- stronger sandbox/micro-VM,
- VS Code client,
- web/mobile/watch client,
- distributed workers,
- remote always-on Debian execution.

---

## 33. Suggested first-intake plan-area inventory

Do **not** clone US-0001..US-0130 into the new repo. Intake the standalone product as capability slices.

| `plan_area_id` | v1 mapping intent | Defer? |
|---|---|---|
| `repo-bootstrap` | TS workspace, CI, pinned Pi deps | No |
| `kernel-consume-contract` | locate/version/invoke current kit | No |
| `pi-kernel-adapter` | embedded SDK boundary | No |
| `auth-model-runtime` | OAuth/API/custom providers | No |
| `session-isolation-attestation` | fresh Pi sessions + proof | No |
| `role-runtime` | phase→role + role manifest | No |
| `tool-policy-engine` | owned tools/path/shell permissions | No |
| `typed-config-legacy-adapter` | runtime config + scratchpad compatibility | No |
| `code-intelligence-aft` | indexed search/AST/LSP/call graph | No |
| `context-engine` | artifacts + index + layered memory | No |
| `workflow-standard` | full lifecycle including closure | No |
| `auto-autonomy` | drain/stop/retry/phase policy | No |
| `delivery-routing` | work-kind + standard/lean/quick | No |
| `dev-environment-runtime` | launch/log/health/restart | No |
| `browser-uat` | Playwright/CDP + evidence | No |
| `remote-execution` | Docker/SSH/WSL abstractions | No |
| `release-deploy-closure` | publish/self-heal/closure | No |
| `sovereign-runtime` | ledger/memory/critic/convergence | Can be v1.5 slice, not dropped |
| `parallel-dev-worktrees` | N candidate implementations + arbiter | Can follow core lifecycle |
| `cli-tui-observability` | operator product surface | No, polish can slice |
| `daemon-control-api` | stable local control protocol | Minimal v1; richer later |
| `own-rust-indexer` | replace AFT if necessary | `deferred_ref` |
| `ide-client` | VS Code/Cursor-like client | `deferred_ref` |
| `mobile-watch-client` | remote voice/control client | `deferred_ref` |
| `opencode-adapter` | existing current-kit program | external/compatibility |
| `cursor-adapter` | existing current-kit program | external/compatibility |

Intake must map every row to story IDs or explicit deferral.

---

## 34. Suggested implementation stories

A sensible new-repo backlog is approximately 12–16 larger vertical stories, not 130 historical ones.

### Story 1 — Pi kernel + repo bootstrap

Prove embedded sessions, events, custom tools, pinned deps.

### Story 2 — Kernel bridge + compatibility handshake

Consume existing validators/artifacts safely.

### Story 3 — Auth/model router

Codex OAuth + APIs + custom providers + per-role model resolution.

### Story 4 — Session/role isolation and runtime attestation

Fresh session evidence, role mismatch fail-closed.

### Story 5 — Policy/tool broker

Owned read/edit/shell/git with hard path/role restrictions.

### Story 6 — Code intelligence and context engine

AFT, semantic/symbol/callgraph retrieval, bounded context packs.

### Story 7 — Standard lifecycle orchestrator

Intake→release→closure→refresh, decision gates, validators.

### Story 8 — Dev environment and runtime QA

App launch, health, logs, retries, execution backends.

### Story 9 — Browser UAT

Playwright/CDP, screenshots, console/network, UAT evidence.

### Story 10 — Delivery modes + work-kind + autonomy

Standard/lean/quick, phase selection, full-autonomy drain and stop policy.

### Story 11 — Sovereign reviews/memory/convergence

Ledger, critic, role reviews, memory, goal loop.

### Story 12 — Parallel DEV and self-healing deploy

Worktrees, arbiter, deploy smoke and bounded repair.

### Story 13 — CLI/TUI/operator experience

Status/timeline/approvals/models/index/app/browser views.

### Story 14 — Installation/migration/compatibility

Existing its-magic project adoption; Cursor/OpenCode coexistence.

### Story 15 — Control protocol/daemon

RPC/event API ready for remote/mobile clients.

---

## 35. Hard proof tests before architecture lock

The following tests must pass before committing to Pi as the long-term kernel.

### Agent/kernel

- create fresh Pi session via SDK,
- disable built-in tools,
- run only owned custom tools,
- stream events reliably,
- abort reliably,
- session id available for attestation,
- no project-local Pi extension auto-execution.

### Isolation

- PO and DEV have distinct session IDs,
- execute↔QA cycle uses new sessions every time,
- orchestrator has no mutation tools,
- stale/reused session fails gate.

### Provider/auth

- Codex OAuth works through model runtime,
- API provider works simultaneously,
- custom OpenAI-compatible provider works,
- role A and role B can use different providers in same run,
- OAuth refresh does not require exposing token to model.

### Permissions

- PO attempt to edit `src/**` denied,
- QA attempt to silently fix production source denied,
- DEV allowed within source scope,
- `.env` read denied,
- destructive shell blocked/asked according to policy.

### Code intelligence

- semantic lookup,
- exact symbol,
- callers,
- related tests,
- diagnostics,
- incremental refresh after edit.

### App/browser

- fixture app auto-start,
- readiness detected,
- console log captured,
- browser navigates/clicks/types,
- screenshot saved,
- browser failure returns deterministic FAIL,
- app crash triggers bounded runtime handling.

### Kernel/gates

- existing validator PASS is accepted,
- existing validator FAIL blocks next phase,
- release cannot bypass QA/UAT,
- closure cannot execute before valid release evidence.

---

## 36. Testing strategy

### Unit tests

- config precedence,
- phase resolver,
- role resolver,
- model resolver,
- stop policy,
- permission rules,
- context ranking,
- reason-code mapping.

### Kernel contract tests

Run actual existing its-magic Python validators against fixtures.

### Pi adapter contract tests

Use deterministic fake/mock model provider where possible to test tool/event/session behavior without paid calls.

### Integration fixtures

Maintain small fixture repos:

- Node web app,
- .NET web API + UI,
- Python API,
- Docker compose stack,
- multi-repo contract fixture.

### Browser E2E

Test app launch → browser flow → evidence → UAT gate.

### Chaos/failure tests

Inject:

- model timeout,
- provider 429/500,
- tool timeout,
- process crash,
- browser crash,
- stale index,
- invalid kernel version,
- validator crash,
- remote disconnect,
- runtime restart mid-phase.

Verify deterministic resume/stop behavior.

### Security tests

- malicious repo `.pi/extensions` does not load,
- prompt tries to read secret file -> tool denies,
- path traversal denied,
- shell exfiltration pattern denied/asked,
- browser evidence redacts headers/cookies,
- untrusted execution backend isolation.

### Host parity tests

For selected lifecycle scenarios, compare Cursor/OpenCode/standalone against **contracts**, not transcript equality:

- artifacts required,
- gates passed,
- role isolation,
- status transitions,
- UAT/release evidence.

---

## 37. Definition of Done — core standalone v1

An operator can install the standalone agent, open an existing or freshly installed its-magic project, and:

1. authenticate at least Codex OAuth plus one API-key provider,
2. configure different models for PO/TL/DEV/QA/critic,
3. run `/intake` through `/closure` without Cursor or OpenCode,
4. prove every role phase ran in a real fresh Pi session,
5. have role/path/tool permissions enforced even when the model ignores instructions,
6. use persistent code indexing to find symbols/references/tests/impact,
7. auto-launch a supported application stack,
8. run browser UAT with screenshots and console/network evidence,
9. block release on failed Python validator/QA/UAT gates,
10. pause/restart the runtime and resume from repository evidence without cross-role chat carry,
11. run standard and at least one lean/quick route,
12. emit model/token/tool/runtime audit data,
13. preserve project artifact schemas expected by the current its-magic kernel,
14. keep Cursor and OpenCode paths intact in the existing kit repo.

---

## 38. Definition of Done — current-framework parity milestone

After core v1, parity is complete when standalone also supports the current advanced contracts:

- full-autonomy backlog/bug drain,
- work-kind routing,
- autonomy presets/repair policy,
- sovereign decision ledger,
- cross-model critic,
- sovereign memory,
- role-behavior reviews,
- parallel DEV/worktrees,
- sovereign deferrals/drain-generate,
- self-healing deploy,
- goal convergence including current critic/smoke semantics,
- release triggers/changelog behavior,
- separate closure phase,
- hot-surface/archive guards.

---

## 39. Explicit non-goals for first release

- Build a full graphical Cursor clone.
- Replace every Python validator with TypeScript.
- Delete Cursor/OpenCode support from its-magic.
- Fork Pi before the SDK proves insufficient.
- Let arbitrary Pi extensions execute in the target repo by default.
- Build our own vector/index engine before benchmarking AFT.
- Make browser automation capable of secretly entering operator credentials.
- Make chat transcripts the project memory.
- Claim security sandboxing from in-process permission checks alone.
- Clone every historical its-magic story into the new backlog.

---

## 40. Primary risks and mitigations

| Risk | Mitigation |
|---|---|
| Pi SDK churn | narrow adapter, exact version pin, upgrade contract suite |
| Pi lacks security boundary | own tools + PolicyEngine + OS isolation backend |
| Third-party project Pi code executes | custom ResourceLoader / default deny project extensions |
| AFT becomes dependency risk | provider interface; benchmark; own Rust escape hatch |
| AFT direct edit bypasses policy | use read-only adapter or wrap all mutation through ToolBroker |
| OAuth behavior changes | keep auth behind ModelRouter/AuthService; credential health tests |
| Duplicate workflow semantics TS vs Python | consume manifests/validators; extract canonical machine-readable contracts later |
| Browser tests flaky | readiness checks, deterministic waits, traces, bounded retries, isolated profiles |
| Authenticated browser unsafe | explicit CDP authorization, no credential reading, redact evidence |
| Context becomes huge again | index-first retrieval, layered memory, strict per-phase budgets |
| Runtime DB becomes new source of truth | project lifecycle state remains artifacts; DB only operational |
| Autonomous loop runs away | existing caps/stop matrix/autonomy policy + hard security gates |
| Parallel DEV burns cost/resources | budget and concurrency guard before spawn |
| Closure/status drift returns | exclusive closure service + existing canonical reconciliation validators |
| App runtime differs by stack | plugin-like stack adapters with deterministic unknown-stack failure/fallback |

---

## 41. Recommended key architecture decisions to lock

Create formal decisions during `/architecture` for at least:

1. **Pi embedded SDK, not Pi CLI/extension host, as primary kernel.**
2. **No raw Pi built-in mutation tools; all agent actions through ToolBroker.**
3. **Repo artifacts remain canonical memory; Pi sessions are ephemeral execution context.**
4. **Fresh Pi session per phase with runtime-generated attestation.**
5. **Existing Python validators remain source of truth in v1.**
6. **AFT behind `CodeIntelligenceProvider`; no direct policy-bypassing edit override.**
7. **Playwright primary isolated UAT + authorized CDP secondary mode.**
8. **Typed config + legacy scratchpad adapter.**
9. **ExecutionBackend abstraction for local/Docker/SSH/sandbox.**
10. **Release and Closure remain separate phases.**
11. **Pi project extension/resource discovery default-off in standalone.**
12. **Versioned kernel/runtime compatibility handshake.**

---

## 42. Research questions to close before implementation

### Pi SDK

- Exact tested Pi version and upgrade policy?
- Best ResourceLoader strategy to disable project-local resources while keeping our internal extensions/tools?
- Best way to obtain/stabilize kernel session IDs for attestation?
- SDK API for programmatic subscription OAuth login UX inside our CLI?
- Event ordering guarantees required for tool audit and abort?

### Kernel

- Which current Python scripts are public host contracts versus Cursor implementation details?
- Can stop-matrix/phase-role/artifact ownership be exported as versioned JSON/YAML without risky refactor?
- Exact runtime contract version marker to add to the kit?

### Index

- Can AFT be consumed cleanly as a backend without loading its Pi mutation overrides?
- AFT process lifecycle under multiple parallel worktrees?
- Index persistence/storage cost on large monorepos?
- Windows behavior and LSP coverage?

### Browser

- Playwright browser install strategy for Windows/Linux?
- CDP launch/attach security UX?
- Evidence redaction implementation?
- Which existing UAT probe fields are sufficient versus additive standalone fields?

### Sandbox

- Preferred v1 isolation on Windows versus Linux?
- Whether Docker is enough for default unattended mode or Gondolin/micro-VM should be supported early?

---

## 43. Recommended sequencing relative to OpenCode

The OpenCode adapter is already a useful compatibility path. Do not discard it.

However, for the primary product direction:

```text
current its-magic kernel
       ├─ Cursor host          compatibility
       ├─ OpenCode host        compatibility
       └─ Standalone Pi host   PRIMARY OWNED PRODUCT
```

Do **not** spend new architecture effort trying to make OpenCode the permanent center if the Pi hard-proof spike passes.

---

## 44. Naming / packaging recommendation

Working repository:

```text
its-magic-agent
```

CLI:

```text
itsm
```

Alternative repo name:

```text
its-magic-runtime
```

Package namespaces could be:

```text
@its-magic/runtime-core
@its-magic/pi-kernel
@its-magic/code-intelligence
@its-magic/browser-uat
@its-magic/cli
```

Do not lock branding in technical spike stories.

---

## 45. Research references — verified 2026-09-05

### Pi official

- https://pi.dev/docs/latest
- https://pi.dev/docs/latest/sdk
- https://pi.dev/docs/latest/providers
- https://pi.dev/docs/latest/extensions
- https://pi.dev/docs/latest/custom-provider
- https://pi.dev/docs/latest/security
- https://pi.dev/docs/latest/containerization
- https://github.com/earendil-works/pi
- https://github.com/earendil-works/pi/tree/main/packages/coding-agent/examples/extensions/subagent

Key verified points at plan time:

- SDK exposes `createAgentSession`, `SessionManager`, resource loading, custom tools and event streaming.
- `ModelRuntime` resolves runtime overrides, stored API/OAuth credentials and environment keys.
- built-in subscription login includes ChatGPT Plus/Pro Codex.
- custom providers can add OAuth/SSO/custom endpoints.
- SDK can disable built-in tools while keeping custom tools.
- Pi has no built-in security sandbox; real isolation requires OS/container/VM boundary.

### Code intelligence candidate

- https://github.com/cortexkit/aft
- https://github.com/cortexkit/aft/blob/main/packages/pi-plugin/README.md

### Browser reference / proof of Pi ecosystem feasibility

- https://pi.dev/packages/pi-browser-cdp-extension

The standalone product should implement browser control directly; this package is a feasibility/reference point, not the required backend.

---

## 46. Intake instructions for the new repository

When the new repo exists:

1. Copy this masterplan into `docs/product/` as the operator source.
2. Run `/intake` with **first-intake-pack**.
3. Treat the current its-magic kit as an external kernel dependency/contract, not as backlog history to clone.
4. Map every row in the plan-area inventory to candidate stories or explicit deferral.
5. Produce full-plan coverage evidence.
6. Then run `/discovery` and `/research` focused first on:
   - Pi session/auth/tool APIs,
   - kernel consume contract,
   - security/resource loading,
   - AFT backend shape,
   - Playwright/CDP app/browser architecture.
7. Only then `/architecture` locks the first 12 decisions above.
8. Implement the **Phase 0 hard-proof spike before broad parity work**.

---

## 47. Final recommendation

The standalone its-magic agent should **not** be “Pi with our prompts.”

It should be:

```text
its-magic product logic
+ its-magic artifact/validator kernel
+ owned permissions/tools/orchestration/context/browser/runtime
+ Pi as a replaceable LLM/session engine
+ AFT initially as a replaceable code-intelligence backend
```

This preserves the strongest part of the existing framework — deterministic, artifact-first autonomous software delivery — while finally removing the weakest part: dependence on an IDE host obeying large prompt/rule files.

If the hard-proof spike passes, this is the recommended primary architecture for the standalone its-magic agent.
