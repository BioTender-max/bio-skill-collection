const { execSync } = require("node:child_process");
const fs = require("node:fs");
const path = require("node:path");

const STATUS_FILE = path.join("/tmp", "neuroclaw_claw_shell_status.json");

function ensureSession() {
  try {
    execSync('tmux has-session -t claw', { stdio: "ignore" });
  } catch {
    execSync('tmux new -s claw -d');
  }
}

function sendCommand(cmd) {
  const escaped = cmd.replace(/"/g, '\\"');
  const status = {
    command: cmd,
    started_at: Date.now(),
    tmux_session: "claw",
  };
  try {
    fs.writeFileSync(STATUS_FILE, JSON.stringify(status, null, 2), "utf8");
  } catch {
    // status display is best-effort only
  }
  execSync(`tmux send-keys -t claw "${escaped}" C-m`);
}

function clearCommandStatus() {
  try {
    if (fs.existsSync(STATUS_FILE)) {
      fs.unlinkSync(STATUS_FILE);
    }
  } catch {
    // ignore
  }
}

function readOutput() {
  try {
    const buf = execSync('tmux capture-pane -t claw -p -S -200');
    return buf.toString("utf8");
  } catch (e) {
    return `ERROR READING TMUX OUTPUT: ${e.message}`;
  }
}

function isDangerous(cmd) {
  const bad = ["sudo", " rm ", " rm-", "reboot", "shutdown", "mkfs", "dd "];
  const lower = ` ${cmd.toLowerCase()} `;
  return bad.some(k => lower.includes(k));
}

// MAIN ENTRYPOINT
// OpenClaw will call this function when using the skill tool
async function claw_shell_run(input) {
  const { command } = input;
  if (!command || typeof command !== "string") {
    return { error: "command is required" };
  }

  if (isDangerous(command)) {
    return {
      error: "dangerous_command",
      message: `Command looks dangerous. Ask the user for explicit approval before running: ${command}`
    };
  }

  ensureSession();
  sendCommand(command);

  // small delay so command can run
  await new Promise(r => setTimeout(r, 500));

  const output = readOutput();
  // If tmux is back at a shell prompt, clear the transient status file.
  try {
    const current = execSync("tmux display-message -p -t claw '#{pane_current_command}'", { stdio: "pipe" })
      .toString("utf8")
      .trim()
      .toLowerCase();
    const shellNames = new Set(["bash", "zsh", "fish", "sh", "dash", "tmux"]);
    if (shellNames.has(current)) {
      clearCommandStatus();
    }
  } catch {
    // keep status file if we cannot inspect tmux
  }
  return { command, output };
}

module.exports = {
  claw_shell_run,
};