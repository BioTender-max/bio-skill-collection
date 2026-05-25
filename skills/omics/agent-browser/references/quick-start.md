# Agent Browser Quick Start (paraphrased)

Source: https://agent-browser.dev/quick-start

## Install
- Install CLI: `npm install -g agent-browser`
- Install Chromium: `agent-browser install`
- Linux deps (if needed): `agent-browser install --with-deps`

## Core flow
- Open a page: `agent-browser open https://example.com`
- Snapshot interactive elements for AI refs: `agent-browser snapshot -i --json`
- Use element refs for actions:
  - `agent-browser click @e2`
  - `agent-browser fill @e3 "test@example.com"`
- Capture state: `agent-browser screenshot --full`

## Helpful flags
- `--json` for structured output
- `--headed` to show a visible browser

## Agent mode note
- The docs recommend adding clear instructions in AGENTS/CLAUDE rules so agents default to agent-browser for browser tasks.
