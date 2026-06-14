#!/usr/bin/env node
const fs = require("fs");
const path = require("path");
const { spawnSync } = require("child_process");

const M = "\x1b[1;35m";
const C = "\x1b[1;36m";
const Y = "\x1b[1;33m";
const G = "\x1b[1;32m";
const W = "\x1b[1;37m";
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
console.log(`${G}                    Installation complete!${R}`);
console.log("");
console.log(`${W}  Run: its-magic --help${R}`);
console.log("");

const pkgRoot = path.resolve(__dirname, "..");
const templateRoot = path.join(pkgRoot, "template");
const bootstrapScript = path.join(pkgRoot, "scripts", "dev_environment_lib.py");

function detectConsumerRepoRoot() {
  let dir = process.cwd();
  for (let depth = 0; depth <= 6; depth += 1) {
    const scratchpad = path.join(dir, ".cursor", "scratchpad.md");
    const versionSentinel = path.join(dir, "its_magic", ".its-magic-version");
    if (fs.existsSync(scratchpad) || fs.existsSync(versionSentinel)) {
      return dir;
    }
    const parent = path.dirname(dir);
    if (parent === dir) {
      break;
    }
    dir = parent;
  }
  return null;
}

function resolvePythonCommand() {
  if (process.platform === "win32") {
    return "python";
  }
  return "python3";
}

function runDevEnvBootstrap() {
  const repoRoot = detectConsumerRepoRoot();
  if (!repoRoot) {
    console.log("[DEV_ENV_BOOTSTRAP_SKIP] no consumer repository detected");
    return;
  }
  if (!fs.existsSync(bootstrapScript)) {
    console.log(
      "[DEV_ENV_BOOTSTRAP_ERROR] bootstrap helper missing; copy template/.cursor/dev-environment.json.example manually"
    );
    return;
  }
  const py = resolvePythonCommand();
  const res = spawnSync(
    py,
    [
      bootstrapScript,
      "--bootstrap",
      "--target",
      repoRoot,
      "--source-root",
      templateRoot,
    ],
    { encoding: "utf-8" }
  );
  if (res.stdout) {
    process.stdout.write(res.stdout);
  }
  if (res.stderr) {
    process.stderr.write(res.stderr);
  }
  if (res.status === 1) {
    console.log(
      "[DEV_ENV_BOOTSTRAP_ERROR] bootstrap failed; copy template/.cursor/dev-environment.json.example to .cursor/dev-environment.json"
    );
  }
}

runDevEnvBootstrap();
