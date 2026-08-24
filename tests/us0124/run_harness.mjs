// US-0124 — Node harness for the Python contract test. Imports the
// orchestrator plugin (template/.opencode/plugins/orchestrator.ts) and the
// MockCtx (tests/us0124/mock_ctx.ts) under --experimental-strip-types, runs
// the scenario named by argv[2], and prints a JSON result to stdout.
import { pathToFileURL } from "node:url";

const PLUGIN_PATH =
  "g:/workdir/github/sonstiges/gsd_cursor/template/.opencode/plugins/orchestrator.ts";
const MOCK_PATH =
  "g:/workdir/github/sonstiges/gsd_cursor/tests/us0124/mock_ctx.ts";

const scenario = process.argv[2];

function out(obj) {
  process.stdout.write(JSON.stringify(obj));
  process.stdout.write("\n");
}

async function main() {
  const plugin = await import(pathToFileURL(PLUGIN_PATH).href);
  const mockMod = await import(pathToFileURL(MOCK_PATH).href);

  if (scenario === "static-info") {
    out({
      id: plugin.default?.id,
      reasonCodes: plugin.REASON_CODES,
      matrixPhases: Object.keys(plugin.PHASE_ROLE_MATRIX),
      hasSetup: typeof plugin.default?.setup === "function",
      hasSpawnPhase: typeof plugin.spawnPhase === "function",
      hasBuildHeadlessArgv: typeof plugin.buildHeadlessArgv === "function",
      hasInvokeHeadless: typeof plugin.invokeHeadless === "function",
      hasDispatchStopMatrix: typeof plugin.dispatchStopMatrix === "function",
    });
    return;
  }

  if (scenario === "build-argv") {
    out({ argv: plugin.buildHeadlessArgv("phase-prompt-here").argv });
    return;
  }

  if (scenario === "invoke-headless-missing") {
    const r = plugin.invokeHeadless("p", { resolveBinary: () => null });
    out(r);
    return;
  }

  if (scenario === "invoke-headless-ok") {
    const r = plugin.invokeHeadless("p", {
      resolveBinary: () => "/usr/bin/opencode",
      spawnFn: () => ({ status: 0, stdout: '[{"type":"message"}]', stderr: "" }),
    });
    out(r);
    return;
  }

  if (scenario === "dispatch-stop-matrix-ok") {
    const r = plugin.dispatchStopMatrix(
      { phase: "execute", role: "dev", story: "US-0124", sprint: "S0124" },
      {
        spawnFn: () => ({
          status: 0,
          stdout:
            '{"action":"spawn_next","next_phase":"qa","stop_reason":"completed"}',
          stderr: "",
        }),
      },
    );
    out(r);
    return;
  }

  if (scenario === "dispatch-stop-matrix-fail") {
    const r = plugin.dispatchStopMatrix(
      { phase: "execute", role: "dev" },
      { spawnFn: () => ({ status: 1, stdout: "", stderr: "boom" }) },
    );
    out(r);
    return;
  }

  if (scenario === "dispatch-stop-matrix-malformed") {
    const r = plugin.dispatchStopMatrix(
      { phase: "execute", role: "dev" },
      { spawnFn: () => ({ status: 0, stdout: "not-json", stderr: "" }) },
    );
    out(r);
    return;
  }

  // spawn scenarios
  const cfg = {};
  if (scenario === "spawn-null") cfg.returnNull = true;
  if (scenario === "spawn-throw-generic") cfg.throwOnCreate = true;
  if (scenario === "spawn-throw-missing-primitive") {
    cfg.throwOnCreate = true;
    cfg.throwMissingPrimitive = true;
  }
  if (scenario === "spawn-identical-id") cfg.identicalID = true;

  let ctx;
  if (scenario === "spawn-no-create") {
    ctx = { tool: { hook: () => {} }, session: {} };
  } else {
    ctx = mockMod.createMockCtx(cfg);
  }

  const api = plugin.default.setup(ctx);
  const args = {
    phaseId: scenario === "spawn-unknown-phase" ? "bogus-phase" : "execute",
    prompt: "phase-prompt",
    orchestratorSessionId: mockMod.MOCK_ORCHESTRATOR_SESSION_ID,
    freshContextMarker: "dev-US0124-execute-20260824T184700Z-fresh",
    storyId: "US-0124",
    sprintId: "S0124",
    orchestratorRunId: "auto-20260824-02",
  };
  const r = await api.spawnPhase(args);
  out({
    ok: r.ok,
    reasonCode: r.reasonCode,
    sessionID: r.sessionID,
    evidence: r.evidence,
    createCalls: ctx._calls ? ctx._calls.create : undefined,
  });
}

main().catch((err) => {
  out({ error: String(err && err.message ? err.message : err) });
  process.exit(1);
});
