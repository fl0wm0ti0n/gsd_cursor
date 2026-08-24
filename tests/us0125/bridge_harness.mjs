// US-0125 — Bridge harness for the Python contract test (marker 4 success
// test (b)). Reads the validator→artifact mapping fixture + drives the mock
// subprocess through the bridge contract. Asserts: non-zero → refuse
// persistence + raw Python reason code; subprocess throw → refuse +
// OPENCODE_DRIVER_INVOKE_FAILED; exit 0 → allow. No OpenCode runtime probe
// (AC-10). Plugin file (US-0124) stays as-is — US-0125 authors the contract
// + mapping data; US-0124 authors the hook.
import { pathToFileURL } from "node:url";
import { readFileSync } from "node:fs";

const MAPPING_PATH =
  "g:/workdir/github/sonstiges/gsd_cursor/tests/us0125/fixtures/validator_artifact_mapping.json";
const MOCK_PATH =
  "g:/workdir/github/sonstiges/gsd_cursor/tests/us0125/mock_subprocess.ts";

const scenario = process.argv[2];

function out(obj) {
  process.stdout.write(JSON.stringify(obj));
  process.stdout.write("\n");
}

async function main() {
  const mockMod = await import(pathToFileURL(MOCK_PATH).href);
  const mapping = JSON.parse(readFileSync(MAPPING_PATH, "utf-8"));

  // Resolve a validator argv for a given artifact path from the mapping.
  function resolveValidatorArgv(artifactPath) {
    for (const row of mapping.rows) {
      if (row.artifact_path.includes(artifactPath) || artifactPath.includes(row.artifact_path.split(" ")[0])) {
        // Tokenize the validator_cli into argv (split on spaces; in production
        // the plugin builds argv from the mapping row + repo path).
        return row.validator_cli.split(/\s+/);
      }
    }
    return null;
  }

  if (scenario === "static-info") {
    out({
      rowCount: mapping.rows.length,
      bridges: mapping.rows.map((r) => r.bridge),
      reasonCodes: mapping.rows.flatMap((r) => r.reason_codes),
    });
    return;
  }

  // Success test (b): non-zero exit on a release-persistence artifact path
  // → bridge refuses write + emits raw Python reason code (not a wrapper).
  if (scenario === "release-blocked-nonzero") {
    const artifactPath = "handoffs/release_queue.md";
    // The release path is gated by bug_issue_validate.py per the mapping
    // (release command body says bug_issue_validate.py gates release writes).
    const validatorArgv = "python scripts/bug_issue_validate.py --repo . --check-acceptance".split(/\s+/);
    const mock = mockMod.createMockSubprocess({
      nextExitCode: 1,
      nextStderr: "INTAKE_PERSISTENCE_BLOCKED",
    });
    const result = mockMod.bridgeEnforceWrite(validatorArgv, mock.spawn);
    out({
      allowed: result.allowed,
      reasonCode: result.reasonCode,
      validatorArgv: result.validatorArgv,
      calls: mock.calls,
    });
    return;
  }

  // Subprocess throw → OPENCODE_DRIVER_INVOKE_FAILED + refuse write.
  if (scenario === "release-blocked-throw") {
    const validatorArgv = "python scripts/intake_evidence_validate.py --repo . --enforce".split(/\s+/);
    const mock = mockMod.createMockSubprocess({ nextThrow: true });
    const result = mockMod.bridgeEnforceWrite(validatorArgv, mock.spawn);
    out({
      allowed: result.allowed,
      reasonCode: result.reasonCode,
      validatorArgv: result.validatorArgv,
      calls: mock.calls,
    });
    return;
  }

  // Exit 0 → allow.
  if (scenario === "release-allowed") {
    const validatorArgv = "python scripts/intake_evidence_validate.py --repo . --enforce".split(/\s+/);
    const mock = mockMod.createMockSubprocess({ nextExitCode: 0 });
    const result = mockMod.bridgeEnforceWrite(validatorArgv, mock.spawn);
    out({
      allowed: result.allowed,
      reasonCode: result.reasonCode,
      validatorArgv: result.validatorArgv,
      calls: mock.calls,
    });
    return;
  }

  // Mapping fixture resolves validator argv for a known artifact path.
  if (scenario === "mapping-resolve") {
    const argv = resolveValidatorArgv("handoffs/intake_evidence");
    out({ argv, found: argv !== null });
    return;
  }

  out({ error: "unknown scenario: " + scenario });
  process.exit(1);
}

main().catch((err) => {
  out({ error: String(err && err.message ? err.message : err) });
  process.exit(1);
});
