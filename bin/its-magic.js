#!/usr/bin/env node
const path = require("path");
const { spawnSync } = require("child_process");

function parseArgs(argv) {
  const args = { target: process.cwd(), mode: "missing", backup: false, create: false };
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
    if (a === "--help" || a === "-h") {
      return { help: true };
    }
  }
  return args;
}

function printHelp() {
  console.log(`its-magic

Usage:
  npx its-magic --target <path> --mode missing [--backup] [--create]

Options:
  --target   Target repository path (default: current directory)
  --mode     missing | overwrite | interactive (default: missing)
  --backup   Backup files before overwrite
  --create   Create target directory if missing
`);
}

const args = parseArgs(process.argv.slice(2));
if (args.help) {
  printHelp();
  process.exit(0);
}

const root = path.resolve(__dirname, "..");
const isWin = process.platform === "win32";

if (isWin) {
  const installer = path.join(root, "gsd-installer.ps1");
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
  const res = spawnSync("powershell", psArgs, { stdio: "inherit" });
  process.exit(res.status || 0);
} else {
  const installer = path.join(root, "gsd-installer.sh");
  const shArgs = [
    installer,
    "--target",
    args.target,
    "--mode",
    args.mode,
  ];
  if (args.backup) shArgs.push("--backup");
  if (args.create) shArgs.push("--create");
  const res = spawnSync("sh", shArgs, { stdio: "inherit" });
  process.exit(res.status || 0);
}
