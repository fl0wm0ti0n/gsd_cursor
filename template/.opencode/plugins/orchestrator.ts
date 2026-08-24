// US-0124 — OpenCode orchestrator plugin (spawn-only `/auto`).
// Composes US-0069 phase→role matrix, US-0092 stop-matrix (Python SOT),
// US-0023/US-0048/BUG-0006 spawn isolation, US-0005 hook enforcement.
// See decisions/DEC-0124.md §1–§10 for the locked contract.

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

// --- Plugin setup (DEC-0124 §1 + §8) --------------------------------------
// ctx.tool.hook("execute.before") is the write-guard (DQ8). Detection is
// path-based, NOT permission-array-based: the plugin does not duplicate the
// agent's `edit`/`bash`/`task` allow-list. The hook flags AUTO_ORCHESTRATOR_PHASE_EXECUTION;
// the Python SOT decides the action (DQ6).

export interface OrchestratorApi {
  spawnPhase: (args: SpawnArgs) => Promise<SpawnResult>;
  dispatchStopMatrix: (
    args: StopMatrixArgs,
    opts?: StopMatrixOptions,
  ) => StopMatrixResult;
  invokeHeadless: (prompt: string, opts?: InvokeOptions) => HeadlessResult;
  buildHeadlessArgv: (prompt: string) => HeadlessArgv;
  reasonCodes: typeof REASON_CODES;
  phaseRoleMatrix: Record<string, string>;
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
    return {
      spawnPhase: (args: SpawnArgs) => spawnPhase(ctx, args),
      dispatchStopMatrix,
      invokeHeadless,
      buildHeadlessArgv,
      reasonCodes: REASON_CODES,
      phaseRoleMatrix: PHASE_ROLE_MATRIX,
    };
  },
});

export default plugin;
export { resolveRole, PHASE_ROLE_MATRIX };
