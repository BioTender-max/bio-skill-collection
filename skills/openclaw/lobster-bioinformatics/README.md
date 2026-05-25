# Lobster Claude Code Skill

This directory contains the Agent Skill for using Lobster AI with [Claude Code](https://claude.com/claude-code).

## What is this?

This Skill allows Claude Code to automatically invoke Lobster for bioinformatics analyses. When you ask Claude Code to analyze genomics data, search papers, or work with biological datasets, it will use Lobster seamlessly.

## Installation

### Quick Install (Recommended)

```bash
curl -fsSL https://raw.githubusercontent.com/the-omics-os/lobster-local/main/claude-skill/install.sh | bash
```

### Manual Install

```bash
# 1. Ensure Lobster is installed
uv tool install lobster-ai
lobster init

# 2. Create skills directory
mkdir -p ~/.claude/skills/lobster

# 3. Copy SKILL.md
cp claude-skill/SKILL.md ~/.claude/skills/lobster/SKILL.md

# 4. Restart Claude Code
claude
```

## Usage

Once installed, just ask Claude Code naturally:

```bash
# In Claude Code CLI:
You: "Analyze the single-cell data in data/experiment.h5ad"
You: "Download GSE109564 and run quality control"
You: "Find papers about CRISPR screens and extract their datasets"
```

Claude Code will automatically invoke Lobster when it detects bioinformatics tasks.

## Verification

Check that the Skill is installed:

```bash
ls ~/.claude/skills/lobster/SKILL.md

# Or ask Claude Code directly:
claude
You: "What skills are available?"
# Should show "lobster-bioinformatics" in the list
```

## Uninstall

```bash
rm -rf ~/.claude/skills/lobster
```

## Troubleshooting

**Skill not activating:**
- Verify installation: `cat ~/.claude/skills/lobster/SKILL.md`
- Restart Claude Code
- Check Lobster is installed: `which lobster`

**Lobster errors:**
- Configure API keys: `lobster init`
- Check configuration: `lobster config show`
- Test directly: `lobster query "test"`

## Learn More

- [Agent Skills Documentation](https://docs.claude.com/en/docs/agents-and-tools/agent-skills)
- [Lobster Documentation](https://github.com/the-omics-os/lobster-local/wiki)
- [Examples Cookbook](https://github.com/the-omics-os/lobster-local/wiki/27-examples-cookbook)
