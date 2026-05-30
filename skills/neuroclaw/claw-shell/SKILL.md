---
name: claw-shell
description: "Use this skill whenever any NeuroClaw skill, sub-agent, or model needs to execute shell commands safely (e.g. source environment scripts, run recon-all, git operations, conda commands, ls, cat logs, etc.). Triggers include: 'run shell', 'execute command', 'shell command', 'tmux claw', 'run in claw session', 'safe shell execution', or any request that requires running terminal commands. This skill is the mandatory gatekeeper for all shell execution in NeuroClaw: it ALWAYS routes commands through the dedicated tmux session `claw`, never touches other sessions, and returns captured output to the calling agent."
license: MIT License (NeuroClaw core skill – freely modifiable within the project)
layer: base
skill_type: tool
dependencies: []
---
# Claw Shell

## Overview

`claw-shell` is the central, safe shell execution layer for the entire NeuroClaw system. All long-running or system-level commands (FreeSurfer recon-all, dependency installation steps, git operations, conda commands, file operations, etc.) are routed through this skill.

**Core principles:**
- **Always** uses the dedicated tmux session named `claw` (creates it automatically if missing).
- **Never** touches any other tmux session or runs commands directly in the main shell.
- Captures the latest pane output and returns it to the calling skill/agent.
- Enforces strict safety rules: dangerous commands (sudo, rm, reboot, etc.) trigger an explicit user confirmation step before execution.

This design solves the problems of the main agent not proactively installing dependencies and handling long-running commands, as identified in the MedicalClaw evaluation, by providing centralized logging, detachment support, and safe execution.

## Quick Reference

| Type                              | Example Commands                                      | Behavior |
|-----------------------------------|-------------------------------------------------------|----------|
| Safe (direct run)                 | `ls -la`, `cat log.txt`, `git status`                 | Executes immediately in `claw` session |
| Environment setup                 | `source $FREESURFER_HOME/SetUpFreeSurfer.sh`          | Executes and returns output |
| Long-running pipeline             | `recon-all -subjid sub-001 -all -parallel`            | Runs in background-capable tmux pane |
| Dangerous (requires confirmation) | `rm -rf ...`, `sudo apt install ...`, `docker system prune -a` | Asks user “YES” before proceeding |

**Tool Interface**  
**Tool name:** `claw_shell_run`  
**Input:**  
- `command` (string, required): the full shell command to run inside the `claw` tmux session.

## Installation

This is a core NeuroClaw skill and requires no external packages beyond tmux.

**One-time setup (run once via dependency-planner or manually):**

```bash
# Ensure tmux session exists
tmux new -s claw -d || true
```

To register in NeuroClaw:
```bash
# Place files in: skills/claw-shell/
# Update SOUL.md and/or USER.md to register as the default shell executor
```

## Usage Examples

### Example 1: Simple command

```text
# Skill call:
claw_shell_run with command="ls -la /data"

# Returns captured tmux pane output directly to the agent
```

### Example 2: FreeSurfer environment + recon-all (delegated from freesurfer-tool)

```text
# Internal commands sent to claw-shell:
1. export FREESURFER_HOME=/usr/local/freesurfer
2. source $FREESURFER_HOME/SetUpFreeSurfer.sh
3. recon-all -subjid sub-001 -i ./T1.nii.gz -all -parallel -openmp 8
```

### Example 3: Dangerous command (safety trigger)

```text
# User requests: rm -rf /tmp/old_data
# claw-shell automatically responds:
"Warning: This command contains 'rm'. Do you confirm execution? Reply YES to proceed."
```

## NeuroClaw recommended wrapper script

```python
# claw_shell.py
import argparse
import sys

# In real NeuroClaw this is implemented as a tool call, not direct Python execution
def claw_shell_run(command: str):
    print(f"[claw-shell] Sending to tmux session 'claw':")
    print(f"  {command}")
    print("\n[Simulation] Command executed. Output would be captured here.")
    # Real implementation:
    # return agent.tool_call("claw_shell_run", {"command": command})

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="NeuroClaw Claw-Shell Wrapper")
    parser.add_argument("--command", required=True, help="Shell command to run in tmux session 'claw'")
    args = parser.parse_args()
    claw_shell_run(args.command)
```

## Important Notes & Limitations

- **Always runs inside tmux session `claw`** — never in the main shell or any other session.
- **Safety enforcement**:
  - Commands containing `sudo`, `rm -rf`, `reboot`, `shutdown`, `docker system prune`, destructive `chmod`, etc. **must** receive explicit user “YES” confirmation.
  - Long-running commands (e.g. recon-all) are safe because they run detached in tmux.
- Output is always captured and returned to the calling skill.
- Session is persistent across NeuroClaw runs (ideal for monitoring long pipelines).

## When to Call This Skill

- Any skill (`freesurfer-tool`, `dependency-planner`, `git-essentials`, etc.) needs to run shell commands.
- Post-installation environment variable setup.
- File operations, log checking, or any terminal action inside NeuroClaw.

## Complementary / Related Skills

- `dependency-planner` → delegates installation and environment variable commands here

## Reference

Custom core skill designed for NeuroClaw to provide safe, tmux-based shell execution while solving the dependency and long-running command issues from the MedicalClaw evaluation.

---
Created At: 2026-03-19 20:00 HKT  
Last Updated At: 2026-03-25 16:22 HKT  
Author: chengwang96