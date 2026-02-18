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
  --backup          Before overwriting, save existing files to backups/<timestamp>/.
                    Ignored when mode is "missing" (nothing gets replaced).
  --create          Create the target directory if it does not exist.

Clean options:
  --clean-repo      Remove all its-magic workflow artifacts from the target repo
                    (.cursor, docs/product, docs/engineering, sprints, handoffs,
                    decisions). Your own source code is never touched.
  --target <path>   Repo to clean (default: current directory).
  --yes             Skip the confirmation prompt.

Info:
  --help, -h        Show this help and exit.
  --version, -v     Print the installed version and exit.

Examples:
  its-magic --target . --mode missing          Safe first-time setup
  its-magic --target . --mode overwrite --backup  Update all files, keep backup
  its-magic --clean-repo --target . --yes      Remove workflow artifacts silently
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
  ];
  if (args.backup) shArgs.push("--backup");
  if (args.create) shArgs.push("--create");
  if (args.cleanRepo) shArgs.push("--clean-repo");
  if (args.yes) shArgs.push("--yes");
  const res = spawnSync("sh", shArgs, { stdio: "inherit" });
  process.exit(res.status || 0);
}
