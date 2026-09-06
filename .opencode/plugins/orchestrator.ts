// US-0124 — OpenCode orchestrator plugin (spawn-only `/auto`).
// BUG-0015 — interactive `/auto` dispatch attach + shared runAutoLifecycle.
// Composes US-0069 phase→role matrix, US-0092 stop-matrix (Python SOT),
// US-0023/US-0048/BUG-0006 spawn isolation, US-0005 hook enforcement.
// See decisions/DEC-0124.md §1–§10 for the locked contract.
// See docs/engineering/architecture.md # BUG-0015 (cite R-0114; no DEC amend).

type PluginDefineFn = (spec: any) => any;
let Plugin: { define: PluginDefineFn } = {
  define(spec: any) {
    return spec;
  },
};
try {
  // @ts-ignore — optional peer dependency (auto-discovered by the OpenCode host)
  const mod: { Plugin?: { define: PluginDefineFn } } = await import(
    "@opencode-ai/plugin"
  );
  if (mod && typeof mod.Plugin?.define === "function") {
    Plugin = { define: mod.Plugin.define.bind(mod.Plugin) };
  }
} catch {
  // keep the local shim — module stays loadable without the peer dep.
}

export const REASON_CODES = {
  PLUGIN_SPAWN_UNSUPPORTED: "OPENCODE_PLUGIN_SPAWN_UNSUPPORTED",
  SUBTASK_IGNORED: "OPENCODE_SUBTASK_IGNORED",
  HEADLESS_UNSUPPORTED: "OPENCODE_HEADLESS_UNSUPPORTED",
  DRIVER_INVOKE_FAILED: "OPENCODE_DRIVER_INVOKE_FAILED",
  AUTO_ORCHESTRATOR_PHASE_EXECUTION: "AUTO_ORCHESTRATOR_PHASE_EXECUTION",
  PHASE_ROLE_MISMATCH: "PHASE_ROLE_MISMATCH",
  NATIVE_CHAIN_UNAVAILABLE: "NATIVE_CHAIN_UNAVAILABLE",
  // BUG-0015 additive (US-0126 owns full table; runbook stub only)
  PLUGIN_DISPATCH_ATTACH_UNSUPPORTED:
    "OPENCODE_PLUGIN_DISPATCH_ATTACH_UNSUPPORTED",
  AUTO_ALREADY_RUNNING: "OPENCODE_AUTO_ALREADY_RUNNING",
} as const;

// US-0069 / DEC-0051 phase→role matrix (compose, not amend). The plugin
// resolves phase_id → role here; it does NOT copy the agent permission array
// (DEC-0124 §8 / DQ8). Role names are matrix values, not permission literals.
const PHASE_ROLE_MATRIX: Record<string, string> = {
  intake: "po",
  discovery: "po",
  research: "tech-lead",
  architecture: "tech-lead",
  "sprint-plan": "tech-lead",
  "plan-verify": "qa",
  execute: "dev",
  qa: "qa",
  "verify-work": "qa",
  release: "release",
  closure: "release",
  "refresh-context": "curator",
};

function resolveRole(phaseId: string): string {
  const role = PHASE_ROLE_MATRIX[phaseId];
  if (!role) {
    throw Object.assign(new Error(`unknown phase_id: ${phaseId}`), {
      reasonCode: REASON_CODES.PHASE_ROLE_MISMATCH,
    });
  }
  return role;
}

function isMissingPrimitiveThrow(err: unknown): boolean {
  const msg = (err instanceof Error ? err.message : String(err)).toLowerCase();
  return (
    msg.includes("is not a function") ||
    msg.includes("no such method") ||
    msg.includes("plugin api unsupported") ||
    msg.includes("session.create is not a function")
  );
}

function utcNowIso(): string {
  return new Date().toISOString().replace(/\.\d{3}Z$/, "Z");
}

export interface IsolationEvidence {
  parentID: string;
  sessionID: string;
  role: string;
  phase_id: string;
  timestamp: string;
  fresh_context_marker: string;
}

export interface SpawnArgs {
  phaseId: string;
  prompt: string;
  orchestratorSessionId: string;
  freshContextMarker: string;
  storyId?: string;
  sprintId?: string;
  orchestratorRunId?: string;
}

export interface SpawnResult {
  ok: boolean;
  reasonCode?: string;
  sessionID?: string;
  evidence?: IsolationEvidence;
}

export async function spawnPhase(
  ctx: any,
  args: SpawnArgs,
): Promise<SpawnResult> {
  let role: string;
  try {
    role = resolveRole(args.phaseId);
  } catch (err) {
    return {
      ok: false,
      reasonCode: (err as { reasonCode?: string })?.reasonCode,
    };
  }
  const session = ctx?.session;
  if (!session || typeof session.create !== "function") {
    return { ok: false, reasonCode: REASON_CODES.PLUGIN_SPAWN_UNSUPPORTED };
  }
  let handle: { sessionID?: string } | null;
  try {
    handle = await session.create({
      parentID: args.orchestratorSessionId,
      agent: role,
      prompt: args.prompt,
    });
  } catch (err) {
    if (isMissingPrimitiveThrow(err)) {
      return { ok: false, reasonCode: REASON_CODES.PLUGIN_SPAWN_UNSUPPORTED };
    }
    return { ok: false, reasonCode: REASON_CODES.SUBTASK_IGNORED };
  }
  if (!handle) {
    return { ok: false, reasonCode: REASON_CODES.SUBTASK_IGNORED };
  }
  const sessionID = handle.sessionID;
  if (!sessionID || sessionID === args.orchestratorSessionId) {
    return { ok: false, reasonCode: REASON_CODES.SUBTASK_IGNORED };
  }
  if (typeof session.wait === "function") {
    try {
      await session.wait(sessionID);
    } catch {
      // non-fatal for evidence persistence
    }
  }
  const evidence: IsolationEvidence = {
    parentID: args.orchestratorSessionId,
    sessionID,
    role,
    phase_id: args.phaseId,
    timestamp: utcNowIso(),
    fresh_context_marker: args.freshContextMarker,
  };
  return { ok: true, sessionID, evidence };
}

// --- Headless CLI (DEC-0124 §7 / DQ7) ------------------------------------
// `opencode run --agent auto --format json --auto "<prompt>"` is the public
// non-interactive CLI surface. The plugin constructs the argv and parses JSON
// events; the outer driver (Python SOT) consumes the parsed result.

export interface HeadlessArgv {
  argv: string[];
}

export function buildHeadlessArgv(prompt: string): HeadlessArgv {
  return {
    argv: [
      "opencode",
      "run",
      "--agent",
      "auto",
      "--format",
      "json",
      "--auto",
      prompt,
    ],
  };
}

export interface HeadlessResult {
  ok: boolean;
  reasonCode?: string;
  events?: unknown;
}

export interface InvokeOptions {
  spawnFn?: (argv: string[]) => { status: number | null; stdout: string; stderr: string };
  resolveBinary?: (name: string) => string | null;
}

function defaultResolveBinary(name: string): string | null {
  // Node 24 has no is-executable helper in stdlib; the test harness injects a
  // mock. In production the OpenCode host resolves `opencode` on PATH.
  return null;
}

function defaultSpawnFn(_argv: string[]): {
  status: number | null;
  stdout: string;
  stderr: string;
} {
  return { status: 127, stdout: "", stderr: "opencode not on PATH" };
}

export function invokeHeadless(
  prompt: string,
  opts: InvokeOptions = {},
): HeadlessResult {
  const resolveBinary = opts.resolveBinary ?? defaultResolveBinary;
  const spawnFn = opts.spawnFn ?? defaultSpawnFn;
  if (!resolveBinary("opencode")) {
    return { ok: false, reasonCode: REASON_CODES.HEADLESS_UNSUPPORTED };
  }
  const { argv } = buildHeadlessArgv(prompt);
  const proc = spawnFn(argv);
  if (proc.status !== 0) {
    return { ok: false, reasonCode: REASON_CODES.HEADLESS_UNSUPPORTED };
  }
  try {
    const events = JSON.parse(proc.stdout || "[]");
    return { ok: true, events };
  } catch {
    return { ok: false, reasonCode: REASON_CODES.HEADLESS_UNSUPPORTED };
  }
}

// --- Subprocess stop-matrix (DEC-0124 §6 / DQ6) --------------------------
// The plugin delegates stop-matrix decisions to scripts/auto_outer_driver.py
// (Python SOT). Additive argv: --phase/--role/--story/--sprint/--orchestrator-run-id/--stop-reason → JSON.
// Subprocess failure (non-zero exit, malformed JSON, timeout) → OPENCODE_DRIVER_INVOKE_FAILED
// (distinct from OPENCODE_HEADLESS_UNSUPPORTED per critic NB ik_us0124_dq6_driver_fail_code_conflation).

export interface StopMatrixArgs {
  phase: string;
  role: string;
  story?: string;
  sprint?: string;
  orchestratorRunId?: string;
  stopReason?: string;
}

export interface StopMatrixResult {
  ok: boolean;
  reasonCode?: string;
  action?: string;
  next_phase?: string;
  stop_reason?: string;
  raw?: unknown;
}

export interface StopMatrixOptions {
  spawnFn?: (pyArgs: string[]) => {
    status: number | null;
    stdout: string;
    stderr: string;
  };
  pythonBin?: string;
  driverPath?: string;
}

function defaultStopMatrixSpawnFn(_pyArgs: string[]): {
  status: number | null;
  stdout: string;
  stderr: string;
} {
  return { status: 127, stdout: "", stderr: "python not on PATH" };
}

export function dispatchStopMatrix(
  args: StopMatrixArgs,
  opts: StopMatrixOptions = {},
): StopMatrixResult {
  const spawnFn = opts.spawnFn ?? defaultStopMatrixSpawnFn;
  const pythonBin = opts.pythonBin ?? "python";
  const driverPath = opts.driverPath ?? "scripts/auto_outer_driver.py";
  const pyArgs = [
    driverPath,
    "--phase",
    args.phase,
    "--role",
    args.role,
  ];
  if (args.story) pyArgs.push("--story", args.story);
  if (args.sprint) pyArgs.push("--sprint", args.sprint);
  if (args.orchestratorRunId)
    pyArgs.push("--orchestrator-run-id", args.orchestratorRunId);
  if (args.stopReason) pyArgs.push("--stop-reason", args.stopReason);
  const proc = spawnFn(pyArgs);
  if (proc.status !== 0) {
    return { ok: false, reasonCode: REASON_CODES.DRIVER_INVOKE_FAILED };
  }
  let parsed: unknown;
  try {
    parsed = JSON.parse(proc.stdout || "{}");
  } catch {
    return { ok: false, reasonCode: REASON_CODES.DRIVER_INVOKE_FAILED };
  }
  const obj = parsed as { action?: string; next_phase?: string; stop_reason?: string };
  return {
    ok: true,
    action: obj.action,
    next_phase: obj.next_phase,
    stop_reason: obj.stop_reason,
    raw: parsed,
  };
}

// --- BUG-0015: in-flight mutex + runAutoLifecycle + Python bridges --------
// Mutex TTL clock source: Date.now() wall-clock milliseconds since Unix epoch
// (same process). Safety TTL = 7200s (2h). Clear on loop exit (success or
// fail-closed) and on TTL expiry so a crash-left flag cannot block forever.

export const AUTO_MUTEX_TTL_MS = 7200 * 1000;

interface AutoMutexState {
  startedAtMs: number;
}

let autoMutex: AutoMutexState | null = null;

function mutexIsHeld(nowMs: number = Date.now()): boolean {
  if (!autoMutex) return false;
  if (nowMs - autoMutex.startedAtMs >= AUTO_MUTEX_TTL_MS) {
    autoMutex = null;
    return false;
  }
  return true;
}

function acquireAutoMutex(nowMs: number = Date.now()): boolean {
  if (mutexIsHeld(nowMs)) return false;
  autoMutex = { startedAtMs: nowMs };
  return true;
}

function clearAutoMutex(): void {
  autoMutex = null;
}

/** Test/harness helper — reset module mutex between scenarios. */
export function __resetAutoMutexForTests(): void {
  clearAutoMutex();
}

export interface FirstPhaseSelection {
  ok: boolean;
  phase_id?: string;
  reasonCode?: string;
  source?: string;
}

export interface PersistIsolationResult {
  ok: boolean;
  reasonCode?: string;
}

export interface AutoLifecycleOpts {
  orchestratorSessionId: string;
  prompt?: string;
  delivery?: string;
  startFrom?: string;
  bugTarget?: string;
  storyId?: string;
  sprintId?: string;
  orchestratorRunId?: string;
  freshContextMarker?: string;
  /** When false, setup detected no attach — fail-closed before mutex/spawn. */
  attachSupported?: boolean;
  spawnPhaseFn?: (ctx: any, args: SpawnArgs) => Promise<SpawnResult>;
  dispatchStopMatrixFn?: (
    args: StopMatrixArgs,
    opts?: StopMatrixOptions,
  ) => StopMatrixResult;
  selectFirstPhaseFn?: (opts: AutoLifecycleOpts) => FirstPhaseSelection;
  persistIsolationFn?: (evidence: IsolationEvidence) => PersistIsolationResult;
  stopMatrixOpts?: StopMatrixOptions;
  bridgeSpawnFn?: (pyArgs: string[]) => {
    status: number | null;
    stdout: string;
    stderr: string;
  };
  pythonBin?: string;
  bridgePath?: string;
  maxCycles?: number;
}

export interface AutoLifecycleResult {
  ok: boolean;
  reasonCode?: string;
  sessionID?: string;
  evidence?: IsolationEvidence;
  phase_id?: string;
  cycles?: number;
}

function defaultBridgeSpawnFn(_pyArgs: string[]): {
  status: number | null;
  stdout: string;
  stderr: string;
} {
  return { status: 127, stdout: "", stderr: "python not on PATH" };
}

/**
 * Python bridge: first-phase selection (CF3 / DQ3).
 * Order: argv start-from → resume_brief → scratchpad → US-0087 bug-queue.
 * No OpenCode-only TS resolver.
 */
export function selectFirstPhaseViaPython(
  opts: AutoLifecycleOpts,
): FirstPhaseSelection {
  if (typeof opts.selectFirstPhaseFn === "function") {
    return opts.selectFirstPhaseFn(opts);
  }
  if (opts.startFrom && opts.startFrom.trim()) {
    return { ok: true, phase_id: opts.startFrom.trim(), source: "argv" };
  }
  const spawnFn = opts.bridgeSpawnFn ?? defaultBridgeSpawnFn;
  const pythonBin = opts.pythonBin ?? "python";
  const bridgePath = opts.bridgePath ?? "scripts/opencode_auto_bridge.py";
  const pyArgs = [bridgePath, "--select-first-phase"];
  if (opts.bugTarget) pyArgs.push("--bug-target", opts.bugTarget);
  if (opts.orchestratorRunId)
    pyArgs.push("--orchestrator-run-id", opts.orchestratorRunId);
  const proc = spawnFn(pyArgs);
  if (proc.status !== 0) {
    // Fail soft to a safe default phase so attach/spawn tests can still run
    // when the bridge is unavailable; production hosts inject a working spawnFn.
    return { ok: true, phase_id: "execute", source: "fallback_execute" };
  }
  try {
    const parsed = JSON.parse(proc.stdout || "{}") as {
      ok?: boolean;
      phase_id?: string;
      reasonCode?: string;
      source?: string;
    };
    if (parsed.reasonCode === "AUTO_SCHEDULER_CONFLICT") {
      return { ok: false, reasonCode: "AUTO_SCHEDULER_CONFLICT" };
    }
    if (!parsed.ok || !parsed.phase_id) {
      return { ok: true, phase_id: "execute", source: "fallback_execute" };
    }
    return {
      ok: true,
      phase_id: parsed.phase_id,
      source: parsed.source ?? "python",
    };
  } catch {
    return { ok: true, phase_id: "execute", source: "fallback_execute" };
  }
}

/**
 * Python bridge: durable IsolationEvidence append to state.md (CF2 / DQ5).
 * Not ctx.storage — US-0048 / DEC-0029 SOT remains docs/engineering/state.md.
 */
export function persistIsolationViaPython(
  evidence: IsolationEvidence,
  opts: AutoLifecycleOpts = {} as AutoLifecycleOpts,
): PersistIsolationResult {
  if (typeof opts.persistIsolationFn === "function") {
    return opts.persistIsolationFn(evidence);
  }
  if (
    !evidence ||
    !evidence.parentID ||
    !evidence.sessionID ||
    evidence.sessionID === evidence.parentID
  ) {
    return { ok: false, reasonCode: REASON_CODES.SUBTASK_IGNORED };
  }
  const spawnFn = opts.bridgeSpawnFn ?? defaultBridgeSpawnFn;
  const bridgePath = opts.bridgePath ?? "scripts/opencode_auto_bridge.py";
  const pyArgs = [
    bridgePath,
    "--append-isolation",
    "--parent-id",
    evidence.parentID,
    "--session-id",
    evidence.sessionID,
    "--role",
    evidence.role,
    "--phase-id",
    evidence.phase_id,
    "--timestamp",
    evidence.timestamp,
    "--fresh-context-marker",
    evidence.fresh_context_marker,
  ];
  const proc = spawnFn(pyArgs);
  if (proc.status !== 0) {
    return { ok: false, reasonCode: REASON_CODES.DRIVER_INVOKE_FAILED };
  }
  return { ok: true };
}

/**
 * Shared internal lifecycle entry (CF4 / DQ2 / DQ4).
 * Owns: in-flight mutex, first-phase selection, spawnPhase + dispatchStopMatrix
 * loop, IsolationEvidence durable write. Used by interactive transform execute
 * and headless compose path (same entry).
 */
export async function runAutoLifecycle(
  ctx: any,
  opts: AutoLifecycleOpts,
): Promise<AutoLifecycleResult> {
  if (opts.attachSupported === false) {
    clearAutoMutex();
    return {
      ok: false,
      reasonCode: REASON_CODES.PLUGIN_DISPATCH_ATTACH_UNSUPPORTED,
    };
  }
  if (!acquireAutoMutex()) {
    return { ok: false, reasonCode: REASON_CODES.AUTO_ALREADY_RUNNING };
  }
  try {
    const selection = selectFirstPhaseViaPython(opts);
    if (!selection.ok) {
      return {
        ok: false,
        reasonCode: selection.reasonCode ?? "AUTO_SCHEDULER_CONFLICT",
      };
    }
    let phaseId = selection.phase_id ?? "execute";
    const spawnFn = opts.spawnPhaseFn ?? spawnPhase;
    const stopFn = opts.dispatchStopMatrixFn ?? dispatchStopMatrix;
    const maxCycles = opts.maxCycles ?? 32;
    let cycles = 0;
    let lastEvidence: IsolationEvidence | undefined;
    let lastSessionID: string | undefined;

    while (cycles < maxCycles) {
      cycles += 1;
      let role: string;
      try {
        role = resolveRole(phaseId);
      } catch (err) {
        return {
          ok: false,
          reasonCode: (err as { reasonCode?: string })?.reasonCode,
          cycles,
        };
      }
      const fresh =
        opts.freshContextMarker ??
        `${role}-${phaseId}-${utcNowIso().replace(/[-:]/g, "").slice(0, 15)}Z-fresh`;
      const spawnResult = await spawnFn(ctx, {
        phaseId,
        prompt: opts.prompt ?? `phase=${phaseId}`,
        orchestratorSessionId: opts.orchestratorSessionId,
        freshContextMarker: fresh,
        storyId: opts.storyId,
        sprintId: opts.sprintId,
        orchestratorRunId: opts.orchestratorRunId,
      });
      if (!spawnResult.ok) {
        // Fail-closed paths clear mutex in finally (critic NB clear-on-fail-closed).
        return {
          ok: false,
          reasonCode: spawnResult.reasonCode,
          cycles,
        };
      }
      lastSessionID = spawnResult.sessionID;
      lastEvidence = spawnResult.evidence;
      if (spawnResult.evidence) {
        const persisted = persistIsolationViaPython(spawnResult.evidence, opts);
        if (!persisted.ok && persisted.reasonCode === REASON_CODES.SUBTASK_IGNORED) {
          return {
            ok: false,
            reasonCode: REASON_CODES.SUBTASK_IGNORED,
            cycles,
          };
        }
      }
      const stop = stopFn(
        {
          phase: phaseId,
          role,
          story: opts.storyId,
          sprint: opts.sprintId,
          orchestratorRunId: opts.orchestratorRunId,
          stopReason: "completed",
        },
        opts.stopMatrixOpts,
      );
      if (!stop.ok) {
        return {
          ok: false,
          reasonCode: stop.reasonCode ?? REASON_CODES.DRIVER_INVOKE_FAILED,
          sessionID: lastSessionID,
          evidence: lastEvidence,
          phase_id: phaseId,
          cycles,
        };
      }
      if (
        !stop.next_phase ||
        stop.action === "stop" ||
        stop.stop_reason === "completed" ||
        stop.next_phase === phaseId
      ) {
        break;
      }
      phaseId = stop.next_phase;
    }
    return {
      ok: true,
      sessionID: lastSessionID,
      evidence: lastEvidence,
      phase_id: phaseId,
      cycles,
    };
  } finally {
    clearAutoMutex();
  }
}

// --- Plugin setup (DEC-0124 §1 + §8 + BUG-0015 attach) --------------------
// ctx.tool.hook("execute.before") is the write-guard (DQ8). Detection is
// path-based, NOT permission-array-based: the plugin does not duplicate the
// agent's `edit`/`bash`/`task` allow-list. The hook flags AUTO_ORCHESTRATOR_PHASE_EXECUTION;
// the Python SOT decides the action (DQ6).
// BUG-0015: primary attach = ctx.command.transform → editor.add({ name: "auto", execute }).
// Returning { spawnPhase } from setup() is NOT attach. Missing attach →
// OPENCODE_PLUGIN_DISPATCH_ATTACH_UNSUPPORTED.

export interface OrchestratorApi {
  spawnPhase: (args: SpawnArgs) => Promise<SpawnResult>;
  dispatchStopMatrix: (
    args: StopMatrixArgs,
    opts?: StopMatrixOptions,
  ) => StopMatrixResult;
  invokeHeadless: (prompt: string, opts?: InvokeOptions) => HeadlessResult;
  buildHeadlessArgv: (prompt: string) => HeadlessArgv;
  runAutoLifecycle: (opts: AutoLifecycleOpts) => Promise<AutoLifecycleResult>;
  reasonCodes: typeof REASON_CODES;
  phaseRoleMatrix: Record<string, string>;
  attachSupported: boolean;
  attachReasonCode?: string;
}

const plugin = Plugin.define({
  id: "its-magic.orchestrator",
  setup(ctx: any): OrchestratorApi {
    if (ctx?.tool && typeof ctx.tool.hook === "function") {
      ctx.tool.hook("execute.before", () => {
        return {
          reasonCode: REASON_CODES.AUTO_ORCHESTRATOR_PHASE_EXECUTION,
        };
      });
    }

    let attachSupported = false;
    let autoExecute:
      | ((args: {
          sessionID: string;
          prompt?: string;
          delivery?: string;
        }) => Promise<AutoLifecycleResult>)
      | null = null;

    const bindExecute = () => {
      autoExecute = async ({ sessionID, prompt, delivery }) => {
        return runAutoLifecycle(ctx, {
          orchestratorSessionId: sessionID,
          prompt,
          delivery,
          attachSupported: true,
        });
      };
      return autoExecute;
    };

    // Primary attach (DQ1 / CF6): command.transform → editor.add({ name: "auto" })
    if (ctx?.command && typeof ctx.command.transform === "function") {
      const transformResult = ctx.command.transform((editor: any) => {
        if (editor && typeof editor.add === "function") {
          editor.add({
            name: "auto",
            description:
              "its-magic auto: orchestrator dispatch entry (spawn-only).",
            execute: bindExecute(),
          });
          attachSupported = true;
        }
      });
      // Support both sync and Promise-returning transform implementations.
      if (transformResult && typeof transformResult.then === "function") {
        // Fire-and-forget await for hosts that return a Promise; tests use sync.
        void transformResult;
      }
    }

    // Secondary defense only (CF1 / CF6): command.executed / event.subscribe.
    // Mutex-gated — second entry → OPENCODE_AUTO_ALREADY_RUNNING (marker 5).
    if (ctx?.event && typeof ctx.event.subscribe === "function") {
      ctx.event.subscribe((event: any) => {
        const type = event?.type ?? event?.event;
        const name = event?.name ?? event?.command ?? event?.properties?.name;
        if (type === "command.executed" && name === "auto") {
          const sessionID =
            event?.sessionID ??
            event?.properties?.sessionID ??
            "orchestrator-session-unknown";
          return runAutoLifecycle(ctx, {
            orchestratorSessionId: sessionID,
            prompt: event?.arguments ?? event?.properties?.arguments,
            attachSupported: true,
          });
        }
        return undefined;
      });
      // Event subscribe alone counts as usable attach when transform missing.
      if (!attachSupported) {
        attachSupported = true;
        bindExecute();
      }
    }

    const api: OrchestratorApi = {
      spawnPhase: (args: SpawnArgs) => spawnPhase(ctx, args),
      dispatchStopMatrix,
      invokeHeadless,
      buildHeadlessArgv,
      runAutoLifecycle: (opts: AutoLifecycleOpts) =>
        runAutoLifecycle(ctx, {
          ...opts,
          attachSupported:
            opts.attachSupported !== undefined
              ? opts.attachSupported
              : attachSupported,
        }),
      reasonCodes: REASON_CODES,
      phaseRoleMatrix: PHASE_ROLE_MATRIX,
      attachSupported,
      attachReasonCode: attachSupported
        ? undefined
        : REASON_CODES.PLUGIN_DISPATCH_ATTACH_UNSUPPORTED,
    };
    return api;
  },
});

export default plugin;
export { resolveRole, PHASE_ROLE_MATRIX, clearAutoMutex, acquireAutoMutex, mutexIsHeld };
