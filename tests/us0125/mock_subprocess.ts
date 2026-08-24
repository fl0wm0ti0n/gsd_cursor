// US-0125 — Mock subprocess harness for the validator bridge contract
// (DEC-0125 §8 / DQ8). Reuses the US-0124 MockCtx pattern; additive, US-0124
// surface unchanged. The mock subprocess accepts a scripted nextExitCode
// (0 or non-zero) + nextStderr (raw Python reason code) + nextThrow (for
// OPENCODE_DRIVER_INVOKE_FAILED simulation). No live OpenCode runtime probe
// (AC-10) — CI runs pure Node (same as US-0124 DQ3).

export interface MockSubprocessConfig {
  nextExitCode?: number;
  nextStderr?: string;
  nextStdout?: string;
  nextThrow?: boolean;
}

export interface MockSubprocessCall {
  argv: string[];
}

export interface MockSubprocessResult {
  status: number | null;
  stdout: string;
  stderr: string;
}

export type MockSubprocessFn = (
  argv: string[],
) => MockSubprocessResult;

export function createMockSubprocess(
  config: MockSubprocessConfig = {},
): {
  spawn: MockSubprocessFn;
  calls: MockSubprocessCall[];
  setConfig: (cfg: MockSubprocessConfig) => void;
  getConfig: () => MockSubprocessConfig;
} {
  const calls: MockSubprocessCall[] = [];
  let cfg: MockSubprocessConfig = { ...config };
  const spawn = (argv: string[]): MockSubprocessResult => {
    calls.push({ argv: [...argv] });
    if (cfg.nextThrow) {
      throw new Error("subprocess invocation failed (mock)");
    }
    return {
      status: cfg.nextExitCode ?? 0,
      stdout: cfg.nextStdout ?? "",
      stderr: cfg.nextStderr ?? "",
    };
  };
  return {
    spawn,
    calls,
    setConfig: (c) => {
      cfg = { ...cfg, ...c };
    },
    getConfig: () => ({ ...cfg }),
  };
}

// Bridge contract: given a validator CLI argv and a mock subprocess, enforce
// persistence-blocking semantics. Non-zero exit → refuse + raw Python reason
// code from stderr. Subprocess throw → refuse + OPENCODE_DRIVER_INVOKE_FAILED.
// Exit 0 → allow. This is the contract the US-0124 plugin hook must follow;
// US-0125 authors the contract + mapping data, US-0124 authors the hook.
export interface BridgeEnforceResult {
  allowed: boolean;
  reasonCode?: string;
  validatorArgv?: string[];
}

export function bridgeEnforceWrite(
  validatorArgv: string[],
  mockSubprocess: MockSubprocessFn,
): BridgeEnforceResult {
  let proc: MockSubprocessResult;
  try {
    proc = mockSubprocess(validatorArgv);
  } catch {
    return {
      allowed: false,
      reasonCode: "OPENCODE_DRIVER_INVOKE_FAILED",
      validatorArgv,
    };
  }
  if (proc.status !== 0) {
    const reasonCode = proc.stderr.trim() || "VALIDATOR_NON_ZERO_EXIT";
    return { allowed: false, reasonCode, validatorArgv };
  }
  return { allowed: true, validatorArgv };
}
