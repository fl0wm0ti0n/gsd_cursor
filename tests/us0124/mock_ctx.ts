// US-0124 — MockCtx harness for the orchestrator plugin (DEC-0124 §3 / DQ3).
// Implements the v2 plugin context subset the orchestrator uses:
//   ctx.session.create / ctx.session.wait / ctx.session.prompt
//   ctx.tool.hook (no-op recorder)
//   ctx.options (readonly)
// session.create accepts scripted flags to drive the three-case detection
// matrix (DEC-0124 §5): null return, generic throw, identical-id return,
// plus the missing-primitive throw case (throw-discrimination rule).

export interface MockCreateConfig {
  nextSessionID?: string;
  throwOnCreate?: boolean;
  throwMissingPrimitive?: boolean;
  returnNull?: boolean;
  identicalID?: boolean;
}

export interface MockCreateCall {
  parentID: string;
  agent: string;
  prompt: string;
}

export interface MockWaitCall {
  sessionID: string;
}

export interface MockHookCall {
  event: string;
}

export interface MockCtx {
  session: {
    create: (args: {
      parentID: string;
      agent: string;
      prompt: string;
    }) => Promise<{ sessionID?: string } | null>;
    wait: (sessionID: string) => Promise<string>;
    prompt: (sessionID: string, message: string) => Promise<unknown>;
  };
  tool: {
    hook: (event: string, cb: (event: unknown) => unknown) => unknown;
  };
  options: Record<string, unknown>;
  // test inspection
  _calls: {
    create: MockCreateCall[];
    wait: MockWaitCall[];
    hook: MockHookCall[];
  };
  _config: MockCreateConfig;
  _setCreate: (cfg: MockCreateConfig) => void;
  _result: string;
  _setResult: (r: string) => void;
}

function freshSessionID(parentID: string): string {
  return `child-${parentID}-${Math.random().toString(36).slice(2, 10)}`;
}

export function createMockCtx(
  config: MockCreateConfig = {},
  result = "phase-complete",
): MockCtx {
  const calls: MockCtx["_calls"] = {
    create: [],
    wait: [],
    hook: [],
  };
  const ctx: MockCtx = {
    session: {
      async create(args) {
        calls.create.push({ ...args });
        if (config.throwOnCreate) {
          if (config.throwMissingPrimitive) {
            throw new TypeError(
              "ctx.session.create is not a function (host cannot spawn)",
            );
          }
          throw new Error("subagent not found");
        }
        if (config.returnNull) {
          return null;
        }
        const sessionID = config.identicalID
          ? args.parentID
          : (config.nextSessionID ?? freshSessionID(args.parentID));
        return { sessionID };
      },
      async wait(sessionID) {
        calls.wait.push({ sessionID });
        return result;
      },
      async prompt(_sessionID, _message) {
        return result;
      },
    },
    tool: {
      hook(event, _cb) {
        calls.hook.push({ event });
        return undefined;
      },
    },
    options: {},
    _calls: calls,
    _config: config,
    _setCreate(cfg) {
      Object.assign(config, cfg);
    },
    _result: result,
    _setResult(r) {
      result = r;
    },
  };
  return ctx;
}

export const MOCK_ORCHESTRATOR_SESSION_ID = "orchestrator-session-0";
