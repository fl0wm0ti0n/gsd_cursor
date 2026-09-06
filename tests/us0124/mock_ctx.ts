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

export interface MockEditorAddCall {
  name: string;
  description?: string;
  execute?: (args: {
    sessionID: string;
    prompt?: string;
    delivery?: string;
  }) => Promise<unknown>;
}

export interface MockEventSubscribeCall {
  registered: boolean;
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
  // BUG-0015 additive attach surfaces (extend, do not replace US-0124 fields)
  command?: {
    transform: (
      cb: (editor: {
        add: (def: MockEditorAddCall) => void;
      }) => void,
    ) => void | Promise<void>;
  };
  event?: {
    subscribe: (cb: (event: unknown) => unknown) => void;
  };
  options: Record<string, unknown>;
  // test inspection
  _calls: {
    create: MockCreateCall[];
    wait: MockWaitCall[];
    hook: MockHookCall[];
    editorAdd: MockEditorAddCall[];
    eventSubscribe: MockEventSubscribeCall[];
  };
  _config: MockCreateConfig;
  _setCreate: (cfg: MockCreateConfig) => void;
  _result: string;
  _setResult: (r: string) => void;
  _waitGate: Promise<void> | null;
  _setWaitGate: (gate: Promise<void> | null) => void;
  _eventHandler: ((event: unknown) => unknown) | null;
  _autoExecute:
    | ((args: {
        sessionID: string;
        prompt?: string;
        delivery?: string;
      }) => Promise<unknown>)
    | null;
}

function freshSessionID(parentID: string): string {
  return `child-${parentID}-${Math.random().toString(36).slice(2, 10)}`;
}

export interface CreateMockCtxOptions {
  /** When false, omit command.transform (missing primary attach). Default true. */
  withCommandTransform?: boolean;
  /** When true, register event.subscribe (secondary attach). Default false. */
  withEventSubscribe?: boolean;
}

export function createMockCtx(
  config: MockCreateConfig = {},
  result = "phase-complete",
  options: CreateMockCtxOptions = {},
): MockCtx {
  const withCommandTransform = options.withCommandTransform !== false;
  const withEventSubscribe = options.withEventSubscribe === true;
  const calls: MockCtx["_calls"] = {
    create: [],
    wait: [],
    hook: [],
    editorAdd: [],
    eventSubscribe: [],
  };
  let waitGate: Promise<void> | null = null;
  let eventHandler: ((event: unknown) => unknown) | null = null;
  let autoExecute:
    | ((args: {
        sessionID: string;
        prompt?: string;
        delivery?: string;
      }) => Promise<unknown>)
    | null = null;

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
        if (waitGate) {
          await waitGate;
        }
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
    _waitGate: null,
    _setWaitGate(gate) {
      waitGate = gate;
      ctx._waitGate = gate;
    },
    _eventHandler: null,
    _autoExecute: null,
  };

  if (withCommandTransform) {
    ctx.command = {
      transform(cb) {
        const editor = {
          add(def: MockEditorAddCall) {
            calls.editorAdd.push(def);
            if (typeof def.execute === "function") {
              autoExecute = def.execute;
              ctx._autoExecute = def.execute;
            }
          },
        };
        cb(editor);
      },
    };
  }

  if (withEventSubscribe) {
    ctx.event = {
      subscribe(cb) {
        calls.eventSubscribe.push({ registered: true });
        eventHandler = cb;
        ctx._eventHandler = cb;
      },
    };
  }

  return ctx;
}

export const MOCK_ORCHESTRATOR_SESSION_ID = "orchestrator-session-0";
