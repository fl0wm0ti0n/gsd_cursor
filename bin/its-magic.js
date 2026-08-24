#!/usr/bin/env node
const path = require("path");
const { spawnSync } = require("child_process");
const packageJson = require("../package.json");

const REPO_URL = "https://github.com/fl0wm0ti0n/its-magic";

function printBanner() {
  const M = "\x1b[1;35m";
  const C = "\x1b[1;36m";
  const Y = "\x1b[1;33m";
  const R = "\x1b[0m";
  console.log("");
  console.log(`${M}  ██╗████████╗███████╗      ███╗   ███╗ █████╗  ██████╗ ██╗ ██████╗${R}`);
  console.log(`${M}  ██║╚══██╔══╝██╔════╝      ████╗ ████║██╔══██╗██╔════╝ ██║██╔════╝${R}`);
  console.log(`${M}  ██║   ██║   ███████╗█████╗██╔████╔██║███████║██║  ███╗██║██║     ${R}`);
  console.log(`${C}  ██║   ██║   ╚════██║╚════╝██║╚██╔╝██║██╔══██║██║   ██║██║██║     ${R}`);
  console.log(`${C}  ██║   ██║   ███████║      ██║ ╚═╝ ██║██║  ██║╚██████╔╝██║╚██████╗${R}`);
  console.log(`${C}  ╚═╝   ╚═╝   ╚══════╝      ╚═╝     ╚═╝╚═╝  ╚═╝ ╚═════╝ ╚═╝ ╚═════╝${R}`);
  console.log("");
  console.log(`${Y}                         AI dev team${R}`);
  console.log("");
}

function parseArgs(argv) {
  const args = {
    target: process.cwd(),
    mode: "missing",
    backup: false,
    create: false,
    cleanRepo: false,
    yes: false,
    help: false,
    version: false,
    host: "cursor",
    hostSeen: 0,
    hostError: null,
  };

  if (argv.length === 0) {
    args.help = true;
    return args;
  }

  const first = argv[0];
  if (first === "help") return { ...args, help: true };
  if (first === "version") return { ...args, version: true };
  if (first === "clean") {
    args.cleanRepo = true;
    argv = argv.slice(1);
  }

  for (let i = 0; i < argv.length; i += 1) {
    const a = argv[i];
    if (a === "--target" && argv[i + 1]) {
      args.target = argv[i + 1];
      i += 1;
      continue;
    }
    if (a === "--mode" && argv[i + 1]) {
      args.mode = argv[i + 1];
      i += 1;
      continue;
    }
    if (a === "--host" && argv[i + 1]) {
      args.hostSeen += 1;
      if (args.hostSeen > 1) {
        args.hostError = "duplicate";
        continue;
      }
      const raw = argv[i + 1];
      const normalized = String(raw).toLowerCase().trim();
      if (normalized !== "cursor" && normalized !== "opencode" && normalized !== "both") {
        args.hostError = "invalid";
        args.host = normalized;
      } else {
        args.host = normalized;
      }
      i += 1;
      continue;
    }
    if (a === "--backup") {
      args.backup = true;
      continue;
    }
    if (a === "--create") {
      args.create = true;
      continue;
    }
    if (a === "--clean-repo") {
      args.cleanRepo = true;
      continue;
    }
    if (a === "--yes") {
      args.yes = true;
      continue;
    }
    if (a === "--help" || a === "-h") {
      args.help = true;
      continue;
    }
    if (a === "--version" || a === "-v") {
      args.version = true;
      continue;
    }
  }
  return args;
}

function printHelp() {
  printBanner();
  console.log(`its-magic v${packageJson.version}
Repository: ${REPO_URL}

Install AI dev team workflow files into any Cursor repository.

Usage:
  its-magic --target <path> [--mode <mode>] [--backup] [--create]
  its-magic --clean-repo [--target <path>] [--yes]
  its-magic --help | --version

Install options:
  --target <path>   Path to the repository where workflow files are installed.
                    If omitted you will be prompted interactively.
  --mode <mode>     How to handle files that already exist in the target:
                      missing      Only copy files that do not exist yet (default).
                                   Safe for repos that already have some workflow files.
                      overwrite    Replace every file, even if it already exists.
                                   Combine with --backup to keep a snapshot first.
                      interactive  Ask per file whether to overwrite or skip.
                      upgrade      Update framework files (commands, rules, agents,
                                   hooks, skills, CI, scripts) while preserving user
                                   data (docs, sprints, handoffs, decisions, runbook).
                                   Use after updating its-magic to a newer version.
  --host <value>    Host-surface switch: cursor | opencode | both (default: cursor).
                    Normalized case-insensitive and whitespace-trimmed before validate.
                    Unknown value -> exit with INSTALL_HOST_INVALID.
                    Duplicate --host argv -> fail closed INSTALL_HOST_INVALID (no last-wins).
                    --host gates ONLY .cursor/ and .opencode/ trees; kernel paths
                    (docs/, scripts/, its_magic/, handoffs/, decisions/, sprints/,
                    .github/workflows/) always install regardless of --host.
                    clean --host cursor after --host both leaves .opencode/ in place
                    and emits OPENCODE_ORPHANED_BY_CLEAN_CURSOR; upgrade --host cursor
                    after --host both emits OPENCODE_STALE_BY_UPGRADE_CURSOR.
  --backup          Before overwriting, save existing files to backups/<timestamp>/.
                    Ignored when mode is "missing" (nothing gets replaced).
  --create          Create the target directory if it does not exist.
  Note: installer bootstraps runbook TEST/LINT/TYPECHECK commands from
        OS+stack detection; unresolved TEST_COMMAND fails fast with
        [RUNBOOK_BOOTSTRAP_ERROR] diagnostics.
  Note: scratchpad Model B: .cursor/scratchpad.md is materialized when missing;
        post-install always refreshes .cursor/scratchpad.local.example.md from the
        template before baseline handling. PowerShell/bash installers require
        Python 3 on PATH for merged scratchpad validation. Recovery:
        python installer.py --scratchpad-postinstall --target <repo> --mode missing

Clean options:
  --clean-repo      Remove all its-magic workflow artifacts from the target repo
                    (owned paths from installer manifest, including .cursor,
                    docs/product, docs/engineering, docs/user-guides, sprints,
                    handoffs, decisions, workflow scripts, CI files, and
                    installer metadata under its_magic/ (legacy .its-magic-version
                    is also removed when present). Your own source code is never touched.
  --target <path>   Repo to clean (default: current directory).
  --yes             Skip the confirmation prompt.

Info:
  --help, -h        Show this help and exit.
  --version, -v     Print the installed version and exit.

Examples:
  its-magic --target . --mode missing            Safe first-time setup
  its-magic --target . --mode upgrade             Update framework, keep user data
  its-magic --target . --mode upgrade --backup    Upgrade with backup of old files
  its-magic --target . --mode overwrite --backup  Replace all files, keep backup
  its-magic --clean-repo --target . --yes         Remove workflow artifacts silently
`);
}

const args = parseArgs(process.argv.slice(2));
if (args.help) {
  printHelp();
  process.exit(0);
}
if (args.version) {
  console.log(`its-magic v${packageJson.version}`);
  process.exit(0);
}
if (args.hostError) {
  const reason = args.hostError === "duplicate"
    ? "duplicate --host argv (no last-wins)"
    : `unknown host value '${args.host}'`;
  console.log(`[INSTALL_HOST_INVALID] ${reason}. Accepted: cursor | opencode | both (default: cursor).`);
  process.exit(1);
}

const root = path.resolve(__dirname, "..");
const isWin = process.platform === "win32";

if (isWin) {
  const installer = path.join(root, "installer.ps1");
  const psArgs = [
    "-ExecutionPolicy",
    "Bypass",
    "-File",
    installer,
    "-Target",
    args.target,
    "-Mode",
    args.mode,
    "-InstallHost",
    args.host,
  ];
  if (args.backup) psArgs.push("-Backup");
  if (args.create) psArgs.push("-Create");
  if (args.cleanRepo) psArgs.push("-CleanRepo");
  if (args.yes) psArgs.push("-Yes");
  const res = spawnSync("powershell", psArgs, { stdio: "inherit" });
  process.exit(res.status || 0);
} else {
  const installer = path.join(root, "installer.sh");
  const shArgs = [
    installer,
    "--target",
    args.target,
    "--mode",
    args.mode,
    "--host",
    args.host,
  ];
  if (args.backup) shArgs.push("--backup");
  if (args.create) shArgs.push("--create");
  if (args.cleanRepo) shArgs.push("--clean-repo");
  if (args.yes) shArgs.push("--yes");
  const res = spawnSync("sh", shArgs, { stdio: "inherit" });
  process.exit(res.status || 0);
}
