// BUG-0015 — Node harness for the Python contract test. Imports the
// orchestrator plugin (template/.opencode/plugins/orchestrator.ts) and the
// MockCtx (tests/us0124/mock_ctx.ts, extended additively) under
// --experimental-strip-types. No live OpenCode runtime probe.
import { pathToFileURL } from "node:url";
import { dirname, join } from "node:path";
import { fileURLToPath } from "node:url";

const __dirname = dirname(fileURLToPath(import.meta.url));
const REPO_ROOT = join(__dirname, "..", "..");
const PLUGIN_PATH = join(
  REPO_ROOT,
  "template",
  ".opencode",
  "plugins",
  "orchestrator.ts",
);
const MOCK_PATH = join(REPO_ROOT, "tests", "us0124", "mock_ctx.ts");

const scenario = process.argv[2];

function out(obj) {
  process.stdout.write(JSON.stringify(obj));
  process.stdout.write("\n");
}

async function main() {
  const plugin = await import(pathToFileURL(PLUGIN_PATH).href);
  const mockMod = await import(pathToFileURL(MOCK_PATH).href);
  plugin.__resetAutoMutexForTests?.();

  if (scenario === "static-info") {
    out({
      id: plugin.default?.id,
      reasonCodes: plugin.REASON_CODES,
      hasSetup: typeof plugin.default?.setup === "function",
      hasSpawnPhase: typeof plugin.spawnPhase === "function",
      hasRunAutoLifecycle: typeof plugin.runAutoLifecycle === "function",
      hasDispatchStopMatrix: typeof plugin.dispatchStopMatrix === "function",
      mutexTtlMs: plugin.AUTO_MUTEX_TTL_MS,
    });
    return;
  }

  const stopOk = () => ({
    status: 0,
    stdout: JSON.stringify({
      action: "stop",
      next_phase: null,
      stop_reason: "completed",
    }),
    stderr: "",
  });

  const persistOk = () => ({ status: 0, stdout: '{"ok":true}', stderr: "" });

  if (scenario === "attach-registers-auto") {
    const ctx = mockMod.createMockCtx({}, "phase-complete", {
      withCommandTransform: true,
    });
    const api = plugin.default.setup(ctx);
    out({
      attachSupported: api.attachSupported,
      attachReasonCode: api.attachReasonCode ?? null,
      editorAddNames: ctx._calls.editorAdd.map((d) => d.name),
      hasExecute: typeof ctx._autoExecute === "function",
      transformRegistered: ctx._calls.editorAdd.length > 0,
    });
    return;
  }

  if (scenario === "execute-invokes-spawn") {
    const ctx = mockMod.createMockCtx({}, "phase-complete", {
      withCommandTransform: true,
    });
    const api = plugin.default.setup(ctx);
    const r = await api.runAutoLifecycle({
      orchestratorSessionId: mockMod.MOCK_ORCHESTRATOR_SESSION_ID,
      prompt: "run-auto",
      startFrom: "execute",
      storyId: "BUG-0015",
      sprintId: "S0131",
      orchestratorRunId: "auto-20260906-bug0015",
      freshContextMarker: "dev-BUG0015-execute-20260906T144000Z-fresh",
      bridgeSpawnFn: persistOk,
      stopMatrixOpts: { spawnFn: stopOk },
      persistIsolationFn: () => ({ ok: true }),
    });
    out({
      ok: r.ok,
      reasonCode: r.reasonCode ?? null,
      sessionID: r.sessionID ?? null,
      createCalls: ctx._calls.create,
      evidence: r.evidence ?? null,
    });
    return;
  }

  if (scenario === "missing-attach") {
    const ctx = mockMod.createMockCtx({}, "phase-complete", {
      withCommandTransform: false,
      withEventSubscribe: false,
    });
    // Strip command/event if present
    delete ctx.command;
    delete ctx.event;
    const api = plugin.default.setup(ctx);
    const r = await api.runAutoLifecycle({
      orchestratorSessionId: mockMod.MOCK_ORCHESTRATOR_SESSION_ID,
      prompt: "should-fail",
    });
    out({
      attachSupported: api.attachSupported,
      attachReasonCode: api.attachReasonCode ?? null,
      ok: r.ok,
      reasonCode: r.reasonCode ?? null,
    });
    return;
  }

  if (scenario === "missing-session-create") {
    const ctx = mockMod.createMockCtx({}, "phase-complete", {
      withCommandTransform: true,
    });
    const api = plugin.default.setup(ctx);
    // Attach ok, but remove session.create
    ctx.session = {};
    const r = await api.runAutoLifecycle({
      orchestratorSessionId: mockMod.MOCK_ORCHESTRATOR_SESSION_ID,
      prompt: "should-fail-spawn",
      startFrom: "execute",
      persistIsolationFn: () => ({ ok: true }),
      stopMatrixOpts: { spawnFn: stopOk },
    });
    out({
      attachSupported: api.attachSupported,
      ok: r.ok,
      reasonCode: r.reasonCode ?? null,
    });
    return;
  }

  if (scenario === "concurrent-reentry") {
    const ctx = mockMod.createMockCtx({}, "phase-complete", {
      withCommandTransform: true,
      withEventSubscribe: true,
    });
    let releaseWait;
    const gate = new Promise((resolve) => {
      releaseWait = resolve;
    });
    ctx._setWaitGate(gate);
    const api = plugin.default.setup(ctx);

    const first = api.runAutoLifecycle({
      orchestratorSessionId: mockMod.MOCK_ORCHESTRATOR_SESSION_ID,
      prompt: "first",
      startFrom: "execute",
      persistIsolationFn: () => ({ ok: true }),
      stopMatrixOpts: { spawnFn: stopOk },
    });

    // Yield so first acquires mutex and reaches session.wait
    await new Promise((r) => setTimeout(r, 30));

    const second = await api.runAutoLifecycle({
      orchestratorSessionId: mockMod.MOCK_ORCHESTRATOR_SESSION_ID,
      prompt: "second",
      startFrom: "execute",
      persistIsolationFn: () => ({ ok: true }),
      stopMatrixOpts: { spawnFn: stopOk },
    });

    // Dual-fire secondary command.executed while first still in-flight (R1/R2)
    const eventResult = await ctx._eventHandler({
      type: "command.executed",
      name: "auto",
      sessionID: mockMod.MOCK_ORCHESTRATOR_SESSION_ID,
    });

    releaseWait();
    const firstResult = await first;

    out({
      firstOk: firstResult.ok,
      secondOk: second.ok,
      secondReasonCode: second.reasonCode ?? null,
      eventOk: eventResult ? eventResult.ok : null,
      eventReasonCode: eventResult ? eventResult.reasonCode ?? null : null,
      expectedAlreadyRunning: "OPENCODE_AUTO_ALREADY_RUNNING",
    });
    return;
  }

  out({ error: `unknown scenario: ${scenario}` });
  process.exit(1);
}

main().catch((err) => {
  out({ error: String(err && err.message ? err.message : err) });
  process.exit(1);
});
